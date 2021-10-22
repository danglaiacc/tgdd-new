import pandas as pd

# print(pd.read_csv('../iphone.csv')['id'].values.tolist())
def get_phone_id(file_path, column):
    return pd.read_csv(file_path)[column].values.tolist()

