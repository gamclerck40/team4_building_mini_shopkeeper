import streamlit as st
import pandas as pd
from ledger import models as md 
import code_test

if 'data_list' not in st.session_state:
    st.session_state['data_list'] = []

date = st.date_input('날짜를 입력하시오.')
st.write(list)

type = st.selectbox('구분',["수입","지출"])
# 사용자 입맛대로 추가하고 삭제하도록 하는 기능 >> "기타"에서 분기를 나눔
  # -> 따로 Text_input UI 생성
if type =="수입":
    category = st.selectbox('카테고리',["식사","교통","통신","생활","기타"])
else:
    category = st.selectbox('카테고리',["월급","투자","대출","장학금"])

description = st.text_input("부가 설명.")
amount = st.number_input("금액 입력", step=1, format="%d")
deploy = st.button("입력")

# if deploy:
#     md.transaction.append(
#         {"date": date,
#          "type": type,
#          "category": category,
#          "description": description,
#          "amount": amount}
#     )

code_test.transaction_data(deploy, )
for i in range(len(md.transaction)):
    st.table(md.transaction[i])
# 파일 자체를 기능별로 분담해서 작업하기. git pull origin >> git 허브 리포지토리를 Origin이라 명명
# Main 브랜치 당겨 오는것. 자기 각자 Branch를 Pull하고 싶다
# git pull origin <원하는 브랜치 이름> 

# Version 0.4      
