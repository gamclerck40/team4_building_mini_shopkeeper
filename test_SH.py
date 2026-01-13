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
from datetime import datetime
from ledger import models as md
from ledger import services as sv
from ledger import repository as rv 

# new_data = md.transaction
# F4: load data
# md.engage_session_state_data_list()
if 'data_list' not in st.session_state:
        data_list = st.session_state['data_list'] = []
        rv.save_to_csv(st.session_state['data_list'])

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
        rv.save_to_csv(st.session_state['data_list'])
        st.success("저장되었습니다")
    else:
        if amount==0:
            st.warning("금액이 지출/수익이 실질적으로 존재해야 합니다.")


gf = pd.read_csv("ledger.csv")
start, end = st.date_input("기간 선택", value=(gf["date"].min(),gf["date"].max()))

tab_search, tab_table,tab_outline,tab_graph = st.tabs(["가계부 검색","표로 보기","요약 통계","그래프로 보기"])
    # 여기부터는 검색어 받기, 데이터 거르기(D2)
with tab_search:
    st.title("가계부 내역 검색")

    keyword = st.text_input("내용 검색", placeholder="검색어를 입력하세요")


    all_data = st.session_state['data_list']

    if keyword: # 완성한 내용
        filtered_result = [
            d for d in all_data
            if keyword.lower() in d['description'].lower()
        ]
    else:
        filtered_result = all_data

    # st.session_state['filtered_data'] = filtered_result
    md.save_filtered_data(filtered_result)
 
    # F2 목록 출력

    if len(filtered_result) > 0 and keyword:
        df = pd.DataFrame(filtered_result)

        if keyword:
            st.caption(f"검색 결과: {len(filtered_result)}건")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        if keyword:
            st.info("검색 결과가 없습니다.")
        else:
            st.info("데이터가 없습니다.")



with tab_table:
    df = pd.DataFrame(all_data)
    st.table(df)

with tab_outline:
    summary = sv.calculate_summary(st.session_state['data_list'])
    sv.show_summary(summary)


with tab_graph:
    # for i in range(len(st.session_state['data_list'])):
    #     st.table(st.session_state['data_list'][i])
    st.title("가계부 내역 검색")
    st.header("지출 통계 Graph")    

    if st.session_state['data_list']:
        df = pd.DataFrame(st.session_state['data_list'])
        sv.expenditure_statistics_graph(df)
    else:
        st.warning("데이터가 없습니다.")

# if keyword:
#     filtered_result = [] # 아직 여기는 진행 안함
    
    
    
# F2

# if len(filtered_result) > 0:
#     df = pd.DataFrame(filtered_result)
    
#     if keyword:
#         st.caption(f"검색 결과: {len(filtered_result)}건")