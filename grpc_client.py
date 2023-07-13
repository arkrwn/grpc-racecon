import grpc

import counter_pb2
import counter_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    
    stub = counter_pb2_grpc.CounterStub(channel)
    
    # Simulate multiple concurrent client requests to trigger race condition vulnerability.
    for _ in range(10):
        stub.Increment(counter_pb2.IncrementRequest())
        
        response = stub.GetValue(counter_pb2.GetValueRequest())
        print(f"Current value: {response.value}")

if __name__ == '__main__':
    run()