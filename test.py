import pandas as pd

data = [[1000, 2000, 3000, 4000, 5000, 6000], [2000, 3000, 4000, 5000, 6000, 7000]]
day = ["M", "T", "W", "Th", "Fr", "Sat"]
df = pd.DataFrame(data,day,  columns=day)
print(df)