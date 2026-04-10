# import pandas as pd
# df = pd.read_csv(r'C:\Users\91774\OneDrive\customer_shopping_behavior.csv')
# df.head()
# df.info()
# df.describe()
# df.isnull().sum()
# df["Review Rating"] = df.groupby('Category')
# ["Review Rating"].transform(lambda x: x.fillna(x.median()))
# df.columns = df.columns.str.lower()
# df.columns =  df.columns.str.replace(' ','_')
# df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount_usd'})
# df = df.rename(columns={'frequency_of_purchases':'freq_of_purchases'})
# #create a column age_group
# labels = ['young Adult','Adult','Middle-aged','Senior']
# df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)
# df[['age','age_group']].head(100)
# df['freq_of_purchases'].unique()
# # create column purchase_frequency_days
# frequency_mapping ={'Fortnightly': 14,
#  'Weekly':7,
#  'Annually':365,
#  'Quarterly':90,
#  'Bi-Weekly':14,
#  'Monthly':30,
#  'Every 3 Months':90
#                    }
# df['purchase_frequency_days'] = df['freq_of_purchases'].map(frequency_mapping)
# df[['discount_applied', 'promo_code_used']].head(10)
# (df['discount_applied'] == df['promo_code_used']).all()
# df = df.drop('promo_code_used',axis=1)
# df.columns

# from sqlalchemy import create_engine

# engine = create_engine(
#     "mysql+mysqlconnector://root:tanishkaaa%4016@localhost:3306/consumer"
# )

# # Test connection
# try:
#     with engine.connect() as conn:
#         print("Connected successfully!")
# except Exception as e:
#     print("Error:", e)

# # ✅ Ensure DataFrame is valid before inserting
# df = df.reset_index(drop=True)

# # Optional: fill missing values (avoids SQL issues)
# df = df.fillna("")

# # Upload to MySQL
# df.to_sql(
#     name="consumer",
#     con=engine,
#     if_exists="replace",
#     index=False,
#     chunksize=500,
#     method="multi"
# )

# print("✅ Data uploaded successfully!")
import pandas as pd
from sqlalchemy import create_engine

# ── Load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(r'C:\Users\91774\OneDrive\customer_shopping_behavior.csv')

print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())

# ── Clean columns ─────────────────────────────────────────────────────────────
df["Review Rating"] = df.groupby('Category')["Review Rating"].transform(
    lambda x: x.fillna(x.median())
)

df.columns = df.columns.str.lower().str.replace(' ', '_')
df = df.rename(columns={
    'purchase_amount_(usd)': 'purchase_amount_usd',
    'frequency_of_purchases': 'freq_of_purchases'
})

# ── Age group ─────────────────────────────────────────────────────────────────
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels, duplicates='drop')

print(df[['age', 'age_group']].head(100))

# ── Purchase frequency (days) ─────────────────────────────────────────────────
print(df['freq_of_purchases'].unique())

frequency_mapping = {
    'Fortnightly':    14,
    'Weekly':          7,
    'Annually':      365,
    'Quarterly':      90,
    'Bi-Weekly':      14,
    'Monthly':        30,
    'Every 3 Months': 90
}
df['purchase_frequency_days'] = df['freq_of_purchases'].map(frequency_mapping)

# ── Drop redundant column ─────────────────────────────────────────────────────
print(df[['discount_applied', 'promo_code_used']].head(10))
print("Columns identical:", (df['discount_applied'] == df['promo_code_used']).all())

df = df.drop('promo_code_used', axis=1)
print(df.columns)

# ── Upload to MySQL ───────────────────────────────────────────────────────────
engine = create_engine(
    "mysql+mysqlconnector://root:tanishkaaa%4016@localhost:3306/consumer"
)

try:
    with engine.connect() as conn:
        print("Connected successfully!")
except Exception as e:
    print("Error:", e)

df = df.reset_index(drop=True)

# Fill missing values safely per dtype (avoids corrupting numeric columns)
for col in df.columns:
    if hasattr(df[col], 'cat'):          # Categorical (e.g. age_group)
        df[col] = df[col].astype(str).fillna("")
    elif df[col].dtype == object:        # String columns
        df[col] = df[col].fillna("")
    else:                                # Numeric columns
        df[col] = df[col].fillna(0)

df.to_sql(
    name="consumer",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=500,
    method="multi"
)

print("Data uploaded successfully!")