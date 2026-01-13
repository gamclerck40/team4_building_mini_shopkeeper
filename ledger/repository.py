import csv
FIELDS = ["date", "type", "category", "amount", "description"]

def save_to_csv(transactions, filename="ledger.csv"):
    if not transactions:
        return

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(transactions)

def initalization_to_csv(df):
    df.iloc[0:0].to_csv("ledger.csv", index=False)

