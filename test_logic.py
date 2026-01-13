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

# F4: load data
# if it's the first time the program runs:
#     if a csv file exists:
# load the csv file and store it in 'data_list'

#     else:
#         create an empty list[]
#     save 'data_list' in st.session_state

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
    
    if st.button("추가", use_container_width=True):
        new_data = {
            "date": transaction_date.strftime("%Y-%m-%d"), # 날짜를 str 변환
            "type": ttype,
            "category": category,
            "description": description,
            "amount": amount
        }
        
        st.session_state['data_list'].append(new_data)
        st.success("저장되었습니다")
        
        

# 여기부터는 검색어 받기, 데이터 거르기(D2)
st.title("가계부 내역 검색")

keyword = st.text_input("내용 검색", placeholder="검색어를 입력하세요")


all_data = st.session_state["data_list"]

if keyword:
    filtered_result = [] # 아직 여기는 진행 안함
    
    
    
# F2

if len(filtered_result) > 0:
    df = pd.DataFrame(filtered_result)
    
    if keyword:
        st.caption(f"검색 결과: {len(filtered_result)}건")