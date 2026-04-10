import pandas as pd
df = pd.read_csv(r'C:\Users\91774\OneDrive\customer_shopping_behavior.csv')
df.head()
df.info()
df.describe()
df.isnull().sum()
df["Review Rating"] = df.groupby('Category')
["Review Rating"].transform(lambda x: x.fillna(x.median()))
df.columns = df.columns.str.lower()
df.columns =  df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount_usd'})
df = df.rename(columns={'frequency_of_purchases':'freq_of_purchases'})
#create a column age_group
labels = ['young Adult','Adult','Middle-aged','Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)
df[['age','age_group']].head(100)
df['freq_of_purchases'].unique()

frequency_mapping ={'Fortnightly': 14,
 'Weekly':7,
 'Annually':365,
 'Quarterly':90,
 'Bi-Weekly':14,
 'Monthly':30,
 'Every 3 Months':90
                   }
df['purchase_frequency_days'] = df['freq_of_purchases'].map(frequency_mapping)