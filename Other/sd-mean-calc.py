import pandas as pd

df = pd.read_csv("./MetroPT3(AirCompressor).csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

start_time_1 = '2020-04-18 00:23:59'
end_time_1 = '2020-04-19 01:55:36'

start_time_2 = '2020-05-29 23:14:56'
end_time_2 = '2020-05-30 05:56:46'

start_time_3 = '2020-06-05 09:48:40'
end_time_3 = '2020-06-07 14:19:39'

start_time_4 = '2020-07-15 14:25:23'
end_time_4= '2020-07-15 18:52:54'

start_time_5 = '2020-04-12 11:50:31'
end_time_5 = '2020-04-12 23:36:00'


good_data = df[((df["timestamp"] < start_time_1) | (df["timestamp"] > end_time_1)) 
                & ((df["timestamp"] < start_time_2) | (df["timestamp"] > end_time_2)) 
                & ((df["timestamp"] < start_time_3) | (df["timestamp"] > end_time_3)) 
                & ((df["timestamp"] < start_time_4) | (df["timestamp"] > end_time_4))
                & ((df["timestamp"] < start_time_5) | (df["timestamp"] > end_time_5))]

# Todo: There are two types of good data, they look different. I need to sort them out. 

bad_data = df[~df.index.isin(good_data.index)]
good_data_2 = good_data[good_data["TP2"] > 0]
good_data = good_data[good_data["TP2"] <= 0]
gd_2_size = good_data_2.shape[0]
gd_size = good_data.shape[0]
gd_total = gd_2_size + gd_size

good_data = good_data.drop(columns=["Unnamed: 0", "timestamp"])
good_data_2 = good_data_2.drop(columns=["Unnamed: 0", "timestamp"])
bad_data = bad_data.drop(columns=["Unnamed: 0", "timestamp"])

good_data = good_data.dropna()
good_data_2 = good_data_2.dropna()
bad_data = bad_data.dropna()

gd_mean = good_data.mean()
gd_mean_2 = good_data_2.mean()
bd_mean = bad_data.mean()

gd_std = good_data.std()
gd_std_2 = good_data_2.std()
bd_std = bad_data.std()

print("Good Data Mean:", gd_mean)
print("Good Data 2 Mean:", gd_mean_2)
print("Bad Data Mean:", bd_mean)
print("Good Data Std:", gd_std)
print("Good Data 2 Std:", gd_std_2)
print("Bad Data Std:", bd_std)

print("Good Data %:", gd_size / gd_total * 100)
print("Good Data 2 %:", gd_2_size / gd_total * 100)

print("Bad Data Size:", bad_data.shape[0])
print("Good Data Size:", good_data.shape[0])






