import streamlit as st
import pandas as pd
import altair as alt


def plot_chart(data, x, y, x_title, y_title="", height=850):
    return (alt
            .Chart(data, height=height)
            .mark_bar(tooltip=alt.TooltipContent('encoding'))
            .encode(x=alt.X(x,
                            title=x_title,
                            axis=alt.Axis(labelFontSize=12)),
                    y=alt.Y(y,
                            sort=alt.EncodingSortField(field=x, order="descending"),
                            title=y_title,
                            axis=alt.Axis(labelFontSize=14)
                            ),
                    color=alt.Color(y,
                                    legend=None,
                                    scale=alt.Scale(scheme="category10"),
                                    )
                    )
            )


def load_page():
    st.title("Статистика архива")
    st.header("Эта страница техническая. Здесь можно увидеть обзор всех материалов архива")
    stats_selected = st.selectbox("Выберите источник", ["Все источники", "Лента", "Новости 33"])

    if stats_selected == "Все источники":
        col1, col2 = st.beta_columns(2)

        with col1:

            # ТОП СУЩНОСТЕЙ
            ner = pd.read_csv('data/ner_top1000.csv')
            ner_data = ner.iloc[:10]
            ner_chart = plot_chart(ner_data, "count", "ner", "Количество упоминаний")
            st.subheader('Топ-10 самых частоупоминаемых явлений в материалах архива')
            st.altair_chart(ner_chart, use_container_width=True)

            # ГРАФИК ПО ВСЕМ ДАТАМ
            alldat = pd.read_csv('data/final_date.csv')
            date_stats = alldat.set_index('Дата').sort_index()[-24:]
            st.subheader('Количество опубликованных материалов за последние 2 года')
            st.line_chart(date_stats, height=500)

        with col2:

            # ГРАФИК ПО ВСЕМ РУБРИКАМ
            alltop = pd.read_csv('data/all_topic.csv')
            topic_chart = plot_chart(alltop, "Количество статей", "Рубрика", "Количество статей")
            st.subheader('Количество всех статей по рубрикам')
            st.altair_chart(topic_chart, use_container_width=True)

            # ГРАФИК КОЛИЧЕСТВО СТАТЕЙ ПО ГОДАМ
            yeardat = pd.read_csv('data/year_date.csv')
            year_stats = yeardat.set_index('Год')
            st.subheader('Количество доступных опубликованных материалов по годам')
            st.bar_chart(year_stats, height=500)

        # ГРАФИК ПО ИСТОЧНИКАМ
        source_data = pd.read_csv('data/all_source.csv')
        st.subheader('Количество статей в доступных источниках')
        source_chart = plot_chart(source_data, "Источник", "Количество статей", "Источник", height=500)
        st.altair_chart(source_chart, use_container_width=True)

    elif stats_selected == "Лента":
        col1, col2 = st.beta_columns(2)

        with col1:

            # ГРАФИК ПО РУБРИКАМ ЛЕНТЫ
            lentop = pd.read_csv('data/lenta_topic.csv')
            st.subheader('Количество всех статей по рубрикам')
            lenta_topic_chart = plot_chart(lentop, "Количество статей", "Рубрика", "Количество статей")
            st.altair_chart(lenta_topic_chart, use_container_width=True)

        with col2:

            # ГРАФИК ПО ДАТАМ ЛЕНТЫ
            lendat = pd.read_csv('data/lenta_date_final.csv')
            lenta_date_stats = lendat.set_index('Дата')
            ld = lenta_date_stats.sort_index()
            st.subheader('Количество опубликованных материалов по времени')
            st.line_chart(ld, height=500)

    elif stats_selected == "Новости 33":
        col1, col2 = st.beta_columns(2)

        with col1:

            # ГРАФИК ПО РУБРИКАМ НОВОСТИ 33
            n33top = pd.read_csv('data/news33_topic.csv')
            st.subheader('Количество всех статей по рубрикам')
            news33_topic_chart = plot_chart(n33top, "Количество статей", "Рубрика", "Количество статей")
            st.altair_chart(news33_topic_chart, use_container_width=True)

        with col2:

            # ГРАФИК ПО ДАТАМ НОВОСТИ 33
            n33dat = pd.read_csv('data/news33_date_final.csv')
            n33_date_stats = n33dat.set_index('Дата')
            st.subheader('Количество опубликованных материалов по времени')
            st.line_chart(n33_date_stats, height=500)
