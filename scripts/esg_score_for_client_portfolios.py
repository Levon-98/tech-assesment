import pandas as pd

# Step 1: Load the required datasets
trades_df = pd.read_csv('data/dataset-trades.csv')
sym_info_df = pd.read_csv('data/dataset-syminfo.csv')
sym_scores_df = pd.read_csv('data/dataset-symscores.csv')

# Step 2: Calculate the daily closing state of each client's portfolio
portfolio_df = trades_df.groupby(['accid', 'sym'])['qty'].sum().reset_index()
portfolio_df.rename(columns={'qty': 'portfolio_qty'}, inplace=True)

# Step 3: Merge Trades and SymInfo datasets to calculate the client's share of each company
portfolio_df = pd.merge(portfolio_df, sym_info_df, on='sym')
portfolio_df['client_share'] = portfolio_df['portfolio_qty'] / portfolio_df['outstanding_shares']

# Step 4: Merge SymInfo and SymScores datasets to get the score of a company used throughout a month
company_score_df = pd.merge(sym_info_df, sym_scores_df, on='sym')

# Step 5: Calculate the Daily Productive Units (DPU) for each metric for each client for every day
dpu_df = pd.DataFrame()
for metric in ['animals', 'climate', 'social', 'governance', 'transparency']:
    metric_dpu = company_score_df[metric] * 10_000_000_000_000
    metric_dpu = pd.concat([company_score_df[['sym']], metric_dpu], axis=1)
    dpu_df = pd.concat([dpu_df, metric_dpu.rename(columns={metric: 'dpu'})], ignore_index=True)

dpu_df['date'] = pd.to_datetime(sym_scores_df['year_month'])
dpu_df = pd.merge(dpu_df, portfolio_df, on='sym')
dpu_df['dpu'] *= dpu_df['client_share']
dpu_df = dpu_df[['date', 'accid', 'sym', 'dpu']]

# Optional: If you prefer the format with metrics as separate columns
dpu_pivot = dpu_df.pivot_table(index=['date', 'accid'], columns='sym', values='dpu').reset_index()

print(dpu_df)
print(dpu_pivot)