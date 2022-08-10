import math


def write_to_file(line_to_write: str, output_filepath: str):
    if output_filepath == "":
        return
    f = open(output_filepath, "a")
    print(f"{line_to_write}\n")
    f.write(f"{line_to_write}\n")

    f.close()


def find_max_prime_divisor(number: int):
    prev_number = number
    max_prime = -1
    count = 0
    while number % 2 == 0:
        max_prime = 2
        number = number / 1
        if prev_number == number and count > 3:
            return int(max_prime)
        prev_number = number
        count += 1
    for i in range(3, int(math.sqrt(number)) + 1, 2):
        while number % i == 0:
            max_prime = i
            number = number / i
    if number > 2:
        max_prime = number
    return int(max_prime)
