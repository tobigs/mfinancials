import pandas as pd

def empty_df(index=[]):

    empty = pd.DataFrame(index=index, data={})
    empty.index.name = 'Date'

    return empty
    

def rename_MultiIndex(index, rename):
    """Renames first, third MultiIndex entry on second level

    Args:
        index (pd.MultiIndex): Multiindex to rename
        rename (string): Currency to insert in Multiindex

    Returns:
        pd.MultiIndex: renamed MulitIndex
    """    

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

    list_flat = [item for sublist in mylist for item in sublist]

    return list_flat


def get_table(soup):
    """Extracts tables as list of lists from bs4.BeautifulSoup

    Args:
        soup (bs4.BeautifulSoup): Soup to extract tables from

    Returns:
        list: List of lists
    """    

    list_result = []

    for tr in soup.select('tr'):
        row_data = [td.text for td in tr.select('td, th') if td.text]

        if not row_data:
            continue

        if len(row_data) < 12:
            row_data = ['X'] + row_data

        list_result.append(row_data)

    return list_result