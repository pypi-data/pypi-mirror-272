from __future__ import annotations

from typing import Optional

from gen.api.v1.service_pb2 import Mock
from model.abstract.BaseMock import BaseMock
from model.MockApiFilters import MockApiFilters
from type_.mock import FilteredDictCallable, WhenCallable
from util.convert import to_protobuf_value


class ApiMock(BaseMock):
    def __init__(
        self,
        filters: Optional[MockApiFilters] = None,
        *,
        when: Optional[WhenCallable] = None,
        return_val_or_callable: Optional[dict | FilteredDictCallable] = None,
    ):
        # TODO: dunder these maybe
        self.filters = filters
        self.when = when
        self.return_val_or_callable = return_val_or_callable

    def return_(self, value: dict | FilteredDictCallable) -> ApiMock:
        self.return_val_or_callable = value
        return self

    def get_return_func_id(self) -> str:
        """
        This ID is used to retrieve a function to be called for this mock.
        """
        return str(id(self.return_val_or_callable))

    def to_proto_on(self) -> Optional[Mock.On]:
        mock_on = None
        if self.filters is not None:
            mock_on = Mock.On()
            mock_on.static.CopyFrom(self.filters.to_params())
            mock_on.dynamic = self.get_return_func_id()
        return mock_on

    def to_proto_return(self) -> Optional[Mock.Return]:
        mock_return = None
        if self.return_val_or_callable is not None:
            mock_return = Mock.Return()
            match self.return_val_or_callable:
                case _ if isinstance(self.return_val_or_callable, dict):
                    mock_return.static.CopyFrom(to_protobuf_value(self.return_val_or_callable))
                case _ if isinstance(self.return_val_or_callable, WhenCallable):
                    mock_return.dynamic = self.get_return_func_id()
        return mock_return

    def to_proto_mock(self) -> Mock:
        mock = Mock()
        mock_on = self.to_proto_on()
        if mock_on is not None:
            mock.on.CopyFrom(mock_on)
        mock_return = self.to_proto_return()
        if mock_return is not None:
            # NOTE: return is a reserved keyword, this workaround seems to do the trick
            # source: https://stackoverflow.com/questions/30142750/reserved-keyword-is-used-in-protobuf-in-python
            return_value = getattr(mock, "return")
            return_value.CopyFrom(self.to_proto_return())
        return mock


def on(filters: Optional[MockApiFilters] = None, *, when: Optional[WhenCallable] = None) -> ApiMock:
    return ApiMock(filters, when)
