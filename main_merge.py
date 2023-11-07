import pandas as pd

# File paths for the previously generated Excel files
SCOPUS_FILE_PATH = 'data/target/scopus_autor_2023.xlsx'
WOS_FILE_PATH = 'data/target/wos_autor_2023.xlsx'
MERGED_FILE_PATH = 'data/target/merged_results.xlsx'

# Load the data from the two Excel files into Pandas DataFrames
df_scopus = pd.read_excel(SCOPUS_FILE_PATH)
df_wos = pd.read_excel(WOS_FILE_PATH)

# Find the common column names between the two DataFrames
common_columns = list(set(df_scopus.columns) & set(df_wos.columns))

# Convert the data types of the common columns to strings in both DataFrames
for col in common_columns:
    df_scopus[col] = df_scopus[col].astype(str)
    df_wos[col] = df_wos[col].astype(str)

# Merge DataFrames using the common column names
df_merged = pd.merge(df_scopus, df_wos, on=common_columns, how='outer')

# Identify non-matching columns from each DataFrame
scopus_non_matching_cols = [col for col in df_scopus.columns if col not in common_columns]
wos_non_matching_cols = [col for col in df_wos.columns if col not in common_columns]

# Append non-matching columns from df_scopus to df_merged
df_merged[scopus_non_matching_cols] = df_scopus[scopus_non_matching_cols]

# Append non-matching columns from df_wos to df_merged
df_merged[wos_non_matching_cols] = df_wos[wos_non_matching_cols]

# Save the merged DataFrame into a new Excel file
df_merged.to_excel(MERGED_FILE_PATH, index=False)

print('Merged results saved to', MERGED_FILE_PATH)
