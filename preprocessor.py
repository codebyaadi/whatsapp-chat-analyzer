import re
import pandas as pd


def preprocess(data):
    # Creating a regular expression which will help in extracting data
    pattern = '\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'

    # Extraction of data
    messages = re.split(pattern, data)[1:]  # Message extraction
    dates = re.findall(pattern, data)  # Extracting date from data
    dates = [date.replace('\u202f', ' ') for date in dates]  # Remove \u202f character

    # Creating Panda Dataframe
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate user and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
