import time
from concurrent import futures
import grpc

import counter_pb2
import counter_pb2_grpc

class CounterService(counter_pb2_grpc.CounterServicer):
    def __init__(self):
        self.value = 0
        
    def Increment(self, request, context):
        # Simulate race condition vulnerability by introducing delay between read-modify-write operations.
        time.sleep(0.5)
        
        self.value += 1
        
        return counter_pb2.IncrementResponse()

    def GetValue(self, request, context):
        return counter_pb2.GetValueResponse(value=self.value)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Register our servicer class instance to handle gRPC requests.
    counter_pb2_grpc.add_CounterServicer_to_server(CounterService(), server)
    
    server.add_insecure_port('[::]:50051')
    
    print("Starting vulnerable gRPC server...")
    
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()