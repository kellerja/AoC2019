def is_ascending_with_exactly_double_digit(num):
    double_digit = False
    previous_digit = 0
    same_digit_count = 1
    for str_digit in str(num):
        digit = int(str_digit)
        if previous_digit > digit:
            return False
        elif previous_digit == digit:
            same_digit_count += 1
        else:
            if same_digit_count == 2:
                double_digit = True
            same_digit_count = 1
        previous_digit = digit
    return double_digit or same_digit_count == 2


def count_matches(start, end, match_fn):
    count = 0
    for num in range(start, end):
        if match_fn(num):
            count += 1
    return count


def read_input():
    with open('input.txt', 'r') as input_file:
        for line in input_file:
            raw_range = line.strip().split('-')
    return int(raw_range[0]), int(raw_range[1])


def write_output(result):
    with open('output.txt', 'w') as output_file:
        output_file.write(str(result))


if __name__ == '__main__':
    low, high = read_input()
    print(f'Counting matching numbers in range ({low}, {high})')
    count = count_matches(low, high, is_ascending_with_exactly_double_digit)
    print(f'Result {count}')
    write_output(count)
