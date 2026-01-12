from ledger import models as md 

def transaction_data(btn, *args):
    if btn:
        date, type, category, description, amount = args
        md.transaction.append(
            {"date": date,
             "type": type,
             "category": category,
             "description": description,
             "amount": amount}
    )
