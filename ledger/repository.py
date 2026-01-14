import csv
import pandas as pd
import os
FIELDS = ["date", "type", "category", "description", "amount"]

def save_to_csv(transactions, path="data", filename="ledger.csv"):
    """
    CSV에 단일 거래 기록을 append
    줄바꿈 문제 없이 세션 초기 입력도 바로 반영됨
    """
    if transactions is None:
        return  # 입력 없으면 종료

    # 저장 폴더 생성
    if not os.path.exists(path):
        os.makedirs(path)

    #이렇게 선언 함으로써 "data/ledger.csv" 로 묶어서 사용 가능함.
    file_path = os.path.join(path, filename)

    # 파일이 없으면 헤더만 있는 CSV 생성
    if not os.path.exists(file_path):
        empty_csv = pd.DataFrame(columns=FIELDS)
        empty_csv.to_csv(file_path, index=False, encoding="utf-8-sig")

    # 단일 거래를 DataFrame으로 변환
    df = pd.DataFrame([transactions])

    # CSV에 append (줄바꿈 문제 해결)
    with open(file_path, mode="a", newline="", encoding="utf-8-sig") as f:
        df.to_csv(f, header=False, index=False)
    


def load_from_csv(path="data", filename="ledger.csv"):
    # "data/ledger.csv"
    file_path = os.path.join(path, filename)

    # CSV가 없으면 생성
    if not os.path.exists(file_path):
        os.makedirs(path, exist_ok=True)

        # 컬럼만 있는 빈 DataFrame 생성
        df = pd.DataFrame(
            columns=["date", "type", "category", "description", "amount"]
        )
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        return df   # ✅ 반드시 DataFrame 반환

    # CSV가 있으면 읽어서 반환
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    return df
    
# def is_empty_csv(path="data",filename = "ledger.csv"):
#     file_path = os.path.join(path,filename)
#     if not os.path.exists(file_path):
#         return True
#     df = pd.read_csv(file_path)
#     return df.empty

