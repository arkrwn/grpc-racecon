from concurrent import futures
import grpc

import threading

import counter_pb2
import counter_pb2_grpc


class CounterService(counter_pb2_grpc.CounterServicer):
    def __init__(self):
        self.value = 0
        
        # Use a lock to synchronize access to shared data.
        self.lock = threading.Lock()

    def Increment(self, request, context):
        with self.lock:
            self.value += 1
            
        return counter_pb2.IncrementResponse()

    def GetValue(self, request, context):
        return counter_pb2.GetValueResponse(value=self.value)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
     # Register our servicer class instance to handle gRPC requests.
    counter_pb2_grpc.add_CounterServicer_to_server(CounterService(), server)
    
    server.add_insecure_port('[::]:50051')
  
    print("Starting fixed gRPC server...")
  	
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()