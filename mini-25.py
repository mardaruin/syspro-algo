import math
import random
import mmh3
from bitarray import bitarray


class BloomFilter:
    def __init__(self, n, p):
        """
        :param n: прогнозируемое количество элементов
        :param p: желаемая вероятность ложноположительного срабатывания
        """
        self.size = self.calculate_size(n, p)
        self.hash_count = self.calculate_hash_count(n, self.size)

        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

        self.hash_seeds = [random.randint(0, 2 ** 32 - 1) for _ in range(self.hash_count)]

    def calculate_size(self, n, p):
        size = - (n * math.log(p)) / (math.log(2) ** 2)
        return int(math.ceil(size))

    def calculate_hash_count(self, n, m):
        hash_count = (m / n) * math.log(2)
        return int(math.ceil(hash_count))

    def _get_hashes(self, item):
        if isinstance(item, str):
            item = item.encode('utf-8')

        hashes = []
        for seed in self.hash_seeds:
            hash_val = mmh3.hash(item, seed) % self.size
            hashes.append(hash_val)
        return hashes

    def add(self, item):
        hashes = self._get_hashes(item)
        for hash_val in hashes:
            self.bit_array[hash_val] = 1

    def __contains__(self, item):
        hashes = self._get_hashes(item)
        for hash_val in hashes:
            if not self.bit_array[hash_val]:
                return False
        return True


def ip_to_bytes(ip):
    return b''.join(bytes([int(part)]) for part in ip.split('.'))


if __name__ == "__main__":
    bloom = BloomFilter(n=1000, p=0.01)

    ips_to_add = [
        "192.168.1.1",
        "10.0.0.1",
        "172.16.0.1",
        "8.8.8.8",
        "1.1.1.1"
    ]

    for ip in ips_to_add:
        bloom.add(ip)

    test_ips = [
        "192.168.1.1",
        "10.0.0.1",
        "192.168.1.2",
        "10.0.0.2",
        "255.255.255.255"
    ]

    for ip in test_ips:
        if ip in bloom:
            print(f"IP {ip} вероятно есть в фильтре")
        else:
            print(f"IP {ip} точно нет в фильтре")