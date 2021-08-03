from ot_simple_connector.connector import Connector
import pandas as pd
import time

host = '192.168.4.65'
port = '80'
user = 'admin'
password = '12345678'
conn = Connector(host, port, user, password, loglevel="DEBUG")


def get_dedup_list(param):
    query_text = "| readFile format=parquet path=news_kw_ne_index | fields %s | dedup %s" % (param, param)
    cache_ttl = 59
    tws = 11
    twf = 22
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load())[param].values


def get_filtered_archive(ne, kw):
    query_text = "| readFile format=parquet path=news_kw_ne_index "
    for param, col_name in [(ne, "ner"), (kw, "kw")]:
        if len(param) == 0:
            continue
        query_text += '| where like(' + col_name + ', "%' + param + '%") '
    query_text += "| fields _time, art_ind, topic, source | dedup art_ind | sort _time | tail 100"
    cache_ttl = 59
    tws = 11
    twf = 22
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load())


def get_filtered_data(ne, kw, topic, dates, source, index=[]):
    query_text = "| readFile format=parquet path=news_kw_ne_index "
    for params_list, col_name in [(ne, "ner"), (topic, "topic"), (source, "source"), (kw, "kw"), (index, "art_ind")]:
        params = [p for p in params_list if len(p) > 0]
        if len(params) == 0:
            continue
        join_string = " OR %s = " % col_name
        condition = col_name + " = " + join_string.join(
            ['"' + s + '"' for s in params])  # | where col_name = "SomeName" OR col_name = "SomeName"
        query_text += "| where %s " % condition
    if len(dates) == 2:
        start, end = dates
        start = time.mktime(start.timetuple())
        end = time.mktime(end.timetuple())
        query_text += "| search _time>%s AND _time<%s " % (start, end)
    query_text += "| fields art_ind, _time, topic | dedup art_ind | sort _time | tail 100"
    cache_ttl = 59
    tws = 11
    twf = 22
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load())


def get_article_by_index(index):
    query_text = "| readFile format=parquet path=news_text_ind "
    query_text += '| where art_ind = "%s" ' % index
    cache_ttl = 59
    tws = 11
    twf = 22
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load())


def get_source(ne=[]):
    query_text = "| readFile format=parquet path=news_kw_ne_index "
    for params, col_name in [(ne, "ner")]:
        if len(params) == 0:
            continue
        join_string = " OR %s = " % col_name
        condition = col_name + " = " + join_string.join(
            ['"' + s + '"' for s in params])  # | where col_name = "SomeName" OR col_name = "SomeName"
        query_text += "| where %s " % condition
    query_text += "| chart count by source"
    cache_ttl = 59
    tws = 11
    twf = 22
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    result = job.dataset.load()
    return [r["source"] for r in result if len(r["source"]) < 30]


def get_topics(ne=[], source=[]):
    query_text = "| readFile format=parquet path=news_kw_ne_index "
    for params, col_name in [(ne, "ner"), (source, "source")]:
        if len(params) == 0:
            continue
        join_string = " OR %s = " % col_name
        condition = col_name + " = " + join_string.join(
            ['"' + s + '"' for s in params])  # | where col_name = "SomeName" OR col_name = "SomeName"
        query_text += "| where %s " % condition
    query_text += "| chart count by topic"
    cache_ttl = 59
    tws = 11
    twf = 22
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    result = job.dataset.load()
    return [r["topic"] for r in result if len(r["topic"]) < 30]


def get_unique_source_topics():
    query_text = "| readFile format=parquet path=news_kw_ne_index | eval group = source+\":\"+topic | dedup group "
    cache_ttl = 59
    tws = 11
    twf = 22
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    result = pd.DataFrame(job.dataset.load())
    return result
