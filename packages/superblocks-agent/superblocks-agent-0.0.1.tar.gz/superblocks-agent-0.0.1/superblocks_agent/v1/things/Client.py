from typing import Optional

import grpc
from gen.api.v1.service_pb2 import StreamResponse
from model.ClientConfig import ClientConfig
from type_.client import GenericMetadata, TwoWayStreamResponseHandler


class Client:
    def __init__(self, client_config: ClientConfig):
        self.__client_config = client_config

    def run(
        self,
        *,
        with_stub: object,
        stub_func_name: str,
        initial_messages: list[object],
        response_handler: TwoWayStreamResponseHandler,
    ) -> list[object]:
        channel = grpc.insecure_channel(target=self.__client_config.agent.endpoint)
        stub = with_stub(channel=channel)
        stub_function = getattr(stub, stub_func_name)

        return self.__handle_two_way_stream(
            stub_function=stub_function,
            messages=initial_messages,
            response_handler=response_handler,
        )

    def __handle_two_way_stream(
        self,
        *,
        stub_function: callable,
        messages: list[object],
        response_handler: TwoWayStreamResponseHandler,
        generic_metadatas: Optional[list[GenericMetadata]] = None,
    ) -> list[StreamResponse]:
        generic_metadatas = [] if generic_metadatas is None else generic_metadatas
        try:
            for response in stub_function(iter(messages)):
                next_request, generic_metadata = response_handler(response)
                if generic_metadata is not None:
                    generic_metadatas.append(generic_metadata)
                if next_request is not None:
                    # recursively call
                    self.__handle_two_way_stream(
                        stub_function=stub_function,
                        messages=[next_request],
                        response_handler=response_handler,
                        generic_metadatas=generic_metadatas,
                    )
        except Exception as e:
            print("Error processing responses:", e)
        finally:
            return generic_metadatas
