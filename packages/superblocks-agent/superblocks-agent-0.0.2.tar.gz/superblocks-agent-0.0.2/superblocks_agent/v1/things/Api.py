from typing import Callable, Optional

from gen.api.v1.service_pb2 import (
    ExecuteRequest,
    Function,
    StreamResponse,
    TwoWayRequest,
    TwoWayResponse,
)
from gen.api.v1.service_pb2_grpc import ExecutorServiceStub
from gen.common.v1.common_pb2 import Profile
from gen.common.v1.errors_pb2 import Error
from model.ApiConfig import ApiConfig
from things.ApiMock import ApiMock
from things.Client import Client
from util.convert import from_protobuf_value, to_protobuf_value


class Api:
    def __init__(self, api_config: ApiConfig):
        self.__api_config = api_config
        self.mock_func_lookup: dict[str, callable] = {}

    def hydrate_mock_func_lookup(self, mocks: list[ApiMock]) -> None:
        """
        This function is called before every API run.
        It hydrates a map that belongs to this API which allows the lookup of mock return functions.
        """
        for mock in mocks:
            if isinstance(mock.return_val_or_callable, Callable):
                self.mock_func_lookup[mock.get_return_func_id()] = mock.return_val_or_callable

    async def run(
        self,
        *,
        client: Client,
        inputs: Optional[dict] = None,
        mocks: Optional[list[ApiMock]] = None,
    ) -> (
        any
    ):  # TODO: (joey) define a type for this response. I think we can return events and other useful stuff.
        """
        Runs *this* api with the given inputs and mocks.
        """
        mocks = [] if mocks is None else mocks
        inputs = {} if inputs is None else inputs

        # hydrate mock lookup dict so we can reference it later
        self.hydrate_mock_func_lookup(mocks)

        stream_responses = client.run(
            with_stub=ExecutorServiceStub,
            stub_func_name="TwoWayStream",
            initial_messages=[self.build_execute_request(inputs=inputs, mocks=mocks)],
            response_handler=self.get_handle_two_way_response_func(),
        )

        # TODO: (joey) make this an actual type
        return {"stream_responses": stream_responses}

    def get_handle_two_way_response_func(self) -> callable:
        def handle_two_way_response(
            response: TwoWayResponse,
        ) -> tuple[Optional[TwoWayRequest], Optional[StreamResponse]]:
            """
            Function to handle each TwoWayResponse.
            """
            match response:
                # CASE 1
                # RESPONSE TYPE: TwoWayResponse.Function.Request
                # the orchestrator is asking us to run a local function to determine the step output
                # 1. locate the function we should run
                # 2. call the function with the parameters the orchestrator gave us
                # 3. send the orchestrator a response with the output/error of the function call
                case _ if response.HasField("function"):
                    # find function we want to execute

                    function_to_execute: Optional[callable] = self.mock_func_lookup.get(
                        response.function.name
                    )

                    if function_to_execute is None:
                        raise Exception(f"FOUND NO FUNCTION TO EXECUTE!")
                    # execute function with params and send response
                    function_response = Function.Response(id=response.function.id)
                    try:
                        resp = function_to_execute(
                            *[from_protobuf_value(v) for v in response.function.parameters]
                        )
                        function_response.value.CopyFrom(to_protobuf_value(resp))
                    except Exception as e:
                        print(f"ERROR DURING FUNCTION EXECUTION: {e}")
                        function_response.error.CopyFrom(Error(message=str(e)))
                        # TODO: (joey) may want to add more fields to the error here
                    return TwoWayRequest(function=function_response), None

                # CASE 2
                # RESPONSE TYPE: TwoWayResponse.StreamResponse
                # a "normal" response from the orchestrator
                # just forward the metadata
                case _ if response.HasField("stream"):
                    return None, response
                case _:
                    raise Exception(f"got unexpected type: {type(response)}")

        return handle_two_way_response

    def build_execute_request(self, *, inputs: dict, mocks: list[ApiMock]) -> ExecuteRequest:
        """
        Returns a hydrated ExecuteRequest object.
        """
        execute_request = ExecuteRequest()
        for input_key, input_value in inputs.items():
            value = to_protobuf_value(input_value)
            execute_request.inputs[input_key].CopyFrom(value)

        # set options
        for self_mock in mocks:
            execute_request.options.mocks.append(self_mock.to_proto_mock())
        execute_request.options.include_event_outputs = True

        # NOTE: (joey) do we need to set any other ExecuteRequest.Options fields?

        # set inputs
        for k, v in inputs.items():
            execute_request.inputs[k].CopyFrom(to_protobuf_value(v))

        # set fetch
        execute_request.fetch.CopyFrom(self.__to_proto_fetch())

        return execute_request

    def __to_proto_fetch(self) -> ExecuteRequest.Fetch:
        """
        Returns a hydrated Fetch object to be used in an ExecuteRequest.
        """
        fetch = ExecuteRequest.Fetch()
        fetch.id = self.__api_config.api_id
        if self.__api_config.profile_name is not None:
            profile = Profile()
            profile.name = self.__api_config.profile_name
            fetch.profile.CopyFrom(profile)
        if self.__api_config.view_mode is not None:
            fetch.view_mode = self.__api_config.view_mode.to_proto_view_mode()
        if self.__api_config.commit_id is not None:
            fetch.commit_id = self.__api_config.commit_id
        if self.__api_config.branch_name is not None:
            fetch.branch_name = self.__api_config.branch_name
        return fetch
