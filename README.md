Ideally present the solutions in a Jupyter Notebook.
Feel free to use popular open-source libraries tasks like financial calculations etc.
Avoid changing dataset files manually, instead do any cleanup/reshaping using code.
Use in-code comments for explaining rationale if you think there was a critical decision you made.
If time is not enough, try explaining with natural language how you would go about solving it instead.


### 1. Client account states
Provided is a Dataset(Trades) of client account trades (assume starting funds of $100,000).
Using the whole dataset calculate the final client account states in the form of [accid, sym, qty]
Optionally: also calculate the cost basis however you see fit.

### 2. Acquire daily price data for involved equities
Find on the internet daily price data for the involved stocks.

### 3. Calculate client portfolio performances
Using Dataset(Trades) and the pricing data from (2.), calculate and plot the portfolio performances for each client in the same chart.

### 4. Compare best and worst client portfolio performances
Using the same dataset/results, use the best and worst performing portfolios and produce metrics (CAGR, Sharpe ratio etc.) you would use to evaluate them.

### 5. ESG Score Index
Use the Dataset(ScoreIndex) for the weights of stocks, in order to calculate the total (additive) score of the index for each metric through time.

### 6. ESG Score for Client Portfolios
First we define Daily Productive Units as 10,000,000,000,000 when a company has a score of 100 on a metric and adjusted proportionally based on the score.

Now, combine all the needed data:
1. daily closing state of each client's portfolio
2. Dataset(SymInfo) to calculate client's share of each company
3. Dataset(SymScores) to get the score of a company used throughout a month

in order to calculate the Daily Productive Units for each metric for each client for every day.
In the format of [date, accid, metric, dpu] or [date, accid, animals, climate, social, governance, transparency], your choice.
