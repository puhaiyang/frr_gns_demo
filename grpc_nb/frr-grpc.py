import grpc
import frr_northbound_pb2
import frr_northbound_pb2_grpc

channel = grpc.insecure_channel('192.168.1.10:50051')
stub = frr_northbound_pb2_grpc.NorthboundStub(channel)

# Print Capabilities
request = frr_northbound_pb2.GetCapabilitiesRequest()
response = stub.GetCapabilities(request)
print(response)

print("\n\n\n")

# Print Interface State and Config
request = frr_northbound_pb2.GetRequest()
# request.path.append("/frr-interface:lib")
# request.path.append("/frr-ospf:ospf")
# request.path.append("/frr-route-map:lib")
request.path.append("/frr-route-map:lib/route-map[name='test-map']")
# request.path.append("/frr-route-map:rmap-match-condition")
request.type = frr_northbound_pb2.GetRequest.ALL
request.encoding = frr_northbound_pb2.XML


for r in stub.Get(request):
    print(r.data.data)
