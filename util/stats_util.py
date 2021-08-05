import pandas as pd


def collect_stat(data, column_name, axis_name, group_name='Количество статей'):
    data_stat = data[column_name].value_counts().rename_axis(axis_name).to_frame(name=group_name)
    return data_stat

