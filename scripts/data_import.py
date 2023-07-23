import pandas as pd
# import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Load trades dataset
trades_df = pd.read_csv("data/dataset-trades.csv")
# print(trades_df)

Base = declarative_base()

class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    sym = Column(String(255))
    prc = Column(Float)
    action = Column(String(255))
    txid = Column(String(255))
    datetime = Column(String(255))
    accid = Column(Integer)
    qty = Column(Integer)


# Replace 'mysql+pymysql' with the appropriate dialect for your MySQL connector
# The format is 'mysql+connector' or 'mysql+pymysql' depending on the MySQL connector you are using.
# Replace 'root', 'password', 'my_database', and 'db' with your MySQL username, password, database name, and hostname (service name or IP).
engine = create_engine('mysql+mysqlconnector://root:password@db/my_database')

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# Check if the 'trades' table is empty
Session = sessionmaker(bind=engine)
session = Session()
is_table_empty = session.query(Trade).count() == 0
session.close()

# If the table is empty, load trades dataset and insert data into the database
if is_table_empty:
    # Load trades dataset
    trades_df = pd.read_csv("data/dataset-trades.csv")

    # Create the table if it doesn't exist
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Insert trades data into the database
    for _, row in trades_df.iterrows():
        trade = Trade(
            sym=row['sym'],
            prc=row['prc'],
            action=row['action'],
            txid=row['txid'],
            datetime=row['datetime'],
            accid=row['accid'],
            qty=row['qty']
        )
        session.add(trade)

    # Commit the changes and close the session
    session.commit()
    session.close()



# Create a function to calculate the final client account states
def calculate_client_account_states(trades_df):
    # Group the trades data by accid and sym and calculate the final quantity
    final_states_df = trades_df.groupby(['accid', 'sym'], as_index=False)['qty'].sum()
    return final_states_df

# Create a function to calculate the cost basis
def calculate_cost_basis(trades_df):
    # Assuming 'cost_basis' is calculated as prc * qty
    trades_df['cost_basis'] = trades_df['prc'] * trades_df['qty']
    return trades_df


trades_db = pd.read_sql_table('trades', engine)

final_states_df = calculate_client_account_states(trades_db)
cost_basis_df = calculate_cost_basis(trades_db)

# Print the final client account states
print("Final Client Account States:")
print(final_states_df)

# Print the cost basis
print("Cost Basis:")
print(cost_basis_df)


# Return trades_df so that it can be accessed in other scripts
def get_trades_df():
    return trades_df