from analysis import WordAnalysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio

def get_histogram(words: WordAnalysis) -> str:
    """
    Creates a histogram showing the unweighted frequency distribution
    of the (unique) words used in the book. Returns the path to the
    saved histogram.
    Arguments:
    words: WordAnalysis - A WordAnalysis object describing the words used
    in the book
    """
    bins =  generate_bins(get_maximum_frequency(words)) #generating the bins
    dic = {"Range": "0-500" ,"Stars": [np.nan]} #Creating the columns of the data framw
    df = pd.DataFrame(dic)
    for i in bins:
        df = df.append({'Range':i,'Stars':0},ignore_index=True)

    for word in words.with_uses:
        key = 'netflix' #netflix is the key
        if key in word['frequency'].keys():  # element is: i['frequency']['netflix'].frequency
            df = df.append({"Range":bins[get_bins(word['frequency']['netflix'].frequency,bins)],"Stars":word['frequency']['netflix'].stars},ignore_index=True)
    stars_design = ["★","★★","★★★","★★★★","★★★★★"]
    fig = px.histogram(df, 'Range',color='Range') # generating the plotly histogram
    path = 'Histogram.html'
    pio.write_html(fig, file=path)
    return path

def get_bins(freq_num,bins):
    """
    This function determines which range the number falls into
    example: 100, will fall into the range '0-500'
    """
    flag=1
    for i in range(len(bins)):
        lst = bins[i].split("-")
        if freq_num >= int(lst[0]) and freq_num < int(lst[1]):
            return i
    return (len(bins)-1)


def generate_bins(maximum_num):
    """
    This function generates bins based on the maximum element value
    """
    a = 0
    b= 500
    lst=[]
    while(b<=maximum_num):
        lst.append(str(a)+"-"+str(b))
        a=b
        b=b+500
    return lst

def get_maximum_frequency(words: WordAnalysis) -> int:
    """
    This functions gets the highest frequency value of the word
    Arguments:
    words: WordAnalysis - A WordAnalysis object describing the words
    used in the book
    """
    maximum_num = 0
    for word in words.with_uses:
        key = 'netflix'
        if key in word['frequency'].keys():
            maximum_num = max(maximum_num,word['frequency']['netflix'].frequency)
    return maximum_num
