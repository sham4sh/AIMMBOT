import pandas as pd
import customWidgets


df = pd.read_csv('data/movies_detailed.csv')
input = 'shdhdhshs'

#input_case = df[df['title'].str.contains(input) | df['plot'].str.contains(input)] 

tester = df['title'].str.contains(input)
for ind in df.index:
    if (input in df['title'][ind]):
        print(df['title'][ind])


def keySearch(inputStr, box):
    df = pd.read_csv('data/movies_detailed.csv')
    for ind in df.index:
        if (inputStr.upper() in df['title'][ind].upper()):
            widget = customWidgets.movieWidget(df['title'][ind])
            box.addWidget(widget)

