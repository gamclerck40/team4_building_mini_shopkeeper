# # Version 0.6      

import streamlit as st
import pandas as pd
import os
from datetime import date
from datetime import datetime
from ledger import models as md
from ledger import services as sv
from ledger import repository as rv 
# 함수 선언부

#start, end 값을 받기 위해 함수로 정의.
from datetime import date
import pandas as pd
import os
import streamlit as st

def duration_ui():
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
# 변수 선언부 --------------------------------------------------
# dataframe함수의 columns_config에 지정할 조건 데이터를 전역변수로 저장 (자주 사용함)
columns_list = {"date":st.column_config.DateColumn(
                    label = "등록일", format="YYYY년 MM월 DD일"),
                "type":st.column_config.TextColumn(
                    label = "수입/지출"),
                "category":st.column_config.TextColumn(
                    label = "유형"),
                "description":st.column_config.TextColumn(
                    label = "상세 내용", max_chars=100),
                "amount":st.column_config.NumberColumn(
                    label = "금액",format = "%f")}

#CSV 파일 이름 전역 변수.
dir_name = "data/ledger.csv"

#F4. 현재 저장되어 있는 CSV 파일 불러오기. (read_csv)
load_data = rv.load_from_csv()

#현재 세션의 Session_state 리스트 생성 'data_list'
md.engage_session_state_data_list()

#기간 필터 검색 시작, 끝 날짜 정의 + UI 생성
start, end = duration_ui()

#읽어온 CSV(DataFrame) 데이터를 받아서 날짜 필터링 조건을 적용하여 리턴.
def set_duration(df, start_date, end_date):
    """
    날짜 범위(start_date ~ end_date)에 해당하는 데이터만 필터링해서 반환한다.
    start_date == end_date 인 경우에도 정상적으로 하루 기준 필터링을 수행한다.
    """

    # 원본 DataFrame 보호
    df = df.copy()

    # 날짜 컬럼 datetime 변환
    df["date"] = pd.to_datetime(df["date"])

    # 입력 날짜를 datetime으로 변환
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    # 날짜 범위 필터링
    filtered_df_s = df[(df["date"] >= start) & (df["date"] <= end)]

    return filtered_df_s

#F1. 거래등록 - 사이드바에서 기능 구현.
with st.sidebar:
    st.header("내역 추가")

    # 달력 뜨면 굳이 날짜를 입력하시오 라는 안내문이 필요 없을 것 같아 뺐습니다.
    transaction_date = st.date_input("날짜", datetime.today()) 
    
    # type은 변수로 쓸 수 없어 오타같지만 ttype로 썼습니다.
    ttype = st.selectbox("구분", ["지출", "수입"])
    if ttype == "지출":
        c_options = ["식비", "교통", "쇼핑", "생활", "기타"]
    else:
        c_options = ["월급", "용돈", "투자", "기타"]
        
    category = st.selectbox("카테고리", c_options)
    
    description = st.text_input("내용", placeholder="예: 점심 식사")
    amount = st.number_input("금액", step=1, format="%d")
    
    if st.button("추가",key = 1, use_container_width=True) and amount!=0 and description:
        new_data = {
            "date": transaction_date.strftime("%Y-%m-%d"), # 날짜를 str 변환
            "type": ttype,
            "category": category,
            "description": description.lower(),
            "amount": amount
        }        
        st.session_state['data_list'].append(new_data)

        #F4 중 파일 저장하기.
        rv.save_to_csv(new_data)
        st.success("저장되었습니다")
    else:
        if amount==0:
            st.warning("금액이 지출/수익이 실질적으로 존재해야 합니다.")

st.title("4조 미니 가계부 PROJECT")

# 여기부터는 검색어 받기, 표, 요약 통계, 지출 통계(그래프)를 네 개의 탭으로 묶었음.
tab_search, tab_table,tab_outline,tab_graph = st.tabs(["👛가계부 검색","📅표로 보기","🗒️요약 통계","💸지출 통계"]) 

