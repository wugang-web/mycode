import string
import random


def phone_num(num):
    all_phone_nums = set()
    num_start = [
        '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
        '140', '141', '144', '145', '146', '147', '148', '149',
        '150', '151', '152', '153', '155', '156', '157', '158', '159',
        '162', '165', '166', '167', '168',
        '170', '171', '172', '173', '175', '176', '177', '178',
        '180', '181', '182', '183', '184', '185', '186', '187', '188', '189',
        '190', '191', '192', '193', '195', '196', '197', '198', '199',
    ]

    for i in range(0, num):
        start = random.choice(num_start)
        end = ''.join(random.sample(string.digits, 8))
        res = start + end
        all_phone_nums.add(res)
    return all_phone_nums


if __name__ == '__main__':
    print(phone_num(3))