# from grpc import aio
# import concurrent.futures
# import gen.worker.v1.step_executor_pb2_grpc as pb2_grpc
# import gen.api.v1.service_pb2_grpc as apigrpc


# class JGTransport:
#     def __init__(self, address: str = "", port: int = 0) -> None:
#         self._address = address
#         self._port = port
#         self._server = aio.server(concurrent.futures.ThreadPoolExecutor(max_workers=10), options=[])

#     async def init(self):
#         await self.__serve()

#     async def close(self, reason: str = None):
#         await self._server.stop()

#     async def __serve(self):
#         server = self._server
#         executor = apigrpc.ExecutorServiceServicer
#         apigrpc.add_ExecutorServiceServicer_to_server(executor, server)
#         # executor = StepExecutor(self._kv_store)
#         # pb2_grpc.add_StepExecutorServiceServicer_to_server(executor, server)

#         server.add_insecure_port(f"{self._address}:{self._port}")
#         await server.start()
#         await server.wait_for_termination()

import grpc
import streaming_service_pb2
import streaming_service_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = streaming_service_pb2_grpc.StreamingServiceStub(channel)
    messages = [
        streaming_service_pb2.Message(content="Hello"),
        streaming_service_pb2.Message(content="World"),
        streaming_service_pb2.Message(content="!"),
    ]
    responses = stub.TwoWayStream(iter(messages))
    for response in responses:
        print(f"Received: {response.content}")


if __name__ == "__main__":
    run()
