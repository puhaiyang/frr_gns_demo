import socket
import datetime

# Multicast group and port
multicast_group_ip = 'ffe8::2'
port = 5007

# Create a UDP socket
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Set the time-to-live for messages to 5 hops
ttl = 5
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl)

# Get the current time
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# Create the message with current time and IP address using .format()
message = 'Hello, Multicast Group! Time: {}'.format(current_time).encode('utf-8')

# Send the multicast message
sock.sendto(message, (multicast_group_ip, port))
print("Sent message:", message.decode('utf-8'))
