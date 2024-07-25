import socket
import struct

# bind udp socket
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind a multicast address
multicast_group_ip = 'ffe8::2'
port = 5007
sock.bind(('::', port))

# 告诉内核加入多播组
group = socket.inet_pton(socket.AF_INET6, multicast_group_ip)
# 第二个参数是接口索引，此处修改为实际接口填写
mreq = group + struct.pack('@I', 2)
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

print(f"绑定到组播地址 {multicast_group_ip}:{port}")

# 接收数据
while True:
    data, addr = sock.recvfrom(1024)
    print(f"Received message: {data} from {addr}")
