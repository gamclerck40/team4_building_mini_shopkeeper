import streamlit as st
import pandas as pd
from ledger import models as md 
# import code_test
from ledger import services as sv
from ledger import repository as rv 


start, end = st.date_input("기간 선택", value=(pd.to_datetime("2024-01-01"),pd.to_datetime("2026-01-14")))
st.write(start,end)
# md.engage_session_state_data_list()

# def input_information_forms():
#     date = st.date_input('날짜를 입력하시오.')
#     type = st.selectbox('구분',["수입","지출"])
# date = st.date_input('날짜를 입력하시오.')
# # st.write(list)

# type = st.selectbox('구분',["수입","지출"])
# # 사용자 입맛대로 추가하고 삭제하도록 하는 기능 >> "기타"에서 분기를 나눔
#   # -> 따로 Text_input UI 생성
# if type =="지출":
#     category = st.selectbox('카테고리',["식사","교통","통신","생활","기타"])
# else:
#     category = st.selectbox('카테고리',["월급","투자수익","대출","장학금","기타"])

# description = st.text_input("부가 설명.")
# amount = st.number_input("금액 입력", step=1, format="%d")
# deploy = st.button("입력")
# remove = st.button("데이터 전부 삭제")

# if remove:
#     md.st.session_state['data_list'] = []
#     df = pd.read_csv("ledger.csv")
#     rv.initalization_to_csv(df)
# if deploy:
#     # md.transaction.append(
#     st.session_state['data_list'].append(   
#         {"date": date,
#          "type": type,
#          "category": category,
#          "description": description,
#          "amount": amount}
#     )
#     rv.save_to_csv(st.session_state['data_list'])

# for i in range(len(st.session_state['data_list'])):
#     st.table(st.session_state['data_list'][i])

# summary = sv.calculate_summary(st.session_state['data_list'])
# df = pd.DataFrame(st.session_state['data_list'])

# sv.show_summary(summary)
# sv.expenditure_statistics_graph(df)

# if md.transaction:
#     df_i = df[df["type"]=="지출"]
#     df_j = df_i[["category","amount"]]
#     st.bar_chart(df_j.set_index("category")["amount"])
# 파일 자체를 기능별로 분담해서 작업하기. git pull origin >> git 허브 리포지토리를 Origin이라 명명
# Main 브랜치 당겨 오는것. 자기 각자 Branch를 Pull하고 싶다
# git pull origin <원하는 브랜치 이름> 

# Version 0.4      
