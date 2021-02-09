import pandas as pd
from tabulate import tabulate

from src.filtering import filter_by_query

df = pd.read_csv("test_data/simple_test_data.csv")

print("Original data:")
print(tabulate(df, headers=df.columns))
print()

query = "tampere"
df_filtered = filter_by_query(df, query)
print("Query: ", query)
print(tabulate(df_filtered, headers=df_filtered.columns))
print()
assert df_filtered.index.to_list() == [3, 4, 6, 7]

query = "tam.*re"
df_filtered = filter_by_query(df, query)
print("Query: ", query)
print(tabulate(df_filtered, headers=df_filtered.columns))
print()
assert df_filtered.index.to_list() == [3, 4, 6, 7]

query = "[Lives, Born] tampere || [Nationality] finland"
df_filtered = filter_by_query(df, query)
print("Query: ", query)
print(tabulate(df_filtered, headers=df_filtered.columns))
print()
assert df_filtered.index.to_list() == [2, 3, 4, 6, 7]

query = "[Lives] [Born] tampere || [Nationality] finland"
df_filtered = filter_by_query(df, query)
print("Query: ", query)
print(tabulate(df_filtered, headers=df_filtered.columns))
print()
assert df_filtered.index.to_list() == [2, 3, 4, 6, 7]

query = "[Lives, Born] tampere && [Nationality] finland"
df_filtered = filter_by_query(df, query)
print("Query: ", query)
print(tabulate(df_filtered, headers=df_filtered.columns))
print()
assert df_filtered.index.to_list() == [3, 4, 6]

query = "[Lives] tampere && [Nationality] finland"
df_filtered = filter_by_query(df, query)
print("Query: ", query)
print(tabulate(df_filtered, headers=df_filtered.columns))
print()
assert df_filtered.index.to_list() == [4]

query = "[Lives] tampere|helsinki && [Nationality] finland"
df_filtered = filter_by_query(df, query)
print("Query: ", query)
print(tabulate(df_filtered, headers=df_filtered.columns))
print()
assert df_filtered.index.to_list() == [2, 3, 4]
