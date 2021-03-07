import pandas as pd

def empty_df(index=[]):

    empty = pd.DataFrame(index=index, data={})
    empty.index.name = 'Date'

    return empty
    

def rename_MultiIndex(index, rename):

    result = []

    for i, myTuple in enumerate(index):
        myTuple = list(myTuple)
        if (i % 2) == 0:
            myTuple[1] = f"Earnings Per Share {rename}"
        myTuple = tuple(myTuple)
        result.append(myTuple)

    index = pd.MultiIndex.from_tuples(result, names=["Year", "Estimates"])

    return index

def flatten(mylist):

    flat_list = [item for sublist in mylist for item in sublist]

    return flat_list


def get_table(soup):

    mylist= []

    for i, tr in enumerate(soup.select('tr')):
        row_data = [td.text for td in tr.select('td, th') if td.text]

        if not row_data:
            continue

        if len(row_data) < 12:
            row_data = ['X'] + row_data

        mylist.append(row_data)

    return mylist