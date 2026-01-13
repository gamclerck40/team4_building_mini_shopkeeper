import streamlit as st
import pandas as pd
from ledger import models as md 

def expenditure_statistics_graph(client_data):
    if md.transaction and not client_data[client_data["type"]=="지출"].empty:
        df_i = client_data[client_data["type"]=="지출"]
        df_j = df_i[["category","amount"]]
        st.bar_chart(df_j.set_index("category")["amount"])