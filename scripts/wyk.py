# Wyk dataset

# Path
path="data/"
# Load in dataset
df=pd.read_csv(path+'wyk.csv', header =[0], delimiter=',', encoding="utf-8")

df = df.assign(name = df.name.str.split(r'(\; )')).explode('name').loc[lambda x : x['name']!='']
df = df[df['name'].str.contains('; ')==False ]
df.reset_index(inplace=True, drop=True)
df.to_csv(path+'wyk_names.csv')