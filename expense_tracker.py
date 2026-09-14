# 간단한 가계부 프로그램
# 지출 내역을 추가하고, 목록을 보고, 총 지출을 확인할 수 있습니다.
# 지출 내역은 CSV 파일(expenses.csv)에 저장되어 프로그램을 다시 실행해도 유지됩니다.
# 각 지출 내역에는 날짜, 카테고리, 금액, 내용이 함께 저장됩니다.

import csv
import os
import re
from datetime import datetime

CSV_FILE = "expenses.csv"

CATEGORIES = ["식비", "교통", "쇼핑", "여가", "기타"]

# 각 항목은 {"date": 날짜, "category": 카테고리, "amount": 금액, "description": 내용} 형태의 딕셔너리
expenses = []


def load_expenses():
    """expenses.csv 파일을 읽어서 지출 내역 리스트를 반환합니다.
    파일이 없거나, 비어 있거나, 형식이 잘못된 줄이 있어도 프로그램이 멈추지 않습니다.
    날짜/카테고리가 없는 이전 버전 형식(금액, 내용 두 칸)의 데이터도 안전하게 불러옵니다."""
    loaded = []

    if not os.path.exists(CSV_FILE):
        return loaded

    try:
        with open(CSV_FILE, "r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 4:
                    # 새 형식: 날짜, 카테고리, 금액, 내용
                    date, category, amount_text, description = row
                elif len(row) == 2:
                    # 이전 형식: 금액, 내용 (날짜/카테고리 정보가 없으므로 기본값 사용)
                    date, category = "", "기타"
                    amount_text, description = row
                else:
                    continue  # 알 수 없는 형식의 줄은 건너뜁니다.

                try:
                    amount = float(amount_text)
                except ValueError:
                    continue  # 금액이 숫자가 아니면 건너뜁니다.

                if amount < 0:
                    continue  # 음수 금액은 건너뜁니다.

                loaded.append(
                    {
                        "date": date,
                        "category": category,
                        "amount": amount,
                        "description": description,
                    }
                )
    except OSError as error:
        print(f"저장된 지출 내역을 불러오는 중 오류가 발생했습니다: {error}")

    return loaded


def save_expense_to_file(expense):
    """새로운 지출 한 건을 CSV 파일 맨 끝에 추가로 저장합니다."""
    try:
        with open(CSV_FILE, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    expense["date"],
                    expense["category"],
                    expense["amount"],
                    expense["description"],
                ]
            )
    except OSError as error:
        print(f"지출 내역을 저장하는 중 오류가 발생했습니다: {error}")


def get_date(prompt):
    """YYYY-MM-DD 형식의 날짜만 허용합니다. 형식이 다르거나 존재하지 않는 날짜면 다시 입력받습니다."""
    while True:
        text = input(prompt)
        # 자릿수까지 정확히 맞아야 합니다. (2026-9-14 처럼 자릿수가 다르면 거부)
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
            try:
                datetime.strptime(text, "%Y-%m-%d")
                return text
            except ValueError:
                pass  # 13월, 32일처럼 실제로 없는 날짜인 경우
        print(f"'{text}'는 올바른 날짜 형식이 아닙니다. YYYY-MM-DD 형식으로 입력해주세요. (예: 2026-09-14)")


def get_category(prompt):
    """미리 정해진 카테고리 목록 중 하나를 번호로 선택받습니다."""
    while True:
        print("카테고리를 선택하세요:")
        for i, category in enumerate(CATEGORIES, start=1):
            print(f"  {i}. {category}")
        choice = input(prompt)
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print(f"'{choice}'는 올바른 카테고리 번호가 아닙니다. 1~{len(CATEGORIES)} 중에서 선택해주세요.")


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
    date = get_date("날짜를 입력하세요 (YYYY-MM-DD): ")
    category = get_category("카테고리 번호를 입력하세요: ")
    amount = get_amount("지출 금액을 입력하세요: ")
    description = input("지출 내용을 입력하세요: ")

    expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "description": description,
    }
    expenses.append(expense)
    save_expense_to_file(expense)
    print("지출 내역이 추가되었습니다.")


def show_expenses():
    if not expenses:
        print("아직 등록된 지출 내역이 없습니다.")
        return

    print("\n=== 지출 내역 ===")
    print("날짜 | 카테고리 | 금액 | 내용")
    for i, expense in enumerate(expenses, start=1):
        date = expense["date"] if expense["date"] else "(날짜없음)"
        print(
            f"{i}. {date} | {expense['category']} | {expense['amount']:.0f}원 | {expense['description']}"
        )
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
