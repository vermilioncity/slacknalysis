from pandas.io.json import json_normalize
import pandas as pd
import json
import os

from slacknalysis import message_analysis
from slacknalysis import reactions_analysis


def read_profile_data(path):
    full_path = os.path.join(path, 'profiles.json')
    with open(full_path) as f:
        r = json.load(f)
        
    profiles = pd.DataFrame.from_dict(r, orient='index', columns=['username']) \
                           .reset_index() \
                           .rename(columns={'index': 'user'})

    return profiles


def read_channel_data(path):
    channel = pd.DataFrame()
    for file in os.listdir(path):
        if file.endswith('.json'):
            full_path = os.path.join(path, file)
            tmp = pd.read_json(full_path)
            channel = pd.concat([channel, tmp], ignore_index=True)
            
    return channel


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


def clean_data(channel, profiles):

    """ Remove non-messages and drop unwanted columns """
    
    channel = channel[(~channel['subtype'].isin(['bot_message', 'tombstone', 'channel_join'])) & (channel['text']!='')]
    channel = channel[['ts', 'user', 'text', 'reactions', 'reply_count', 'reply_users_count']]
    
    countable_cols = ['reply_count', 'reply_users_count']
    channel[countable_cols] = channel[countable_cols].fillna(0)

    df = channel.merge(profiles, on='user') \
                .drop('user', axis=1)

    df = _replace_mentions(df, profiles)
    
    return df


def write_results(filename, func, **kwargs):
    filename = os.path.join('analysis', f'{filename}.csv')
    df = func(**kwargs)
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    channels = read_channel_data('results')
    profiles = read_profile_data('profiles')
    df = clean_data(channels, profiles)

    write_results('chattiest', message_analysis.chattiest, df=df)
    write_results('most_verbose', message_analysis.most_verbose, df=df)
    write_results('most_replied_comments', message_analysis.most_replied_comments, df=df)
    write_results('most_reply_authors', message_analysis.most_reply_authors, df=df)

    reactions = reactions_analysis.parse_reactions(df, profiles)
    write_results('most_emotionally_reactive_comments', reactions_analysis.most_emotionally_reactive_comments,
                  messages=df, reactions=reactions)

    reactions = reactions_analysis.create_index(reactions)
    
    write_results('likelihood_to_use_reaction',
                  reactions_analysis.likelihood_to_use_reaction, reactions=reactions,
                  reaction_name='joy')

    write_results('most_used_reaction', reactions_analysis.most_used_reaction, reactions=reactions)
    write_results('top_reaction_by_user', reactions_analysis.top_reaction_by_user, reactions=reactions,
                  username='rebecca.bruehlman')

    write_results('top_reaction_by_user', reactions_analysis.top_reaction_by_user,
                  reactions=reactions, username='rebecca.bruehlman')