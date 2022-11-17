import pandas as pd
df = pd.read_csv('data/movies_detailed.csv')
input = 'the'

#input_case = df[df['title'].str.contains(input) | df['plot'].str.contains(input)] 

tester = df['title'].str.contains(input)
for ind in df.index:
    if (input in df['title'][ind]):
        print(df['title'][ind])
