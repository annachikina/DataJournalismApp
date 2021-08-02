import pandas as pd
import numpy as np


def remove_citation(text):
    return text.replace('""', "").replace('"', "").replace("“", "").replace("”", "").replace("«", "").replace("»", "")


def preprocess_data(data, text_cols, source, time_col="date"):

    for col in text_cols:
        data = data[~((data[col].isna()) | (data["col"] == ""))]
        data[col] = data[col].apply(remove_citation)

    data["_time"] = pd.to_datetime(data[time_col], dayfirst=True).astype(np.int64) // 10 ** 9

    data["source"] = source

    return data

