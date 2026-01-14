import streamlit as st
import pandas as pd
import os
from datetime import date
from datetime import datetime
from ledger import repository as rv

def duration_ui():
    dir_name = "data/ledger.csv"
    load_data = rv.load_from_csv()
    DEFAULT_START = date(2024, 1, 1)
    DEFAULT_END   = date(2026, 12, 31)

    # 1️⃣ 기본값 준비
    start_date = DEFAULT_START
    end_date = DEFAULT_END

    # 2️⃣ CSV가 "존재"하고 "크기"가 있을 때
    if os.path.exists(dir_name) and os.path.getsize(dir_name) > 0:
        gf = load_data

        # 날짜 컬럼 안전 변환
        gf["date"] = pd.to_datetime(gf["date"], errors="coerce")

        # 🚨 실제 날짜 데이터가 하나라도 있을 때만 min/max 사용
        if not gf.empty and gf["date"].notna().any():
            start_date = gf["date"].min().date()
            end_date   = gf["date"].max().date()

    # 3️⃣ date_input (여기엔 절대 NaT / None 안 들어감)
    date_value = st.date_input(
        "기간 선택",
        value=(start_date, end_date)
    )

    # ==================================================
    # 4️⃣ 반드시 정규화 (tuple / 단일값 대응)
    # ==================================================

    # (date, date) 형태
    if isinstance(date_value, tuple):

        # 정상적인 기간 선택
        if len(date_value) == 2:
            return date_value

        # (date,) 형태 (이론상 거의 없지만 방어)
        else:
            st.warning("시작 날짜와 종료 날짜를 모두 선택해 주세요.")
            return date_value[0], date_value[0]

    # 단일 date 선택 시
    else:
        return date_value, date_value