import pandas as pd
df71 = pd.read_csv('office_address.csv', encoding="UTF-8")
df72=df71.query('public_office_classification==1')
df72.to_csv('office_preprocess.csv')
print(df72)
