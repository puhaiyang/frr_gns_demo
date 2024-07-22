import socket
import struct

# 组播地址和端口
# multicast_group_ip = 'ff3e::3'  # 多播地址
multicast_group_ip = 'ff3e::2'  # 多播地址
port = 5007

# 创建UDP socket
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# 设置TTL (Time-to-Live) 以控制多播数据包的范围
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl)

# 发送数据包
message = b'Hello, Multicast Group!'
sock.sendto(message, (multicast_group_ip, port))
print(f"Sent message: {message} to {multicast_group_ip}:{port}")
