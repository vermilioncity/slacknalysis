import json
import os

import pandas as pd
from pandas.io.json import json_normalize

from slacknalysis.analysis import messages, reactions


def read_profile_data():
    full_path = os.path.join('results/raw/profiles', 'profiles.json')
    with open(full_path) as f:
        r = json.load(f)
        
    profiles = pd.DataFrame.from_dict(r, orient='index', columns=['username']) \
                           .reset_index() \
                           .rename(columns={'index': 'user'})

    return profiles


def read_message_data():
    messages = pd.DataFrame()
    for file in os.listdir('results/raw/messages'):
        if file.endswith('.json'):
            full_path = os.path.join('results/raw/messages', file)
            tmp = pd.read_json(full_path)
            messages = pd.concat([messages, tmp], ignore_index=True)
            
    return messages


def _replace_mentions(df, profiles):

    """ Remove @s because they appear as the user id and not username, hampering legibility """

    replacements = {'<!(?:(\w+))>': r'@\1',  # group mentions
                    '<#\w+\|(?:(\w+))>': r'@\1', # channel mentions
                    }

    for row in profiles.itertuples():
        mention = f'<@{row.user}>'
        replacements[mention] = f'@{row.username}'

    df = df.replace(replacements, regex=True)

    return df


def clean_messages(message, profiles):

    """ Remove non-messages and drop unwanted columns """
    
    message = message[(~message['subtype'].isin(['bot_message', 'tombstone', 'message_join'])) & (message['text']!='')]
    message = message[['ts', 'user', 'text', 'reactions', 'reply_count', 'reply_users_count']]
    
    countable_cols = ['reply_count', 'reply_users_count']
    message[countable_cols] = message[countable_cols].fillna(0)

    df = message.merge(profiles, on='user') \
                .drop('user', axis=1)

    df = _replace_mentions(df, profiles)
    
    return df


def clean_reactions(messages, profiles):

    """ Reshape nested reactions blob into something usable """

    reactions = messages[['ts', 'reactions']].dropna(subset=['reactions'])

    master_reactions = pd.DataFrame()
    for _, col in reactions.iterrows():
        tmp = json_normalize(col['reactions'])
        tmp['ts'] = col['ts']
        master_reactions = pd.concat([master_reactions, tmp], ignore_index=True)
    
    master_reactions = master_reactions.explode('users') \
                                       .drop('count', axis=1) \
                                       .rename(columns={'name': 'reaction', 'users': 'user'})

    master_reactions = master_reactions.merge(profiles, on='user') \
                                       .drop('user', axis=1)
    
    return master_reactions


def write_cleaned_data():
    profiles_df = read_profile_data()
    messages_df = read_message_data()
    messages_df = clean_messages(messages_df, profiles_df)
    reactions_df = clean_reactions(messages_df, profiles_df)

    if not os.path.exists('results/cleaned_data'):
        os.makedirs('results/cleaned_data')

    profiles_df.to_csv('results/cleaned_data/profiles.csv', index=False)
    messages_df.to_csv('results/cleaned_data/messages.csv', index=False)
    reactions_df.to_csv('results/cleaned_data/reactions.csv', index=False)
