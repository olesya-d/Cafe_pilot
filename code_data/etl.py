
import pandas as pd
import os
import hashlib


script_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(script_dir, 'cafe-raw-data.txt')
out_path = os.path.join(script_dir, 'cafe-clean-data.csv')

df = pd.read_csv(
        file_path,  
        sep = ' ', 
        header = None, 
        names =["customer",
        "product",
        "price",
        "branch",
        "payment_type",
        "card_number",
        "date"]
)

# Anonymise customer name → customer_id
df["customer"] = df["customer"].apply(lambda x: "CUST_" + hashlib.sha256(x.lower().encode()).hexdigest()[:8])

# Remove card details ASAP
df = df.drop(columns=["card_number"])

# Clean price
df["price"] = df["price"].str.replace("£", "", regex=False).astype(float)

# Convert date
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")

# Calculate sales and profit
df["sales"] = df["price"] # just in case in the future column quantity will be added then sales = price*quantity
df["profit"] = df["price"] * 0.50

# -----------------------------
# 3) Save clean data
# -----------------------------
df.to_csv(out_path, index=False)
print ("ETL complete. Prepared data saved at 'cafe-clean-data.csv'")

