import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import altair as alt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # Fetch Unique User
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Analysis for", user_list)

    if st.sidebar.button("Show Analysis"):

        total_messages, total_words, total_media, total_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(total_messages)
        with col2:
            st.header("Total Words")
            st.title(total_words)
        with col3:
            st.header("Total Media")
            st.title(total_media)
        with col4:
            st.header("Total  Links")
            st.title(total_links)

    # Most active user in the group

    if selected_user == 'Overall':
        st.title("Most Active Users")
        active_users, percent_df = helper.most_active_users(df)
        active_users_df = active_users.reset_index().rename(columns={'index': 'user', 0: 'count'})
        chart = alt.Chart(active_users_df).mark_bar().encode(
            x='user',
            y='count'
        )
        st.altair_chart(chart, use_container_width=True)

        st.title("Percent of User's Message")
        st.checkbox("Use container width", value=False, key="use_container_width")
        st.dataframe(percent_df, use_container_width=st.session_state.use_container_width)

    # Generating Word Cloud

    st.title("Word Cloud")
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)