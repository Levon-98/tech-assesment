import pandas as pd

# Step 1: Load the 'ScoreIndex' dataset
score_index_df = pd.read_csv('data/dataset-scoreindex.csv')
score_index_df['year_month'] = pd.to_datetime(score_index_df['year_month'])
score_index_df.set_index('year_month', inplace=True)

# Step 2: Calculate the cumulative index score for each metric
score_index_df_cumulative = score_index_df.cumsum()

# Step 3: Get the total (additive) score of the index for each metric through time
index_scores = score_index_df_cumulative.iloc[-1]

print(index_scores)
