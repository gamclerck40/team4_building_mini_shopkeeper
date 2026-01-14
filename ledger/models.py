import json
import streamlit as st
from ledger import repository as rv 

def engage_session_state_data_list():
    if 'data_list' not in st.session_state:
        st.session_state['data_list'] = []
        rv.save_to_csv(st.session_state['data_list'])
        