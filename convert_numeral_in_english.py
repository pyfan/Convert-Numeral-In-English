BASIC_DICT = {
    0: 'zero',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen',
    20: 'twenty',
    30: 'thirty',
    40: 'forty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety'
}

# the units can be added or removed as needed
DIGIT_UNITS = ('', 'thousand', 'million', 'billion', 'trillion', 'quadrillion')


def convert_below100(below100_num):
    """
    :param below100_num: int
    :return: str which converts numeral < 100 in English
    """
    if below100_num in BASIC_DICT.keys():
        return BASIC_DICT[below100_num]
    else:
        ten_div, ten_mod = divmod(below100_num, 10)
        return '{}-{}'.format(BASIC_DICT[ten_div * 10], BASIC_DICT[ten_mod])


def convert_below1000(below1000_num):
    """
    :param below1000_num: int
    :return: str which converts numeral < 1000 in English
    """
    if below1000_num < 100:
        return convert_below100(below1000_num)
    else:
        h_div, h_mod = divmod(below1000_num, 100)
        if h_mod == 0:
            return '{} hundred'.format(BASIC_DICT[h_div])
        else:
            return '{} hundred {}'.format(BASIC_DICT[h_div], convert_below100(h_mod))


def convert_above1000_gen(numeral):
    """
    :param numeral: int
    :return: generator to yield every number-unit pair string
    """
    # split the numeral string into two-parts: first_part matches the units exclude highest unit,
    # the rest_part matches the highest unit.
    split_index = -3 * (len(DIGIT_UNITS) - 1)
    first_part, rest_part = str(numeral)[split_index:], str(numeral)[:split_index]

    # Iterate the first_part to yield each number-unit pair in English format.
    split_first_part = '{:,}'.format(int(first_part)).split(',')
    for number, unit in zip(reversed(split_first_part), DIGIT_UNITS):
        if int(number) != 0:
            yield (convert_below1000(int(number)) + ' ' + unit).strip()

    # Yield the highest unit firstly, then process the rest_part recursively if there is the rest.
    if rest_part:
        yield DIGIT_UNITS[-1]
        # Python versions <3.3 do not support this syntax.
        yield from convert_above1000_gen(rest_part)
        # Syntax for python versions <3.3
        # for item in convert_above1000_gen(rest_part):
        #     yield item


def convert_above1000(above1000_num):
    """
    :param above1000_num: int
    :return: join each item from the generator to render a complete string
    """
    return ' '.join(reversed(list(convert_above1000_gen(above1000_num))))


class ConvertNumeral:
    def __init__(self, numeral):
        if not isinstance(numeral, int):
            raise TypeError('Should be an integer!')
        self.numeral = numeral
        self.convert_func = convert_below1000 if numeral < 1000 else convert_above1000

    def __str__(self):
        return '{:,} => {}'.format(self.numeral, self.convert_func(self.numeral))


if __name__ == '__main__':
    while True:
        num = input("Input an integer ('q' to quit) -> ")
        if num == 'q':
            break
        if not num.isnumeric():
            print('Please input an integer!')
            continue
        try:
            print(ConvertNumeral(int(num)))
        except TypeError as e:
            print(e)
            continue
