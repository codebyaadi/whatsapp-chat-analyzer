def fetch_stats(selected_user, df):

    if selected_user != 'Overall':

        df = df[df['user'] == selected_user]

    no_of_msg = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    no_of_words = len(words)
    return no_of_msg, no_of_words
