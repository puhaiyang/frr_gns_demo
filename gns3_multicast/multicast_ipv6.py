import os
import telnetlib

import time

# Telnet 服务器的主机和端口列表
HOST = "192.168.31.169"
# PORTS = [5006, 5008, 5010]
PORTS = [5006, 5015, 5001]


def telnet_connect(host, port):
    try:
        # 连接到 Telnet 服务器
        tn = telnetlib.Telnet(host, port)
        return tn
    except Exception as e:
        print(f"Telnet connection to {host}:{port} failed: {e}")
        return None


def send_commands(tn, commands):
    for command in commands:
        tn.write(command.encode('ascii') + b"\n")
        time.sleep(1)  # 等待命令执行，适当的延迟可调整
        print(tn.read_very_eager().decode('ascii'))


def read_config_file(config_name, port_index):
    config_filename = f"config/{config_name}-{port_index}.conf"
    if not os.path.isfile(config_filename):
        print(f"Config file {config_filename} does not exist.")
        return None

    with open(config_filename, 'r') as file:
        return file.read()


def main():
    # 打开ospfv3和pimv6
    open_daemons = [
        "sed -i 's/ospf6d=no/ospf6d=yes/g' /etc/frr/daemons",
        "sed -i 's/pim6d=no/pim6d=yes/g' /etc/frr/daemons"
    ]

    for index, port in enumerate(PORTS):
        # 读取配置文件内容
        zebra_config_content = read_config_file("zebra", index + 1)
        if zebra_config_content is None:
            continue
        mgmtd_config_content = read_config_file("mgmtd", index + 1)
        if mgmtd_config_content is None:
            continue
        ospf6d_config_content = read_config_file("ospf6d", index + 1)
        if ospf6d_config_content is None:
            continue
        pim6d_config_content = read_config_file("pim6d", index + 1)
        if pim6d_config_content is None:
            continue
        # 连接到每个 Telnet 服务器
        tn = telnet_connect(HOST, port)
        if tn is None:
            continue

        print(f"Connected to {HOST}:{port}")

        # 打开ipv6的ospf和pim
        send_commands(tn, open_daemons)
        # 开启ipv6转发
        send_commands(tn, [f"cat > /etc/frr/zebra.conf <<EOF\n{zebra_config_content}\nEOF"])
        # 配置接口的ip地址
        send_commands(tn, [f"cat > /etc/frr/mgmtd.conf <<EOF\n{mgmtd_config_content}\nEOF"])
        # 配置ospf
        send_commands(tn, [f"cat > /etc/frr/ospf6d.conf <<EOF\n{ospf6d_config_content}\nEOF"])
        # 配置pim
        send_commands(tn, [f"cat > /etc/frr/pim6d.conf <<EOF\n{pim6d_config_content}\nEOF"])

        # 退出 Telnet 会话
        tn.write(b"exit\n")
        tn.close()
        print(f"Disconnected from {HOST}:{port}")


if __name__ == "__main__":
    main()
