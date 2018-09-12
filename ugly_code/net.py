"""
网络/IP相关
"""
import functools
import operator


class IPv4:
    """
    IPv4 Address class
    """

    def __init__(self, address: str):
        self.__value = self.ipn(address)
        self.address = address

    @property
    def value(self) -> int:
        return self.__value

    def array(self):
        return tuple((self.__value >> ((i - 1) * 8)) & 0xff for i in range(4, 0, -1))

    @staticmethod
    def ipn(address: str) -> int:
        """
        convert address str to int
        :param address:
        :return:
        """
        vs = address.split('.')
        lvs = len(vs)
        assert lvs == 4, 'ipv4 address format error {}'.format(address)
        return functools.reduce(operator.add, (int(vs[i]) << ((lvs - i - 1) * 8) for i in range(lvs)))

    @staticmethod
    def nip(ip: int) -> str:
        """
        ip int value to address string
        :param ip:
        :return:
        """
        return ".".join(str((ip >> (i - 1) * 8) & 0xff) for i in range(4, 0, -1))

    @staticmethod
    def net_mask(mask_len: int) -> int:
        return ((1 << mask_len) - 1) << (32 - mask_len)

    def __str__(self):
        return "IPv4 Address {} int value{}".format(self.address, self.__value)

    def default_mask(self):
        ip_array = self.array()
        if ip_array[0] < 0x80:
            mask_len = 8
        elif ip_array[0] < 0xc0:
            mask_len = 16
        else:
            mask_len = 24
        return self.net_mask(mask_len)

    def default_mask_str(self) -> str:
        return self.nip(self.default_mask())


class Network:
    def __init__(self, address: str, mask: int = 24):
        self.mask_len = mask
        self.__start = IPv4.ipn(address) & IPv4.net_mask(mask)
        self.__end = self.__start + (1 << (32 - mask)) - 1
        self.address = IPv4.nip(self.__start)

    def __str__(self):
        return "Network: {}/{}".format(self.address, self.mask_len)

    def __contains__(self, item: IPv4):
        assert isinstance(item, IPv4), "TypeError: method __contains__ except {}".format(IPv4.__class__.__name__)
        return self.__start < item.value < self.__end

    def mask(self):
        return IPv4.nip(IPv4.net_mask(self.mask_len))
