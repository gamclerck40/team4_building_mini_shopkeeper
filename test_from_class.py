import streamlit as st
import pandas as pd
from ledger import models

# # -----------------------------
# # 0) 페이지 설정 (선택이지만 추천)
# # -----------------------------
# st.set_page_config(page_title="감정 기록/통계", page_icon="📊", layout="wide")

# # -----------------------------
# # 1) 세션 상태 초기화
# # -----------------------------
# if "moods" not in st.session_state:
#     st.session_state["moods"] = []  # 예: ["😀 행복", "😐 보통", ...]

# st.title("📊 감정 기록 & 통계")

# # 탭으로 화면을 2개로 분리 (기록 / 통계)
# tab_record, tab_stats = st.tabs(["📝 감정 기록", "📈 감정 통계"])

# # =========================================================
# # 탭 1) 감정 기록
# # =========================================================
# with tab_record:
#     st.header("📝 감정 기록하기")

#     mood = st.selectbox(
#         "오늘의 감정",
#         ["😀 행복", "😊 좋음", "😐 보통", "😞 슬픔", "😡 화남"],
#         key="mood_select"  # 위젯 key (중복 방지)
#     )

#     # 버튼은 한 번만 만들고 변수로 받기
#     add_clicked = st.button("감정 추가", key="add_mood_btn")
#     if add_clicked:
#         st.session_state["moods"].append(mood)
#         st.success("✅ 감정이 저장되었습니다!")

#     st.subheader("📋 저장된 감정 목록")

#     if len(st.session_state["moods"]) == 0:
#         st.info("아직 저장된 감정이 없습니다. 위에서 감정을 추가해보세요.")
#     else:
#         for i, m in enumerate(st.session_state["moods"], start=1):
#             st.write(f"{i}. {m}")

#     # 전체 삭제
#     delete_clicked = st.button("⚠️ 전체 삭제", key="delete_all_btn")
#     if delete_clicked:
#         st.session_state["moods"] = []
#         st.warning("모든 감정 기록을 삭제했습니다.")

# # =========================================================
# # 탭 2) 감정 통계
# # =========================================================
# with tab_stats:
#     st.header("📈 감정 통계 보기")

#     # 데이터가 없으면 통계 계산 불가
#     if len(st.session_state["moods"]) == 0:
#         st.info("먼저 '📝 감정 기록' 탭에서 감정을 기록해주세요.")
#         st.stop()

#     # 리스트 -> DataFrame
#     df = pd.DataFrame(st.session_state["moods"], columns=["감정"])

#     # 감정별 횟수 집계
#     mood_count = (
#         df.groupby("감정")
#           .size()
#           .reset_index(name="횟수")
#     )

#     st.subheader("📋 감정별 통계 (표)")
#     st.dataframe(mood_count, width="stretch")  # use_container_width 경고 제거

#     st.subheader("📊 감정 분포 그래프")
#     st.bar_chart(mood_count.set_index("감정"))

list = []
transaction = []
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
amount = int(st.number_input("금액 입력", min_value=0, value=0, step=10))
deploy = st.button("입력")

if deploy:
    trans = models.Transaction([date.year, date.month, date.day],type,description,category,amount)
    st.write(trans.amount)

    
