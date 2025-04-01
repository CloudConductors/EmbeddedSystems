import pandas as pd

df = pd.read_csv("./MetroPT3(AirCompressor).csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

start_time_1 = '2020-04-18 00:00:00'
end_time_1 = '2020-04-18 23:59:59'

start_time_2 = '2020-05-29 23:30:00'
end_time_2 = '2020-05-30 06:00:59'

start_time_3 = '2020-06-05 10:00:00'
end_time_3 = '2020-06-07 14:30:59'

start_time_4 = '2020-07-15 14:30:00'
end_time_4= '2020-07-15 19:00:59'

good_data = df[((df["timestamp"] < start_time_1) | (df["timestamp"] > end_time_1)) 
                & ((df["timestamp"] < start_time_2) | (df["timestamp"] > end_time_2)) 
                & ((df["timestamp"] < start_time_3) | (df["timestamp"] > end_time_3)) 
                & ((df["timestamp"] < start_time_4) | (df["timestamp"] > end_time_4))]

# Todo: There are two types of good data, they look different. I need to sort them out. 

bad_data = df[~df.index.isin(good_data.index)]

good_data = good_data.drop(columns=["Unnamed: 0", "timestamp"])
bad_data = bad_data.drop(columns=["Unnamed: 0", "timestamp"])

good_data = good_data.dropna()
bad_data = bad_data.dropna()

gd_mean = good_data.mean()
bd_mean = bad_data.mean()

gd_std = good_data.std()
bd_std = bad_data.std()

print("Good Data Mean:", gd_mean)
print("Bad Data Mean:", bd_mean)
print("Good Data Std:", gd_std)
print("Bad Data Std:", bd_std)







