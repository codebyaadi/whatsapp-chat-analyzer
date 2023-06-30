from urlextract import URLExtract
from wordcloud import WordCloud
extractor = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':

        df = df[df['user'] == selected_user]

    no_of_msg = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    no_of_words = len(words)

    # Extracting number of media
    no_of_media = df[df['message'].str.contains('<Media omitted>')].shape[0]

    # Extracting number of links
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    no_of_links = len(links)

    return no_of_msg, no_of_words, no_of_media, no_of_links


def most_active_users(df):
    x = df['user'].value_counts().head()
    percent = (df['user'].value_counts() / df.shape[0]) * 100
    df = round(percent, 2).reset_index().rename(columns={'index': 'user', 'user': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':

        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc