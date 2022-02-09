file = "https://storage.googleapis.com/bevdbbucket/Bevolkerungsdaten.csv"
import pandas as pd


df = pd.read_csv(file, error_bad_lines=False, sep=";")
print(df)

#pd.read_sql_query()