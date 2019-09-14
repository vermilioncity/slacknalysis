import pandas as pd

def chattiest(df):
    
    """ Who sends the most messages? """
    
    df['sent_messages'] = df.groupby('username')['ts'].transform('count')
    df['percent_of_all_messages_sent'] = df['sent_messages'] / df['sent_messages'].count()
    df['percent_rank'] = df['sent_messages'].rank(pct=True)
    df = df.sort_values('percent_rank', ascending=False)

    df = df[['username', 'sent_messages', 'percent_of_all_messages_sent', 'percent_rank']].drop_duplicates()
    
    return df


def most_verbose(df, sent_messages_threshold=5):
    
    """ Who writes the most per message? """
    
    df = df[['username', 'text', 'sent_messages']].copy(deep=True)
    df = df[df['sent_messages']>=sent_messages_threshold]
    
    df['tokenized_text'] = df['text'].str.split()
    df['message_length'] = df['tokenized_text'].apply(len)
    df['average_message_length'] = df['message_length'].apply('median')
    
    df = df.groupby(['username', 'average_message_length', 'sent_messages'], as_index=False)['message_length'].median() \
           .sort_values('message_length', ascending=False)
    
    df['index'] = df['message_length']/df['average_message_length']*100
    
    return df

def most_replied_comments(df):
    
    """ Which comments generated the most discussion? """
    
    df = df[['username', 'text', 'reply_count']].sort_values('reply_count', ascending=False)
    return df

def most_reply_authors(df):
    
    """ Which messages elicited commentary from the most people? """
    
    df = df[['username', 'text', 'reply_users_count']].sort_values('reply_users_count', ascending=False)
    
    return df