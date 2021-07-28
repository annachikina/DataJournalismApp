import streamlit as st
import ner_finder
import otp_request


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
        st.subheader('Параметры фильтрации')

        ne = st.multiselect("Выберите имя, место и/или организацию", names)

        sources_list = otp_request.get_source(ne)
        sources = st.multiselect('Выберите источник', sources_list)

        topics_list = otp_request.get_topics(ne, sources)
        topics = st.multiselect("Выберите одну или несколько рубрик", topics_list)

        dates = st.date_input("Задайте период поиска", value=[])

        filtered_df = otp_request.get_filtered_data(ne, topics, dates, sources)

        if len(filtered_df) == 100:
            st.write("Я нашёл более 100 статей. Показываю последние 30 из них.")
            filtered_df = filtered_df[-30:]
        elif len(filtered_df) > 30:
            st.write("Всего я нашёл %d статей. Показываю последние 30 из них." % len(filtered_df))
            filtered_df = filtered_df[-30:]
        else:
            st.write("Всего я нашёл %d статей." % len(filtered_df))
        article_names = [": ".join(x) for x in list(zip(filtered_df["source"], filtered_df["title"].values))]

        selected_article = st.selectbox("Выберите статью, чтобы прочитать её текст", article_names)

    article = filtered_df[filtered_df["title"] == selected_article.split(": ")[1]]

    st.header(article["title"].values[0])
    st.subheader(article["date"].values[0])
    st.subheader('Рубрика: %s' % article["topic"].values[0])
    st.write(article["text"].values[0])
