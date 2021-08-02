import streamlit as st
from util import ner_finder, otp_request


def load_page():
    st.title('Помощник журналиста')
    st.header('На этой странице можно просмотреть все релевантные статьи к готовящемуся материалу')
    col1, col2 = st.beta_columns(2)

    with col1:
        button_name = "Найти имена, места и организации"
        input_text = st.text_area('Начните набирать текст в поле. Когда готово, нажмите  "%s"' % button_name,
                                  height=700)
        st.button(button_name)
        names = ner_finder.finder(input_text)

    with col2:
        with st.form("filter_form"):
            st.subheader('Параметры фильтрации')

            ne = st.multiselect("Выберите имя, место и/или организацию", names)
            ne = [n.lower() for n in ne]

            unique_source_topic = otp_request.get_unique_source_topics()

            # sources_list = otp_request.get_source()
            sources_list = sorted(unique_source_topic["source"].unique())
            sources = st.multiselect('Выберите источник', sources_list)

            # topics_list = otp_request.get_topics()
            topics_list = sorted(unique_source_topic["topic"].unique())
            topics = st.multiselect("Выберите одну или несколько рубрик", topics_list)

            dates = st.date_input("Задайте период поиска", value=[])

            st.form_submit_button("Применить фильтры")

        filtered_df = otp_request.get_filtered_data(ne, [], topics, dates, sources)

        if len(filtered_df) == 100:
            st.write("Я нашёл более 100 статей. Показываю последние 30 из них.")
            filtered_df = filtered_df.sort_values(by="_time", ascending=False)[:30]
        elif len(filtered_df) > 30:
            st.write("Всего я нашёл %d статей. Показываю последние 30 из них." % len(filtered_df))
            filtered_df = filtered_df.sort_values(by="_time", ascending=False)[:30]
        else:
            st.write("Всего я нашёл %d статей." % len(filtered_df))
        if len(filtered_df) > 0:
            article_names = filtered_df["art_ind"].values
            selected_article = st.selectbox("Выберите статью, чтобы прочитать её текст", article_names)
            [date, title] = selected_article.split(": ")
        else:
            st.write("Попробуйте поменять фильтры.")

    col1, _ = st.beta_columns([3, 1])
    with col1:
        if len(filtered_df) > 0:
            article = otp_request.get_article_by_index(selected_article)["text"].values[0]
            article_params = filtered_df[filtered_df["art_ind"] == selected_article]

            st.header(title)
            st.subheader(date)
            st.subheader('Рубрика: %s' % article_params["topic"].values[0])
            st.write(article)
