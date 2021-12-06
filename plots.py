from analysis import WordAnalysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from typing import List

def get_histogram(words: WordAnalysis, save_path: str) -> str:
    """
    Creates a histogram showing the unweighted frequency distribution
    of the (unique) words used in the book. Returns the path to the
    saved histogram.
    Arguments:
    words: WordAnalysis - A WordAnalysis object describing the words used
    in the book
    save_path: str - The path to save the histogram to
    """
    bins =  generate_bins(minimum=0, maximum=get_maximum_frequency(words), bin_width=500)
    dic = {"Range": "0-500" ,"Stars": [np.nan]} #Creating the columns of the data framw
    df = pd.DataFrame(dic)

    for i in bins:
        df = df.append({'Range':i,'Stars':0},ignore_index=True)

    for word in words.with_uses:
        key = 'netflix'
        if key in word['frequency'].keys():
            df = df.append({"Range":bins[get_bins(word['frequency']['netflix'].frequency,bins)],"Stars":word['frequency']['netflix'].stars},ignore_index=True)

    fig = px.histogram(df, 'Range',color='Range')
    pio.write_html(fig, file=save_path)

    return save_path

def get_bins(frequency: int, bins: List[str]) -> int:
    """
    Determines which bin a word walls into
    based on its frequency and the bins themselves
    For example, with bins of width 500, a word with frequency
    1301 will fall into the bin 1001-1500.
    Returns the index in bins for the correct bin, i.e. with bin width
    500 and frequency 1301, the function will return 2, as 1001-1500
    is the 3rd bin in the elist.
    Arguments:
    frequency: int - The frequency of the word
    bins: List[str] - A list of the bins in the format 'low-high', for example
    ['0-500', '501-1000', '1001-1500', ...]
    """

    for i in range(len(bins)):
        bin = bins[i].split("-")
        assert len(bin) == 2, "Bin must have length 2"

        low, high = bin
        if frequency >= int(low) and frequency < int(high):
            return i

    return (len(bins)-1)

def generate_bins(minimum: int, maximum: int, bin_width: int=500) -> List[str]:
    """
    This function generates histogram binnings based on the minimum/maximum
    value of the data and the bin width and returns them in the format
    ['low-high'], e.g. ['0-500', '501-1000', ...]
    Arguments:
    minimum: int - The minimum allowed value for the data
    maximum: int - The maximum allowed value for the data
    bin_width: int (Optional, default 500) - The width of the bins
    """
    low = 0
    high = bin_width
    bins=[]

    while(high<=maximum):
        bin = str(low)+"-"+str(high)
        bins.append(bin)
        low = high
        high += bin_width

    return bins

def get_maximum_frequency(words: WordAnalysis) -> int:
    """
    This functions gets the highest frequency present in all the
    words.
    Arguments:
    words: WordAnalysis - A WordAnalysis object describing the words
    used in the book
    """
    maximum_frequency = 0
    for word in words.with_uses:
        key = 'netflix'
        if key in word['frequency'].keys():
            maximum_frequency = max(maximum_frequency,word['frequency']['netflix'].frequency)
    return maximum_frequency

