from urlextract import URLExtract
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
