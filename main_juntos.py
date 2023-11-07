import pandas as pd

# File path for the previously generated Excel file
MERGED_FILE_PATH = 'data/target/merged_results.xlsx'
MERGED_FILE_END = 'data/target/results.xlsx'

# Load the merged data from the Excel file into a Pandas DataFrame
df_merged = pd.read_excel(MERGED_FILE_PATH)

# Find duplicate titles that have WOS codes and at least 50 characters
duplicate_titles = df_merged[df_merged.duplicated(subset='Article Title', keep=False) & df_merged['code'].str.startswith('wos') & (df_merged['Article Title'].str.len() >= 50)]

# Update "wos" and "scopus" columns to "SI" for duplicate titles and handle the "code_eliminado"
for title in duplicate_titles['Article Title'].unique():
    mask_scopus = (df_merged['Article Title'] == title) & df_merged['code'].str.startswith('scopus')
    mask_wos = (df_merged['Article Title'] == title) & df_merged['code'].str.startswith('wos')

    if mask_scopus.any() and mask_wos.any():
        # Find the index of the rows to keep in their original positions
        indices_to_keep = df_merged[mask_scopus].index

        # Concatenate the "code" values from "wos" records and add them to the "code_eliminado" column in the remaining "scopus" records
        code_eliminado = ', '.join(df_merged[mask_wos]['code'].dropna())
        df_merged.loc[indices_to_keep, 'code_eliminado'] = code_eliminado

        # Drop the "wos" records
        df_merged = df_merged.drop(df_merged[mask_wos].index)

# Add the new columns "wos" and "scopus" to the left with empty values
df_merged.insert(1, 'wos', '')
df_merged.insert(2, 'scopus', '')

# Mark "SI" in the "wos" column for the added "code_eliminado" records
df_merged.loc[df_merged['code_eliminado'].notnull(), 'wos'] = 'SI'

# Update the "scopus" column with "SI" for codes that start with "scopus"
df_merged.loc[df_merged['code'].str.startswith('scopus'), 'scopus'] = 'SI'

# Update the "wos" column with "SI" for codes that start with "wos"
df_merged.loc[df_merged['code'].str.startswith('wos'), 'wos'] = 'SI'

# Move the "code_eliminado" column to the first position
code_eliminado = df_merged.pop('code_eliminado')
df_merged.insert(1, 'code_eliminado', code_eliminado)

# Drop the "Unnamed: 0" column
df_merged = df_merged.drop(columns=['Unnamed: 0'])

# Reset the index of the DataFrame after all the modifications
df_merged = df_merged.reset_index(drop=True)

# Save the updated DataFrame to the Excel file
df_merged.to_excel(MERGED_FILE_END, index=False)

print('Column "code_eliminado" added. "SI" assigned in "scopus" and "wos" columns to', MERGED_FILE_END)
