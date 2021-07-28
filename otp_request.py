from ot_simple_connector.connector import Connector
import pandas as pd
import time

host = '192.168.4.65'
port = '80'
user = 'admin'
password = '12345678'
conn = Connector(host, port, user, password, loglevel="DEBUG")


def get_dedup_list(param):
    query_text = "| inputlookup news_kw_ne_expand.csv | fields %s | dedup %s" % (param, param)
    cache_ttl = 59
    tws = 11
    twf = 22
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load())[param].values


def get_filtered_data(ne, topic, dates, source):
    query_text = "| inputlookup news_kw_ne_expand.csv "
    for params, col_name in [(ne, "ner"), (topic, "topic"), (source, "source")]:
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
    query_text += "| fields _c0, date, title, text, topic, source | dedup _c0 | sort _time | head 100"
    cache_ttl = 59
    tws = 11
    twf = 22
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load())


def get_source(ne):
    query_text = "| inputlookup news_kw_ne_expand.csv "
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


def get_topics(ne, source):
    query_text = "| inputlookup news_kw_ne_expand.csv "
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
