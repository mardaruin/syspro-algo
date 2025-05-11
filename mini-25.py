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
        self.target_p = p

        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

        self.hash_seeds = [random.randint(0, 2 ** 32 - 1) for _ in range(self.hash_count)]

        self.added_items = 0
        self.false_positives = 0
        self.true_negatives = 0
        self._known_items = set()

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
        self.added_items += 1
        self._known_items.add(item)
        for hash_val in hashes:
            self.bit_array[hash_val] = 1

    def __contains__(self, item):
        hashes = self._get_hashes(item)
        for hash_val in hashes:
            if not self.bit_array[hash_val]:
                self.true_negatives += 1
                return False

        if item not in self._known_items:
            self.false_positives += 1
        return True

    def false_positive_rate(self):
        if (self.false_positives + self.true_negatives) == 0:
            return 0.0
        return self.false_positives / (self.false_positives + self.true_negatives)


def ip_to_bytes(ip):
    return b''.join(bytes([int(part)]) for part in ip.split('.'))

def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


if __name__ == "__main__":
    NUM_IPS_TO_ADD = 100
    NUM_TEST_IPS = 100
    TARGET_P = 0.01

    bloom = BloomFilter(n=NUM_IPS_TO_ADD, p=TARGET_P)

    print(f"Тестирование Bloom-фильтра с параметрами:")
    print(f"- Количество добавляемых IP-адресов: {NUM_IPS_TO_ADD}")
    print(f"- Количество тестовых IP-адресов: {NUM_TEST_IPS}")
    print(f"- Целевая вероятность ложных срабатываний: {TARGET_P:.4f}")
    print("\nГенерация тестовых данных...")

    added_ips = set()
    while len(added_ips) < NUM_IPS_TO_ADD:
        ip = generate_random_ip()
        if ip not in added_ips:
            added_ips.add(ip)
            bloom.add(ip)

    test_ips = set()
    while len(test_ips) < NUM_TEST_IPS:
        ip = generate_random_ip()
        if ip not in added_ips and ip not in test_ips:
            test_ips.add(ip)

    print("\nНачало тестирования...")

    for ip in test_ips:
        _ = ip in bloom

    print("\nРезультаты тестирования:")
    print(f"Добавлено элементов: {bloom.added_items}")
    print(f"Проверено элементов: {NUM_TEST_IPS}")
    print(f"Ложноположительных срабатываний: {bloom.false_positives}")
    print(f"Верных отрицательных результатов: {bloom.true_negatives}")

    actual_p = bloom.false_positive_rate()
    print(f"\nФактическая вероятность ложных срабатываний: {actual_p:.6f}")
    print(f"Ожидаемая вероятность: {TARGET_P:.6f}")
    print(f"Отклонение: {abs(actual_p - TARGET_P):.6f} ({abs(actual_p - TARGET_P) / TARGET_P * 100:.2f}%)")

    print("\nПроверка на известных IP-адресах:")
    test_exists = list(added_ips)[:3]
    test_not_exists = list(test_ips)[:3]

    print("\nДолжны быть найдены:")
    for ip in test_exists:
        print(f"IP {ip}: {'найден' if ip in bloom else 'не найден'} (ожидается: найден)")

    print("\nНе должны быть найдены (но возможны ложные срабатывания):")
    for ip in test_not_exists:
        print(f"IP {ip}: {'найден' if ip in bloom else 'не найден'} (ожидается: не найден)")