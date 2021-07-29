import streamlit as st
import pandas as pd
import altair as alt


def load_page():
    st.title("Статистика архива")

    st.header("На этой странице вы можете посмотреть статистику по всем материалам архива")

    stats_selected = st.selectbox("Выберите источник", ["Все источники", "Лента", "Новости 33"])

    if stats_selected == "Все источники":
        col1, col2 = st.beta_columns(2)

        with col1:

            # ТОП СУЩНОСТЕЙ

            ner = pd.read_csv('ner_top1000.csv')
            ner_data = ner.iloc[:10]

            ner_chart = (
                alt.Chart(
                    ner_data, height=850
                )
                    .mark_bar()
                    .encode(
                    x=alt.X("count", title="Количество упоминаний"),
                    y=alt.Y(
                        "ner",
                        sort=alt.EncodingSortField(field="Количество статей", order="descending"),
                        title=""
                    ),
                    color=alt.Color(
                        "ner",
                        legend=alt.Legend(title="Имена"),
                        scale=alt.Scale(scheme="category10"),
                    )
                )
            )
            st.subheader('Топ-10 самых частоупоминаемых явлений в материалах архива')
            st.altair_chart(ner_chart, use_container_width=True)

            # ГРАФИК ПО ВСЕМ ДАТАМ

            alldat = pd.read_csv('final_date.csv')
            date_stats = alldat.set_index('Дата')
            dfd = date_stats.sort_index()[56:]
            st.subheader('Количество опубликованных материалов за последние 2 года')
            st.line_chart(dfd, height=500)

        with col2:

            # ГРАФИК ПО ВСЕМ РУБРИКАМ

            alltop = pd.read_csv('all_topic.csv')

            st.subheader('Количество всех статей по рубрикам')

            topic_chart = (
                alt.Chart(
                    alltop, height=850
                )
                    .mark_bar()
                    .encode(
                    x=alt.X("Количество статей", title="Количество статей"),
                    y=alt.Y(
                        "Рубрика",
                        sort=alt.EncodingSortField(field="Количество статей", order="descending"),
                        title=""
                    ),
                    color=alt.Color(
                        "Рубрика",
                        legend=alt.Legend(title="Рубрики"),
                        scale=alt.Scale(scheme="category10"),
                    )
                )
            )

            st.altair_chart(topic_chart, use_container_width=True)

            yeardat = pd.read_csv('year_date.csv')
            year_stats = yeardat.set_index('Год')
            st.subheader('Количество доступных опубликованных материалов по годам')
            st.bar_chart(year_stats, height=500)

        # ГРАФИК ПО ИСТОЧНИКАМ

        allsou = pd.read_csv('all_source.csv')
        st.subheader('Количество статей в доступных источниках')

        source_chart = (
            alt.Chart(
                allsou, height=400
            )
                .mark_bar()
                .encode(
                x=alt.X("Источник", title="Источник"),
                y=alt.Y(
                    "Количество статей",
                    sort=alt.EncodingSortField(field="Количество статей", order="descending"),
                    title=""
                ),
                color=alt.Color(
                    "Источник",
                    legend=alt.Legend(title="Источник"),
                    scale=alt.Scale(scheme="category10"),
                )
            )
        )

        st.altair_chart(source_chart, use_container_width=True)



    elif stats_selected == "Лента":

        col1, col2 = st.beta_columns(2)

        with col1:
            # ГРАФИК ПО РУБРИКАМ ЛЕНТЫ

            lentop = pd.read_csv('lenta_topic.csv')
            st.subheader('Количество всех статей по рубрикам')

            lenta_topic_chart = (
                alt.Chart(
                    lentop, height=500
                )
                    .mark_bar()
                    .encode(
                    x=alt.X("Количество статей", title="Количество статей"),
                    y=alt.Y(
                        "Рубрика",
                        sort=alt.EncodingSortField(field="Количество статей", order="descending"),
                        title=""
                    ),
                    color=alt.Color(
                        "Рубрика",
                        legend=alt.Legend(title="Рубрики"),
                        scale=alt.Scale(scheme="category10"),
                    )
                )
            )

            st.altair_chart(lenta_topic_chart, use_container_width=True)

        with col2:

            # ГРАФИК ПО ДАТАМ ЛЕНТЫ

            lendat = pd.read_csv('lenta_date_final.csv')
            lenta_date_stats = lendat.set_index('Дата')
            ld = lenta_date_stats.sort_index()[:32]
            st.subheader('Количество опубликованных материалов по времени')
            st.line_chart(ld, height=500)

    elif stats_selected == "Новости 33":

        col1, col2 = st.beta_columns(2)

        with col1:
            # ГРАФИК ПО РУБРИКАМ НОВОСТИ 33

            n33top = pd.read_csv('news33_topic.csv')
            st.subheader('Количество всех статей по рубрикам')

            news33_topic_chart = (
                alt.Chart(
                    n33top, height=500
                )
                    .mark_bar()
                    .encode(
                    x=alt.X("Количество статей", title="Количество статей"),
                    y=alt.Y(
                        "Рубрика",
                        sort=alt.EncodingSortField(field="Количество статей", order="descending"),
                        title=""
                    ),
                    color=alt.Color(
                        "Рубрика",
                        legend=alt.Legend(title="Рубрики"),
                        scale=alt.Scale(scheme="category10"),
                    )
                )
            )

            st.altair_chart(news33_topic_chart, use_container_width=True)

        with col2:

            # ГРАФИК ПО ДАТАМ НОВОСТИ 33

            n33dat = pd.read_csv('news33_date_final.csv')
            n33_date_stats = n33dat.set_index('Дата')
            st.subheader('Количество опубликованных материалов по времени')
            st.line_chart(n33_date_stats, height=500)
