import pandas as pd
import os


def chattiest(messages):
    
    """ Who sends the most messages? """
    
    messages['sent_messages'] = messages.groupby('username')['ts'].transform('count')
    messages['percent_of_all_messages_sent'] = messages['sent_messages'] / messages['sent_messages'].count()
    messages['percent_rank'] = messages['sent_messages'].rank(pct=True)
    messages = messages.sort_values('percent_rank', ascending=False)

    messages = messages[['username', 'sent_messages',
                         'percent_of_all_messages_sent', 'percent_rank']].drop_duplicates()
    
    return messages


def most_verbose(messages, sent_messages_threshold=5):
    
    """ Who writes the most per message? """
    
    messages = messages[['username', 'text', 'sent_messages']].copy(deep=True)
    messages = messages[messages['sent_messages']>=sent_messages_threshold]
    
    messages['tokenized_text'] = messages['text'].str.split()
    messages['message_length'] = messages['tokenized_text'].apply(len)
    messages['average_message_length'] = messages['message_length'].apply('median')
    
    messages = messages.groupby(['username', 'average_message_length', 'sent_messages'],
                                 as_index=False)['message_length'].median() \
                       .sort_values('message_length', ascending=False)
    
    messages['index'] = messages['message_length']/messages['average_message_length']*100
    
    return messages


def most_replied_comments(messages):
    
    """ Which comments generated the most discussion? """
    
    messages = messages[['username', 'text', 'reply_count']].sort_values('reply_count', ascending=False)
    return messages


def most_replied_authors(messages):
    
    """ Which messages elicited commentary from the most people? """
    
    messages = messages[['username', 'text', 'reply_users_count']].sort_values('reply_users_count', ascending=False)
    
    return messages


def write_message_analysis(messages):

    if not os.path.exists('results/final'):
        os.mkdir('results/final')

    chattiest_df = chattiest(messages)
    chattiest_df.to_csv('results/final/chattiest.csv', index=False)

    most_verbose_df = most_verbose(messages)
    most_verbose_df.to_csv('results/final/most_verbose.csv', index=False)

    most_replied_comments_df = most_replied_comments(messages)
    most_replied_comments_df.to_csv('results/final/most_replied_comments.csv', index=False)
    
    most_replied_authors_df = most_replied_authors(messages)
    most_replied_authors_df.to_csv('results/final/most_replied_authors.csv', index=False)
