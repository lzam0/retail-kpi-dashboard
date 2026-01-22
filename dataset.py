import pandas as pd
import numpy as np

np.random.seed(42)

dates = pd.date_range(start='2026-01-01', periods=365)
channels = ['store', 'online']

data = []

for date in dates:
    weekday = date.day_name()
    month = date.month
    is_weekend = weekday in ['Saturday', 'Sunday']
    is_holiday = np.random.choice([0,1], p=[0.9,0.1])  # some holidays randomly
    promo_flag = np.random.choice([0,1], p=[0.8,0.2])
    weather_score = np.random.randint(1,11)  # 1=bad, 10=great

    for channel in channels:
        # Base traffic
        if channel == 'store':
            base_footfall = np.random.randint(500, 2000)
            purchase_rate = np.random.uniform(0.05, 0.15)
            return_rate = np.random.uniform(0.02, 0.05)
            # adjust for weekend/holiday
            footfall_or_sessions = int(base_footfall * (1.2 if is_weekend else 1.0) * (1.3 if is_holiday else 1.0))
        else:  # online
            base_sessions = np.random.randint(1000, 5000)
            purchase_rate = np.random.uniform(0.03, 0.12)
            return_rate = np.random.uniform(0.05, 0.08)
            footfall_or_sessions = base_sessions

        # Seasonal adjustments
        if month in [11,12]:
            footfall_or_sessions = int(footfall_or_sessions * np.random.uniform(1.3, 1.6))
            purchase_rate = min(purchase_rate * np.random.uniform(1.2,1.5), 0.9)
        elif month in [8,9]:
            footfall_or_sessions = int(footfall_or_sessions * np.random.uniform(1.1,1.3))
            purchase_rate = min(purchase_rate * np.random.uniform(1.1,1.3), 0.9)

        # Online zero-purchase days
        if channel == 'online' and np.random.rand() < 0.15:
            purchases = 0
            returns = 0
            sales_value = 0
            returns_value = 0
        else:
            purchases = int(footfall_or_sessions * purchase_rate)
            returns = int(purchases * return_rate)
            avg_sale_value = np.random.randint(50,200)
            sales_value = purchases * avg_sale_value
            returns_value = returns * avg_sale_value

        data.append([
            date, channel, footfall_or_sessions, purchases, returns,
            sales_value, returns_value, weekday, is_weekend, is_holiday, promo_flag, weather_score
        ])

df = pd.DataFrame(data, columns=[
    'date', 'channel', 'footfall_or_sessions', 'purchases', 'returns',
    'sales_value', 'returns_value', 'weekday', 'is_weekend', 'is_holiday', 'promo_flag', 'weather_score'
])

df.to_csv('retail_dataset.csv', index=False)
print(df.head())
print(f"Dataset generated with {len(df)} rows")
