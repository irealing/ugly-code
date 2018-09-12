"""
IP/Network tools
"""
from ._net import IPv4, Network

__all__ = ('IPv4', 'Network')
IPv4 = IPv4
Network = Network
__private_network = (Network('10.0.0.0', 8), Network('172.16.0.0', 16), Network('192.168.0.0', 16))


def __is_private_ip(ip: IPv4) -> bool:
    """
    检测是否私有IP
    :param ip:
    :return:
    """
    return any(ip in __net for __net in __private_network)


IPv4.is_private = __is_private_ip
