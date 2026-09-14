# 간단한 가계부 프로그램
# 지출 내역을 추가하고, 목록을 보고, 총 지출을 확인할 수 있습니다.

expenses = []  # 각 항목은 {"amount": 금액, "description": 내용} 형태의 딕셔너리


def get_amount(prompt):
    while True:
        text = input(prompt)
        try:
            amount = float(text)
            if amount < 0:
                print("금액은 0 이상이어야 합니다. 다시 입력해주세요.")
                continue
            return amount
        except ValueError:
            print(f"'{text}'는 올바른 금액이 아닙니다. 숫자로 다시 입력해주세요.")


def add_expense():
    amount = get_amount("지출 금액을 입력하세요: ")
    description = input("지출 내용을 입력하세요: ")
    expenses.append({"amount": amount, "description": description})
    print("지출 내역이 추가되었습니다.")


def show_expenses():
    if not expenses:
        print("아직 등록된 지출 내역이 없습니다.")
        return

    print("\n=== 지출 내역 ===")
    for i, expense in enumerate(expenses, start=1):
        print(f"{i}. {expense['description']} - {expense['amount']:.0f}원")
    print("================\n")


def show_total():
    total = sum(expense["amount"] for expense in expenses)
    print(f"총 지출 금액: {total:.0f}원")


def show_menu():
    print("\n1. 지출 추가")
    print("2. 지출 내역 보기")
    print("3. 총 지출 확인")
    print("4. 종료")


def main():
    print("가계부 프로그램을 시작합니다.")

    while True:
        show_menu()
        choice = input("메뉴를 선택하세요: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            show_total()
        elif choice == "4":
            print("가계부 프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1~4 중에서 선택해주세요.")


if __name__ == "__main__":
    main()
