import json
import streamlit as st
from ledger import repository as rv 

def engage_session_state_data_list():
    if 'data_list' not in st.session_state:
        st.session_state['data_list'] = []
        rv.save_to_csv(st.session_state['data_list'])
        
def init_data(): # 초기화
    if 'data_list' not in st.session_state:
        st.session_state['filtered_data'] = []

def add_transaction(transaction): # 거래 내역 추가
    st.session_state['data_list'].append(transaction)
    

def get_all_transaction(): # 모든 데이터
    return st.session_state['data_list']


# D2 필터된 데이터 저장
def save_filtered_data(input_keyword, in_csv, filtered_keyword):
    if input_keyword: # 완성한 내용
        st.write("keword 분기!")
        result = in_csv[filtered_keyword]
        return result
    else:
        result = in_csv.iloc[0:0]
        return result