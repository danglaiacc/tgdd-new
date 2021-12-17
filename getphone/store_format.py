import pandas as pd, re

source = pd.read_csv('./store1.csv')
#print(source.head())


address_pattern = re.compile(r'(?P<address>.+),\s*(?P<district>.+),')
#source[['district', 'address']] = [re.search(address_pattern, store_address).groups() 
#        for store_address in source['store_address']]

source[['address', 'district']] = source.store_address.str.extract(address_pattern)

source.to_csv('aa.csv')
