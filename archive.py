import streamlit as st
import analysis
import otp_request


def load_page():
    st.title('Архив статей')
    st.header('На этой странице можно провести поиск по всему архиву')

    st.subheader('Введите одно или несколько имён или ключевых слов')

    names = otp_request.get_dedup_list("ner")
    ne = st.multiselect('Начните вводить имя, место и/или название организации', names)

    keywords = otp_request.get_dedup_list("kw")
    kw = st.multiselect('Начните вводить ключевое слово', keywords)

    st.subheader('Задайте фильтры')

    genres = otp_request.get_dedup_list("topic")
    topics = st.multiselect("Выберите одну или несколько тем", genres)

    dates = st.date_input("Введите период", value=[])

    sources_list = otp_request.get_dedup_list("source")
    sources = st.multiselect('Выберите источники', sources_list)

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

    if st.button('Посмотреть статистику'):
        analysis.load_page()

    else:
        st.write('Нажмите, чтобы увидеть аналитику по статьям')
