import streamlit as st
import pandas as pd
import numpy as np


def load_page():
    st.title("Аналитика")

    st.header("На этой странице вы можете посмотреть интересующую вас статистику по выбранным статьям")

    col1, col2 = st.beta_columns(2)

    with col1:
        graph1 = 'Общее количество упоминаний за выбранный период'
        graph2 = 'Количество упоминаний в различных СМИ'
        graph3 = 'Количество упоминаний по тематике'
        graph4 = 'Количество упоминаний в СМИ за месяц'
        graphs = [graph1, graph2, graph3, graph4]
        selected_graph = st.selectbox("Выберите график", graphs)

    with col2:
        if selected_graph == graph1:
            linechart_data = pd.DataFrame(
                np.random.randn(31, 2),
                columns=['Сергей Собянин', 'QR-код'])

            st.subheader('Общее количество упоминаний за выбранный период')
            st.line_chart(linechart_data)
            st.markdown('На графике отображено общее количество упоминаний выбранных имен во всех СМИ за заданный '
                        'период '
                        'времени')

        elif selected_graph == graph2:
            d1 = {'Собянин': [48, 24, 35]}
            i1 = {"РБК", "Коммерсант", "Известия"}

            barchart_data1 = pd.DataFrame(data=d1, index=i1)

            st.subheader('Количество упоминаний в различных СМИ')
            st.bar_chart(barchart_data1)
            st.markdown('График показывает количество упоминаний выбранных имен в зависимости от СМИ за заданный '
                        'период времени')

        elif selected_graph == graph3:

            d2 = {'Политика': [14, 45, 36], "Экономика": [42, 14, 35], "Происшествия": [14, 9, 26]}
            i2 = {"РБК", "Коммерсант", "Известия"}

            barchart_data2 = pd.DataFrame(data=d2, index=i2)

            st.subheader('Количество упоминаний по тематике')
            st.bar_chart(barchart_data2)
            st.markdown('На графике показано, в какой тематике публиковались материалы с выбранными именами')

        elif selected_graph == graph4:

            linechart_data2 = pd.DataFrame(
                np.random.randn(31, 3),
                columns=['РБК', 'Коммерсант', 'Известия'])

            st.subheader('Количество упоминаний в СМИ за месяц')
            st.line_chart(linechart_data2)
            st.markdown(
                'График показывает, сколько материалов, содержащих заданные имена, выходило каждый день в течение '
                'заданного периода')
