import streamlit as st
import pandas as pd
from ledger import models as md 

# ▶ 비즈니스 로직 (계산/처리)
# - 카테고리별 "지출" 통계 그래프
def expenditure_statistics_graph(client_data):
    spending_df = client_data[client_data["type"]=="지출"]
    if spending_df.empty:
        return pd.DataFrame(columns=["category", "amount"])
    categorized_data = (
        spending_df.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )
    return categorized_data
    # if st.session_state['data_list'] and not client_data[client_data["type"]=="지출"].empty:
    #     client_data_spending = client_data[client_data["type"]=="지출"]
    #     categorized_data = client_data_spending[["category","amount"]]
    #     return categorized_data
    
# ▶ 비즈니스 로직 (계산/처리)
# - 총 수입, 총 지출, 잔액을 계산하는 핵심 함수
def calculate_summary(df):
    """
    CSV에서 불러온 DataFrame 기준으로 수입/지출 합계와 잔액 계산
    df: pd.DataFrame
    """
    if df.empty:
        return {"income": 0, "expense": 0, "balance": 0}

    # 수입 합계
    total_income_amount = df.loc[df["type"] == "수입", "amount"].sum()

    # 지출 합계
    total_expense_amount = df.loc[df["type"] == "지출", "amount"].sum()

    # 잔액
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