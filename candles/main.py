from collections import Counter
from pathlib import Path
import csv
import dateutil.parser

DATA_FILE = Path('..') / 'data' / 'crypto' / 'bitcoin.csv'

data = []

# Read file

# контекстный мененджер
with open(DATA_FILE) as f:
    reader = csv.DictReader(f)
    print(reader)
    for row in reader:
        row['Date'] = dateutil.parser.parse(row['Date'])
        for col in ('Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap'):
            row[col] = float(row[col].replace(',','')) if row[col] != '-' else None

        if row['Open'] < row['Close']:
            row['Color'] = 'Green'
        elif row['Open'] > row['Close']:
            row['Color'] = 'Red'
        else:
            row['Color'] = None

        data.append(row)

# Sort data

data.sort(key=lambda row: row['Date'])

# Data exploration

print(''.join(str(row['Color'])[0] for row in data))
print(Counter(str(row['Color'])[0] for row in data))

price_daily_avg = [(row['Low']+row['High']) / 2 for row in data]
volume_sum = sum(row['Volume'] or 0 for row in data)
daily_weights = [(row['Volume'] or 0) / volume_sum for row in data]



price_avg = sum(p*w for p,w in zip(price_daily_avg, daily_weights))
volume_cnt = sum(int(r['Volume'] is not None) for r in data)
price_avg_naive = sum(p*(1/volume_cnt) 
            for p,w in zip(price_daily_avg, daily_weights) if w > 0)
print(price_avg, '||', price_avg_naive)

#import pdb; pdb.set_trace()