import grpc
import frr_northbound_pb2
import frr_northbound_pb2_grpc

channel = grpc.insecure_channel('192.168.31.174:50051')
stub = frr_northbound_pb2_grpc.NorthboundStub(channel)

# Print Capabilities
request = frr_northbound_pb2.GetCapabilitiesRequest()
response = stub.GetCapabilities(request)
print(response)

# Print Interface State and Config
request = frr_northbound_pb2.GetRequest()
request.path.append("/frr-interface:lib")
request.type = frr_northbound_pb2.GetRequest.ALL
request.encoding = frr_northbound_pb2.XML

for r in stub.Get(request):
    print(r.data.data)
