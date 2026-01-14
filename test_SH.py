# import streamlit as st
# import pandas as pd
# from ledger import models as md 
# import code_test

# if 'data_list' not in st.session_state:
#     st.session_state['data_list'] = []

# date = st.date_input('날짜를 입력하시오.')
# st.write(list)

# type = st.selectbox('구분',["수입","지출"])
# # 사용자 입맛대로 추가하고 삭제하도록 하는 기능 >> "기타"에서 분기를 나눔
#   # -> 따로 Text_input UI 생성
# if type =="수입":
#     category = st.selectbox('카테고리',["식사","교통","통신","생활","기타"])
# else:
#     category = st.selectbox('카테고리',["월급","투자","대출","장학금"])

# description = st.text_input("부가 설명.")
# amount = st.number_input("금액 입력", step=1, format="%d")
# deploy = st.button("입력")

# # if deploy:
# #     md.transaction.append(
# #         {"date": date,
# #          "type": type,
# #          "category": category,
# #          "description": description,
# #          "amount": amount}
# #     )

# code_test.transaction_data(deploy, )
# for i in range(len(md.transaction)):
#     st.table(md.transaction[i])
# # 파일 자체를 기능별로 분담해서 작업하기. git pull origin >> git 허브 리포지토리를 Origin이라 명명
# # Main 브랜치 당겨 오는것. 자기 각자 Branch를 Pull하고 싶다
# # git pull origin <원하는 브랜치 이름> 

# # Version 0.4      

import streamlit as st
import pandas as pd
import os
from datetime import date
from datetime import datetime
from ledger import models as md
from ledger import services as sv
from ledger import repository as rv 

# new_data = md.transaction
# F4: load data

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

#CSV 파일 이름 변수.
dir_name = "data/ledger.csv"

#현재 저장되어 있는 CSV 파일 불러오기. (read_csv)
load_data = rv.load_from_csv()
md.engage_session_state_data_list()

def duration_ui():
    if os.path.exists(dir_name) and os.path.getsize(dir_name) > 0:
        gf = load_data
        date_value = st.date_input(
            "기간 선택",
            value=(pd.to_datetime(gf["date"]).min().date(),
                   pd.to_datetime(gf["date"]).max().date())
        )
    else:
        date_value = st.date_input(
            "기간 선택",
            value=(date(2024, 1, 1), date(2026, 12, 31))
        )

    # 🔒 여기서 반드시 정규화
    if isinstance(date_value, tuple):
        if len(date_value) == 2:
            return date_value
        else:  # (date,) 인 경우
            st.warning("시작날짜 혹은 끝날자 중 선택하지 않았어요!")
            return date_value[0], date_value[0]
    else:
        return date_value, date_value

# def set_duration(load_data,start_date, end_date):
#     if start_date!=end_date:
#         load_data["date"] = pd.to_datetime(load_data["date"])
#         starting = pd.to_datetime(start_date)
#         ending = pd.to_datetime(end_date)
#         filtered_df = load_data[(load_data["date"] >= starting) & (load_data["date"] <= ending)] 
#         return filtered_df
#     else:
#         st.warning("시작날과 끝날짜가 같습니다")
#         return filtered_df
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
    filtered_df = df[(df["date"] >= start) & (df["date"] <= end)]

    return filtered_df

# 사이드바 기능 구현.
with st.sidebar:
    st.header("내역 추가")
    transaction_date = st.date_input("날짜", datetime.today()) # 달력 뜨면 굳이 날짜를 입력하시오 라는 안내문이 필요 없을 것 같아 뺐습니다.
    
    ttype = st.selectbox("구분", ["지출", "수입"]) # type은 변수로 쓸 수 없어 오타같지만 ttype로 썼습니다.
    if ttype == "지출":
        c_options = ["식비", "교통", "쇼핑", "생활", "기타"]
    else:
        c_options = ["월급", "용돈", "투자", "기타"]
        
    category = st.selectbox("카테고리", c_options)
    
    description = st.text_input("내용", placeholder="예: 점심 식사")
    amount = st.number_input("금액", step=1, format="%d")
    
    if st.button("추가", use_container_width=True) and amount!=0 and description:
        new_data = {
            "date": transaction_date.strftime("%Y-%m-%d"), # 날짜를 str 변환
            "type": ttype,
            "category": category,
            "description": description,
            "amount": amount
        }        
        st.session_state['data_list'].append(new_data)
        rv.save_to_csv(new_data)
        st.success("저장되었습니다")
    else:
        if amount==0:
            st.warning("금액이 지출/수익이 실질적으로 존재해야 합니다.")

