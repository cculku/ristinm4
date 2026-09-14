# 간단한 가계부 프로그램
# 지출 내역을 추가하고, 목록을 보고, 총 지출을 확인할 수 있습니다.
# 지출 내역은 CSV 파일(expenses.csv)에 저장되어 프로그램을 다시 실행해도 유지됩니다.

import csv
import os

CSV_FILE = "expenses.csv"

expenses = []  # 각 항목은 {"amount": 금액, "description": 내용} 형태의 딕셔너리


def load_expenses():
    """expenses.csv 파일을 읽어서 지출 내역 리스트를 반환합니다.
    파일이 없거나, 비어 있거나, 형식이 잘못된 줄이 있어도 프로그램이 멈추지 않습니다."""
    loaded = []

    if not os.path.exists(CSV_FILE):
        return loaded

    try:
        with open(CSV_FILE, "r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                # 한 줄에 금액, 내용 두 항목이 없으면 잘못된 줄이므로 건너뜁니다.
                if len(row) != 2:
                    continue

                try:
                    amount = float(row[0])
                except ValueError:
                    continue  # 금액이 숫자가 아니면 건너뜁니다.

                description = row[1]
                loaded.append({"amount": amount, "description": description})
    except OSError as error:
        print(f"저장된 지출 내역을 불러오는 중 오류가 발생했습니다: {error}")

    return loaded


def save_expense_to_file(expense):
    """새로운 지출 한 건을 CSV 파일 맨 끝에 추가로 저장합니다."""
    try:
        with open(CSV_FILE, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([expense["amount"], expense["description"]])
    except OSError as error:
        print(f"지출 내역을 저장하는 중 오류가 발생했습니다: {error}")


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
    expense = {"amount": amount, "description": description}
    expenses.append(expense)
    save_expense_to_file(expense)
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

    expenses.extend(load_expenses())
    if expenses:
        print(f"저장된 지출 내역 {len(expenses)}건을 불러왔습니다.")

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
