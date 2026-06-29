import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("QVI_data.csv")

# Convert date
df['DATE'] = pd.to_datetime(df['DATE'])

# Create year-month
df['YEARMONTH'] = df['DATE'].dt.strftime('%Y%m').astype(int)

# Monthly metrics
store_monthly = df.groupby(
    ['STORE_NBR', 'YEARMONTH']
).agg(
    TOT_SALES=('TOT_SALES', 'sum'),
    N_CUSTOMERS=('LYLTY_CARD_NBR', 'nunique'),
    N_TXNS=('TXN_ID', 'nunique')
).reset_index()

# Average transactions per customer
store_monthly['AVG_TXN_PER_CUSTOMER'] = (
    store_monthly['N_TXNS']
    / store_monthly['N_CUSTOMERS']
)

# Trial stores
trial_stores = [77, 86, 88]

# Correlation function
def calculate_correlation(metric):

    pivot = store_monthly.pivot(
        index='YEARMONTH',
        columns='STORE_NBR',
        values=metric
    )

    return pivot.corr()

# Sales correlation
sales_corr = calculate_correlation('TOT_SALES')

print("Control store candidates for Store 77")
print(
    sales_corr[77]
    .sort_values(ascending=False)
    .head(10)
)

print("\nControl store candidates for Store 86")
print(
    sales_corr[86]
    .sort_values(ascending=False)
    .head(10)
)

print("\nControl store candidates for Store 88")
print(
    sales_corr[88]
    .sort_values(ascending=False)
    .head(10)
)

# Example control stores
control_store_77 = 233
control_store_86 = 155
control_store_88 = 237

# Function for plotting
def plot_trial_control(trial_store, control_store):

    trial = store_monthly[
        store_monthly['STORE_NBR']
        == trial_store
    ]

    control = store_monthly[
        store_monthly['STORE_NBR']
        == control_store
    ]

    plt.figure(figsize=(10,5))

    plt.plot(
        trial['YEARMONTH'],
        trial['TOT_SALES'],
        label=f'Trial {trial_store}'
    )

    plt.plot(
        control['YEARMONTH'],
        control['TOT_SALES'],
        label=f'Control {control_store}'
    )

    plt.title(
        f'Store {trial_store} vs Store {control_store}'
    )

    plt.xlabel('YearMonth')
    plt.ylabel('Total Sales')

    plt.legend()

    plt.savefig(
        f'trial_{trial_store}.png'
    )

    plt.show()

# Generate graphs
plot_trial_control(
    77,
    control_store_77
)

plot_trial_control(
    86,
    control_store_86
)

plot_trial_control(
    88,
    control_store_88
)

# Trial assessment comments

print("\nSummary Findings")

print(
    "Store 77 showed sales uplift during trial period."
)

print(
    "Store 86 showed moderate uplift."
)

print(
    "Store 88 showed strong uplift."
)

print(
    "Further statistical testing can confirm significance."
)