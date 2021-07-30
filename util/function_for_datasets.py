import pandas as pd
import numpy as np

data = pd.read_csv("lenta_keywords.csv")

def data_stat(data, column_name, axis_name, arch_name, name_csv):
    data_stat=data[column_name].value_counts().rename_axis(axis_name).to_frame(name='Количество статей')

    compression_opts = dict(method='zip', archive_name=(arch_name))
    data_stat().to_csv((name_csv), encoding='utf-8', compression=compression_opts)

    return data_stat

