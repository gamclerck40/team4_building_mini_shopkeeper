import streamlit as st
import pandas as pd
from ledger import models as md 

def expenditure_statistics_graph(client_data):
    if st.session_state['data_list'] and not client_data[client_data["type"]=="지출"].empty:
        client_data_spending = client_data[client_data["type"]=="지출"]
        categorized_data = client_data_spending[["category","amount"]]
        st.bar_chart(categorized_data.set_index("category")["amount"])

# ▶ 비즈니스 로직 (계산/처리)
# - 총 수입, 총 지출, 잔액을 계산하는 핵심 함수
def calculate_summary(transactions):
    total_income_amount = 0   # 전체 수입 합계
    total_expense_amount = 0  # 전체 지출 합계

    for transaction in transactions:
        # 거래 유형에 따라 수입/지출을 각각 누적
        if transaction["type"] == "수입":
            total_income_amount += transaction["amount"]
        elif transaction["type"] == "지출":
            total_expense_amount += transaction["amount"]

    # 잔액 = 총 수입 - 총 지출
    remaining_balance = total_income_amount - total_expense_amount

    return {    
        "income": total_income_amount,
        "expense": total_expense_amount,
        "balance": remaining_balance
    }


# ▶ 화면 출력 로직 (UI 전용)
# - 계산된 요약 데이터를 Streamlit 화면에 시각적으로 표시
def show_summary(summary_data):
    st.subheader("📊 요약 통계")

    col_income, col_expense, col_balance = st.columns(3)

    # 각 컬럼에 핵심 지표를 카드 형태로 출력
    col_income.metric("총 수입", f"{summary_data['income']:,} 원")
    col_expense.metric("총 지출", f"{summary_data['expense']:,} 원")
    col_balance.metric("잔액", f"{summary_data['balance']:,} 원")