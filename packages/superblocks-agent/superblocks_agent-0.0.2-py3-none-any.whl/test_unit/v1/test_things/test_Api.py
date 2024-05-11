import unittest

from superblocks_agent.v1.enumeration.ViewMode import ViewMode
from superblocks_agent.v1.gen.api.v1.event_pb2 import Event
from superblocks_agent.v1.gen.api.v1.service_pb2 import (
    ExecuteRequest,
    Function,
    Mock,
    StreamResponse,
    TwoWayRequest,
    TwoWayResponse,
)
from superblocks_agent.v1.gen.common.v1.common_pb2 import Profile
from superblocks_agent.v1.gen.common.v1.errors_pb2 import Error
from superblocks_agent.v1.model.ApiConfig import ApiConfig
from superblocks_agent.v1.model.MockApiFilters import MockApiFilters
from superblocks_agent.v1.things.Api import Api
from superblocks_agent.v1.things.ApiMock import ApiMock
from superblocks_agent.v1.util.convert import to_protobuf_value


class TestApi(unittest.TestCase):
    def test_build_execute_request(self):
        api = Api(
            ApiConfig(
                api_id="api_id",
                application_id="app_id",
                branch_name="branch_name",
                commit_id="commit_id",
                profile_name="profile_name",
                page_id="page_id",
                view_mode=ViewMode.DEPLOYED,
            )
        )
        api_mock = ApiMock(
            filters=MockApiFilters(
                integration_type="integration_type", step_name="step_name", inputs={"foo": "bar"}
            ),
            when=lambda _: True,
            return_val_or_callable={"some": "return"},
        )
        actual = api.build_execute_request(
            inputs={
                "str_var": "foo",
                "int_var": 1,
                "bool_var": True,
                "list_var": ["foo", 1, True, {}, []],
                "dict_var": {"foo": "bar"},
                "null_var": None,
            },
            mocks=[api_mock],
        )

        expected_mock_return = Mock.Return(static=to_protobuf_value({"some": "return"}))
        expected = ExecuteRequest(
            inputs={
                "str_var": to_protobuf_value("foo"),
                "int_var": to_protobuf_value(1),
                "bool_var": to_protobuf_value(True),
                "list_var": to_protobuf_value(["foo", 1, True, {}, []]),
                "dict_var": to_protobuf_value({"foo": "bar"}),
                "null_var": to_protobuf_value(None),
            },
            options=ExecuteRequest.Options(
                mocks=[
                    Mock(
                        on=Mock.On(
                            static=Mock.Params(
                                integration_type="integration_type",
                                step_name="step_name",
                                inputs=to_protobuf_value({"foo": "bar"}),
                            ),
                            dynamic=api_mock.get_return_func_id(),
                        )
                    )
                ],
                include_event_outputs=True,
            ),
            fetch=ExecuteRequest.Fetch(
                id="api_id",
                profile=Profile(name="profile_name"),
                view_mode=ViewMode.DEPLOYED.to_proto_view_mode(),
                commit_id="commit_id",
                branch_name="branch_name",
            ),
        )
        # i hate this but have not found a better way
        return_value = getattr(expected.options.mocks[0], "return")
        return_value.CopyFrom(expected_mock_return)

        self.assertEqual(expected, actual)

    def test_handle_two_way_response_invalid_type(self):
        api = Api(ApiConfig(api_id="api_id"))
        func = api.get_handle_two_way_response_func()

        with self.assertRaises(Exception) as context:
            func(TwoWayResponse())
        self.assertEqual(
            "got unexpected type: <class 'api.v1.service_pb2.TwoWayResponse'>",
            str(context.exception),
        )

    def test_handle_two_way_response_stream_type(self):
        api = Api(ApiConfig(api_id="api_id"))
        func = api.get_handle_two_way_response_func()

        stream_response = TwoWayResponse(
            stream=StreamResponse(
                execution="execution",
                event=Event(data=Event.Data(value=to_protobuf_value("some data"))),
            )
        )
        actual = func(stream_response)
        self.assertEqual(2, len(actual))
        self.assertIsNone(actual[0])
        self.assertEqual(stream_response, actual[1])

    def test_handle_two_way_response_function_type_function_call_succeeds(self):
        api = Api(ApiConfig(api_id="api_id"))
        func = api.get_handle_two_way_response_func()

        # have to set up function map first
        def return_func(filters: MockApiFilters) -> dict:
            return {"given_params": filters}

        api_mock = ApiMock(return_val_or_callable=return_func)

        api.hydrate_mock_func_lookup([api_mock])

        function_response = TwoWayResponse(
            function=Function.Request(
                name=api_mock.get_return_func_id(),
                parameters=[to_protobuf_value({"foo": "bar"})],
                id="some_id",
            )
        )
        actual = func(function_response)
        self.assertEqual(2, len(actual))
        self.assertIsNone(actual[1])
        self.assertEqual(
            TwoWayRequest(
                function=Function.Response(
                    value=to_protobuf_value({"given_params": {"foo": "bar"}}), id="some_id"
                )
            ),
            actual[0],
        )

    def test_handle_two_way_response_function_type_function_call_fails(self):
        api = Api(ApiConfig(api_id="api_id"))
        func = api.get_handle_two_way_response_func()

        # have to set up function map first
        def return_func(_: MockApiFilters) -> dict:
            raise Exception("called func error")

        api_mock = ApiMock(return_val_or_callable=return_func)

        api.hydrate_mock_func_lookup([api_mock])

        function_response = TwoWayResponse(
            function=Function.Request(
                name=api_mock.get_return_func_id(),
                parameters=[to_protobuf_value({"foo": "bar"})],
                id="some_id",
            )
        )
        actual = func(function_response)
        self.assertEqual(2, len(actual))
        self.assertIsNone(actual[1])
        self.assertEqual(
            TwoWayRequest(
                function=Function.Response(error=Error(message="called func error"), id="some_id")
            ),
            actual[0],
        )

    def test_hydrate_mock_func_lookup_no_mocks_given(self):
        api = Api(ApiConfig(api_id="api_id"))
        api.hydrate_mock_func_lookup([])
        self.assertEqual({}, api.mock_func_lookup)

    def test_hydrate_mock_func_lookup_only_mocks_with_dict_value_given(self):
        api = Api(ApiConfig(api_id="api_id"))
        mock_1 = ApiMock(return_val_or_callable={"foo": "bar"})
        api.hydrate_mock_func_lookup([mock_1])
        self.assertEqual({}, api.mock_func_lookup)

    def test_hydrate_mock_func_lookup_only_mocks_with_func_value_given(self):
        api = Api(ApiConfig(api_id="api_id"))
        mock_1_func = lambda x: x
        mock_1 = ApiMock(return_val_or_callable=mock_1_func)
        api.hydrate_mock_func_lookup([mock_1])
        self.assertEqual({mock_1.get_return_func_id(): mock_1_func}, api.mock_func_lookup)

    def test_hydrate_mock_func_lookup_mocks_with_func_value_and_mocks_with_dict_value_given(self):
        api = Api(ApiConfig(api_id="api_id"))
        mock_1_func = lambda x: x
        mock_1 = ApiMock(return_val_or_callable=mock_1_func)
        mock_2 = ApiMock(return_val_or_callable={"foo": "bar"})
        api.hydrate_mock_func_lookup([mock_1, mock_2])
        self.assertEqual({mock_1.get_return_func_id(): mock_1_func}, api.mock_func_lookup)
