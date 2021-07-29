import streamlit as st
import analysis
import otp_request


def load_page():
    st.title('Архив статей')
    st.header('На этой странице можно провести поиск по всему архиву')

    st.subheader('Введите имя и/или ключевое слово')

    ne = st.text_input('Введите имя, место и/или название организации')

    kw = st.text_input('Введите ключевое слово')

    archive_df = otp_request.get_filtered_archive(ne, kw)
    if len(archive_df) == 0:
        st.write("Не удалось найти в архиве подходящие материалы, попробуйте новый поиск")
    else:
        st.subheader('Задайте фильтры')

        genres = list(set(archive_df["topic"].values))
        topics = st.multiselect("Выберите одну или несколько тем", genres)

        dates = st.date_input("Введите период", value=[])

        sources_list = list(set(archive_df["source"].values))
        sources = st.multiselect('Выберите источники', sources_list)

        filtered_df = otp_request.get_filtered_data([],
                                                    [],
                                                    topics,
                                                    dates,
                                                    sources,
                                                    index=archive_df["index"].values)

        if len(filtered_df) == 100:
            st.write("Я нашёл более 100 статей. Показываю последние 30 из них.")
            filtered_df = filtered_df[-30:]
        elif len(filtered_df) > 30:
            st.write("Всего я нашёл %d статей. Показываю последние 30 из них." % len(filtered_df))
            filtered_df = filtered_df[-30:]
        else:
            st.write("Всего я нашёл %d статей." % len(filtered_df))
        # article_names = [": ".join(x) for x in list(zip(filtered_df["source"], filtered_df["title"].values))]
        article_names = filtered_df["index"].values

        selected_article = st.selectbox("Выберите статью, чтобы прочитать её текст", article_names)
        [date, title] = selected_article.split(": ")

        # article = filtered_df[filtered_df["title"] == selected_article.split(": ")[1]]
        article = otp_request.get_article_by_index(selected_article)["text"].values[0]
        article_params = filtered_df[filtered_df["index"] == selected_article]

        st.header(title)
        st.subheader(date)
        st.subheader('Рубрика: %s' % article_params["topic"].values[0])
        st.write(article)

    if st.button('Посмотреть статистику'):
        analysis.load_page()

    else:
        st.write('Нажмите, чтобы увидеть аналитику по статьям')
