import pandas as pd
from pandas.io.json import json_normalize
import os


def create_index(reactions):
    
    """ Create stats around how often reactions are used, by whom, and relative standing by user and other reactions """
    
    reactions['total_user_reaction_count'] = reactions.groupby('username')['reaction'] \
                                                      .transform(lambda x: x.count())
    
    reactions['reaction_count'] = reactions.groupby('reaction')['username'] \
                                           .transform(lambda x: x.count())
    
    reactions['user_reaction_count'] = reactions.groupby(['reaction', 'username'])['reaction'] \
                                                .transform(lambda x: x.count())
    
    reactions['total_reaction_count'] = reactions['reaction'].count()
    
    reactions['proportion_of_user_reactions'] = reactions['user_reaction_count'] / reactions['total_user_reaction_count']
    reactions['proportion_of_all_reactions'] = reactions['reaction_count'] / reactions['total_reaction_count']
    reactions['index'] = reactions['proportion_of_user_reactions'] / reactions['proportion_of_all_reactions'] * 100
    
    reactions = reactions.drop('ts', axis=1).drop_duplicates() \
                         .sort_values('index', ascending=False)
    
    return reactions


def most_emotionally_reactive_comments(messages, reactions):
    
    """ Which comments do people react to the most with reactions? """
    
    message_react = messages[['ts', 'username', 'text']].merge(reactions, on='ts', suffixes=('_author', '_reactor'))
    message_react = message_react.groupby(['ts', 'username_author', 'text']) \
                                 .agg(reaction_count=('reaction', 'count'),
                                      reaction_type_count=('reaction', 'nunique'),
                                      reaction_types=('reaction', set))
    
    message_react = message_react.sort_values('reaction_count', ascending=False) \
                                 .reset_index()
    
    return message_react
    

def likelihood_to_use_reaction(reactions, reaction_name, reaction_threshold=5):
    
    """ Who is most/least likely to use a particular reaction? """
    
    reactions = reactions[(reactions['reaction']==reaction_name) & 
                          (reactions['total_user_reaction_count'] >= reaction_threshold)]
    
    cols = ['username', 'user_reaction_count', 'total_user_reaction_count', 'proportion_of_user_reactions', 'index']
    reactions = reactions[cols].drop_duplicates() \
                               .sort_values('index', ascending=False)
    
    return reactions


def most_used_reaction(reactions):
    
    """ What are the most used reactions? """
    
    cols = ['reaction', 'reaction_count', 'proportion_of_all_reactions']
    reactions = reactions[cols].drop_duplicates() \
                               .sort_values('proportion_of_all_reactions', ascending=False)
    
    return reactions


def top_reaction_by_user(reactions, username, reaction_threshold=5, sort_col='index'):
    
    """ What are a user's top reactions?  By index or proportion/count? """
    
    if sort_col not in ('index', 'user_reaction_count', 'proportion_of_user_reactions'):
        raise Exception('sort_col must be index, user_reaction_count, or proportion_of_user_reactions')
    
    reactions = reactions[reactions['username']==username]
    cols = ['reaction', 'user_reaction_count', 'total_user_reaction_count', 'proportion_of_user_reactions', 'index']
    reactions = reactions[cols].drop_duplicates() \
                               .sort_values(sort_col, ascending=False)
    
    return reactions


def write_reaction_analysis(messages, profiles, reactions, users_to_analyze, reactions_to_analyze):

    if not os.path.exists('results/final'):
        os.makedirs('results/final')

    most_emotionally_reactive_comments_df = most_emotionally_reactive_comments(messages, reactions)
    most_emotionally_reactive_comments_df.to_csv('results/final/most_emotionally_reactive_comments.csv', index=False)

    reactions = create_index(reactions)
    reactions.to_csv('results/final/reaction_by_user_index.csv', index=False)

    most_used_reaction_df = most_used_reaction(reactions)
    most_used_reaction_df.to_csv('results/final/most_used_reaction.csv', index=False)

    for user in users_to_analyze:
        top_reaction_by_user_df = top_reaction_by_user(reactions, user)
        top_reaction_by_user_df.to_csv(f"results/final/top_reaction_for_{user.replace('.', ' ')}.csv", index=False)

    for reaction in reactions_to_analyze:
        likelihood_to_use_reaction_df = likelihood_to_use_reaction(reactions, reaction)
        likelihood_to_use_reaction_df.to_csv(f'results/final/likelihood_to_use_{reaction}.csv', index=False)
