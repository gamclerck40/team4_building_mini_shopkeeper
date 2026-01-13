import csv

FIELDS = ["date", "type", "category", "amount", "description"]

def save_to_csv(transactions, filename="ledger.csv"):
    if not transactions:
        return
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(transactions)


def load_from_csv(filename="ledger.csv"):
    transactions = []

    try:
        with open(filename, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append({
                    "date": int(row["date"]),
                    "type": row["type"],
                    "category": row["category"],
                    "amount": int(row["amount"]),
                    "description": row["description"]
                })
    except FileNotFoundError:
        pass

    return transactions
