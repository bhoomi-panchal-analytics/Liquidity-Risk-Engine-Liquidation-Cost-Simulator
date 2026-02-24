

import pandas as pd

def clean_data(df: pd.DataFrame):

    df = df.copy()

    df = df.drop_duplicates(subset='Date')
    df = df.sort_values('Date')

    # Remove rows with zero or missing volume
    df = df[df['Volume'] > 0]
    df = df.dropna()

    return df
