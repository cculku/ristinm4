def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b


def get_number(prompt):
    while True:
        text = input(prompt)
        try:
            return float(text)
        except ValueError:
            print(f"'{text}'는 숫자가 아닙니다. 다시 입력해주세요.")


def get_operator(prompt):
    valid_operators = ("+", "-", "*", "/")
    while True:
        operator = input(prompt)
        if operator in valid_operators:
            return operator
        print(f"'{operator}'는 지원하지 않는 연산자입니다. +, -, *, / 중 하나를 입력해주세요.")


def calculate(a, operator, b):
    if operator == "+":
        return add(a, b)
    if operator == "-":
        return subtract(a, b)
    if operator == "*":
        return multiply(a, b)
    if operator == "/":
        return divide(a, b)


if __name__ == "__main__":
    a = get_number("첫 번째 숫자를 입력하세요: ")
    operator = get_operator("연산자를 입력하세요 (+, -, *, /): ")
    b = get_number("두 번째 숫자를 입력하세요: ")

    try:
        result = calculate(a, operator, b)
        print(f"{a} {operator} {b} = {result}")
    except ValueError as e:
        print(f"오류: {e}")
