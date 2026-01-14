#디렉터리에 CSV파일이 있는지 없는지 검사.
if os.path.exists(csv_name|"ledger.csv"):
    gf = pd.DataFrame(st.session_state['data_list'])
    start, end = st.date_input("기간 선택", value=(gf["date"].min(),gf["date"].max()))
else:
    start, end = st.date_input("기간 선택", value=(pd.to_datetime("2024-01-01"),pd.to_datetime("2026-12-31")))

gf = pd.read_csv("ledger.csv")
start, end = st.date_input("기간 선택", value=(gf["date"].min(),gf["date"].max()))

#기간 설정 함수
def set_duration(start_date=start, end_date =end):
    
    df["date"] = pd.to_datetime(df["date"])
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)
    filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)] 
    return filtered_df 

#출력 구현부
if len(filtered_result) > 0 and keyword:
        df = pd.DataFrame(filtered_result)
        filtered_df = set_duration(df, start_date=start, end_date =end)
        if keyword:
            st.caption(f"검색 결과: {len(filtered_df)}건")
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
else:
    if keyword:
        st.info("검색 결과가 없습니다.")
    else:
        st.info("데이터가 없습니다.")