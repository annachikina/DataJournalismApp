import pandas as pd


def collect_stat(path, column_name, axis_name, name_csv, group_name='Количество статей'):
    data = pd.read_csv(path)
    data_stat = data[column_name].value_counts().rename_axis(axis_name).to_frame(name=group_name)
    data_stat.to_csv(name_csv)
    return data_stat