# D1 가계부 검색 탭
with tab_search:
    st.subheader("👛가계부 내역 검색")

    #CSV 파일 내에서 찾을 "description" 에 대한 "keyword" 생성. (description == keyword 인 값을 찾는다.)
    keyword = st.text_input("내용 검색", placeholder="검색어를 입력하세요..")

    # CSV 데이터 불러오기, 없으면 빈 DataFrame
    if load_data is None:
        load_data = pd.DataFrame(columns=["date","type","category","description","amount"])
    all_data = load_data

    # CSV가 비어있는 경우
    if all_data.empty:
        st.warning("데이터가 없습니다.")
        filtered_df_s = all_data.iloc[0:0]

    else:
        # 검색어가 없는 경우
        if not keyword:
            filtered_df_s = all_data.iloc[0:0]
            st.info("검색어를 입력해주세요.")

        # 검색어가 있는 경우
        else:
            # 문자열 변환 후 필터링 -> "keyword"와 일치하는 "description"이 있는지 검사.
            is_exist = all_data["description"].astype(str).str.contains(keyword, case=False, na=False)

            # 일치하는 조건의 데이터만 저장.
            filtered_df_s = all_data[is_exist]

            # 검색어에 맞는 데이터가 없는 경우
            if filtered_df_s.empty:
                st.warning("찾는 내용이 없습니다.")

    # 검색 결과가 있을 때만 날짜 필터 적용
    if not filtered_df_s.empty:
        filtered_df_s = set_duration(filtered_df_s, start, end)

        #데이터가 존재하나, 기간 필터 적용 값이 공란일 때 (내용은 있음, 기간 필터 바깥에 존재)
        if filtered_df_s.empty:
            st.warning("내용은 있지만 날짜 설정을 다시 확인 해 주세요!")

        #데이터도 존재하고, 기간 필터 설정값 안에 존재 -> 실질적 결과 출력 구문.
        else:
            st.caption(f"검색 결과: {len(filtered_df_s)}건")
            st.header("※필터링된 정보※")
            st.dataframe(filtered_df_s, use_container_width=True, hide_index=True, column_config=columns_list)


# F2. 거래목록을 '표'로 보는 탭
with tab_table:
    
    #CSV 호출
    load_data = rv.load_from_csv()
    # Search에서 가져온 CSV데이터 검사 (비어있는지/아닌지)
    if not load_data.empty:
        if not filtered_df_s.empty:
            st.header("[data/ledger.csv] -- 폴더 내 수입/지출 Lists")
            st.subheader(f"{start} ~ {end}")
            #표 자체를 보여주는거라 원본 필터 그대로 적용해도 무관하다.
            st.dataframe(filtered_df_s, use_container_width=True, hide_index=True, column_config=columns_list)
            all_chart_btn = st.button("전체 표 보이기", key=2, use_container_width=True, help="전체 표 목록을 보여줍니다.")

        else:
            st.warning("지정된 범위내 거래 목록이 없습니다. 모든 거래목록을 보시겠습니까?")
            all_chart_btn = st.button("전체 표 보이기", key=2, use_container_width=True, help="전체 표 목록을 보여줍니다.")

    else:
        st.warning("등록된 거래가 없습니다.")
        all_chart_btn = st.button("전체 표 보이기", key=2, use_container_width=True, help="전체 표 목록을 보여줍니다.", disabled=True)

    if all_chart_btn:
        st.subheader("전체 표 목록")
        st.dataframe(load_data,use_container_width=True, hide_index=True, column_config=columns_list)
    

#F3. 총 수입, 지출, 잔액 요약 통계 탭 | Search에서 생성된 기간 필터 적용
with tab_outline:
    # 총 수입, 지출, 잔액 요약 로직을 기간필터 표 내에서 구현.{Dictionary 리턴 : income | expense | balance}
    summary = sv.calculate_summary(filtered_df_s)
    summary_all = sv.calculate_summary(load_data)
    #Streamlit UI 구현부.
    if not load_data.empty:
        st.header(f"📊 요약 통계 : {start} ~ {end}")
        col_income, col_expense, col_balance = st.columns(3)
        # 각 컬럼에 핵심 지표를 카드 형태로 출력
        col_income.metric("총 수입", f"{summary['income']:,} 원")
        col_expense.metric("총 지출", f"{summary['expense']:,} 원")
        col_balance.metric("잔액", f"{summary['balance']:,} 원")
        all_summary_btn = st.button("전체 통계 보이기", key=3, use_container_width=True, help="전체 통계를 보여줍니다.")
        if all_summary_btn:
            col_income.metric("총 수입", f"{summary_all['income']:,} 원")
            col_expense.metric("총 지출", f"{summary_all['expense']:,} 원")
            col_balance.metric("잔액", f"{summary_all['balance']:,} 원")
    else:
        st.warning("등록된 거래가 없습니다.")
        all_summary_btn = st.button("전체 통계 보이기", key=3, use_container_width=True, help="전체 통계를 보여줍니다.", disabled=True)



    
#F5. 카테고리별 지출 표, 그래프 탭
with tab_graph:
    st.header("카테고리별 [지출] 통계")   
    tab_graph_table, tab_graph_graph = st.tabs(["📅표","📊그래프"])
    if not load_data.empty:

        # 기간 필터 지정.
        filtered_df_g = set_duration(load_data, start, end)
        # "카테고리"와 "지출"로 DataFrame 생성.
        esg = sv.expenditure_statistics_graph(filtered_df_g)
        
        with tab_graph_table:
            st.subheader(f"📅지출 [표] : {start} ~ {end}")
            st.dataframe(esg, use_container_width=True, hide_index=True,column_config=columns_list)
        
        with tab_graph_graph:
            st.subheader(f"📊지출 [그래프] : {start} ~ {end}")
            st.bar_chart(esg.set_index("category")["amount"])        
    else:
        st.warning("데이터가 없습니다.")
