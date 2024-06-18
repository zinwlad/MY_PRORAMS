import argparse
import secrets
import string


def generate_password(length=10, use_lowercase=True, use_uppercase=True, use_digits=True, use_symbols=True):
    """���������� ��������� ������.

    Args:
        length: ����� ������.
        use_lowercase: �������� �� �������� �����.
        use_uppercase: �������� �� ��������� �����.
        use_digits: �������� �� �����.
        use_symbols: �������� �� �������.

    Returns:
        ��������� ������.
    """

    if length < 10:
        raise ValueError("����� ������ ������ ���� �� ����� 10 ��������.")

    if not any([use_lowercase, use_uppercase, use_digits, use_symbols]):
        raise ValueError("���������� �������� ���� �� ���� ��� ��������.")

    alphabet = ''
    if use_lowercase:
        alphabet += string.ascii_lowercase
    if use_uppercase:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_symbols:
        alphabet += string.punctuation

    chars = ''.join(secrets.choice(alphabet) for i in range(length))
    return chars


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a random password.')
    parser.add_argument('-l', '--length', type=int, default=10, help='length of password (default: 10)')
    parser.add_argument('-L', '--lowercase', action='store_true', help='include lowercase characters')
    parser.add_argument('-U', '--uppercase', action='store_true', help='include uppercase characters')
    parser.add_argument('-d', '--digits', action='store_true', help='include digits')
    parser.add_argument('-s', '--symbols', action='store_true', help='include symbols')
    args = parser.parse_args()

    password = generate_password(args.length, use_lowercase=args.lowercase, use_uppercase=args.uppercase, use_digits=args.digits, use_symbols=args.symbols)
    print(password)