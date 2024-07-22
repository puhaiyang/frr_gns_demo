import socket
import struct

# 创建UDP socket
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定到多播组和端口
multicast_group_ip = 'ff3e::2'  # 多播地址
port = 5007
sock.bind(('::', port))  # 绑定到所有接口上的指定端口

# 告诉内核加入多播组
# 第一个参数是IPv6多播地址
# 第二个参数是接口索引（0表示系统默认接口）
group = socket.inet_pton(socket.AF_INET6, multicast_group_ip)
mreq = group + struct.pack('@I', 9)
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

print(f"绑定到组播地址 {multicast_group_ip}:{port}")

# 接收数据
while True:
    data, addr = sock.recvfrom(1024)
    print(f"Received message: {data} from {addr}")

    # 回包逻辑
    response = b'ACK: ' + data
    sock.sendto(response, addr)
    print(f"Sent response: {response} to {addr}")