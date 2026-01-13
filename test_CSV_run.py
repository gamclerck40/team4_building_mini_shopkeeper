from test_CSV import save_to_csv, load_from_csv
from ledger import models as md
import streamlit as st
transactions = load_from_csv()  # 프로그램 시작 시 자동 복구

while True:
    print("\n1. 거래 추가")
    print("2. 저장")
    print("0. 종료")

    choice = input("선택: ")

    if choice == "1":
        t = {
            "date": int(input("날짜(YYYYMMDD): ")),
            "type": input("자산/부채: "),
            "category": input("분류: "),
            "amount": int(input("금액: ")),
            "description": input("내용: ")
        }
        transactions.append(t)

    elif choice == "2":
        save_to_csv(md.st.session_state['input_data'])
        print("저장 완료")

    elif choice == "0":
        save_to_csv(md.st.session_state['input_data'])   # 종료 시 자동 저장 ⭐
        break