tab_search, tab_table,tab_outline,tab_graph = st.tabs(["👛가계부 검색","📅표로 보기","🗒️요약 통계","💸지출 통계"])
    # 여기부터는 검색어 받기, 데이터 거르기(D2)

# 가계부 검색 탭
with tab_search:
    st.subheader("👛가계부 내역 검색")
    keyword = st.text_input("내용 검색", placeholder="검색어를 입력하세요..")

    # CSV 데이터 불러오기, 없으면 빈 DataFrame
    if load_data is None:
        load_data = pd.DataFrame(columns=["date","type","category","description","amount"])
    all_data = load_data

    # CSV가 비어있는 경우
    if all_data.empty:
        st.info("데이터가 없습니다.")
        filtered_result = all_data.iloc[0:0]

    else:
        # 기간 선택 UI
        start, end = duration_ui()

        # 검색어가 없는 경우
        if not keyword:
            filtered_result = all_data.iloc[0:0]
            st.info("검색어를 입력해주세요.")

        # 검색어가 있는 경우
        else:
            # 문자열 변환 후 필터링
            is_exist = all_data["description"].astype(str).str.contains(keyword, case=False, na=False)
            filtered_result = all_data[is_exist]

            # 검색어에 맞는 데이터가 없는 경우
            if filtered_result.empty:
                st.warning("찾는 내용이 없습니다.")

    # 검색 결과가 있을 때만 날짜 필터 적용
    if not filtered_result.empty:
        filtered_df = set_duration(filtered_result, start, end)

        if filtered_df.empty:
            st.warning("내용은 있지만 날짜 설정을 다시 확인 해 주세요!")
        else:
            st.caption(f"검색 결과: {len(filtered_df)}건")
            st.header("※필터링된 정보※")
            st.dataframe(filtered_df, use_container_width=True, hide_index=True, column_config=columns_list)


# '표'로 보는 탭
with tab_table:
    # df = pd.DataFrame(all_data)
    # st.subheader("전체 표 DATA")
    # st.dataframe(df,use_container_width=True, hide_index=True, column_config=columns_list)
    load_data = rv.load_from_csv()
    st.subheader("[ledger.csv] -- 폴더 내 수입/지출 Lists")
    st.dataframe(load_data,use_container_width=True, hide_index=True, column_config=columns_list)

#총 수입, 지출, 잔액 요약 통계 탭
with tab_outline:
    summary = sv.calculate_summary(load_data)
    sv.show_summary(summary)

#카테고리별 지출 표, 그래프 탭
with tab_graph:
    # for i in range(len(st.session_state['data_list'])):
    #     st.table(st.session_state['data_list'][i])
    st.subheader("카테고리별 [지출] 통계")   
    tab_graph_table, tab_graph_graph = st.tabs(["📅표","📊그래프"])
    if not load_data.empty:
        esg = sv.expenditure_statistics_graph(load_data)
        with tab_graph_table:
            st.subheader("📅지출 [표]")
            st.dataframe(esg, use_container_width=True, hide_index=True,column_config=columns_list)
        
        with tab_graph_graph:
            st.subheader("📊지출 [그래프]")
            st.bar_chart(esg.set_index("category")["amount"])        
    else:
        st.warning("데이터가 없습니다.")

# if keyword:
#     filtered_result = [] # 아직 여기는 진행 안함
    
    
    
# F2

# if len(filtered_result) > 0:
#     df = pd.DataFrame(filtered_result)
    
#     if keyword:
#         st.caption(f"검색 결과: {len(filtered_result)}건")