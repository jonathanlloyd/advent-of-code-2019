def find_passwords(possible_passwords, rules):
    return [
        password
        for password in possible_passwords
        if all([rule(password) for rule in rules])
    ]


def contains_double(password):
    password_str = str(password)
    for i in range(1, len(password_str)):
        prev_char = password_str[i-1]
        current_char = password_str[i]
        if prev_char == current_char:
            return True
    return False


def always_increasing(password):
    password_str = str(password)
    for i in range(1, len(password_str)):
        prev_char = password_str[i-1]
        current_char = password_str[i]
        if prev_char > current_char:
            return False
    return True


if __name__ == '__main__':
    lower_bound = 109165
    upper_bound = 576723

    rules = [
        contains_double,
        always_increasing,
    ]
    possible_passwords = [i for i in range(lower_bound, upper_bound+1)]
    filtered_passwords = find_passwords(possible_passwords, rules)

    print(len(filtered_passwords))
