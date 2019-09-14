import argparse
import os
import sys

import pandas as pd
from slacker import Slacker

from slacknalysis.analysis.messages import write_message_analysis
from slacknalysis.analysis.reactions import write_reaction_analysis
from slacknalysis.config import channels, slack_oath
from slacknalysis.data.clean_data import write_cleaned_data
from slacknalysis.data.download_data import (download_all_channel_messages,
                                             download_all_profile_names)


def refresh_data(oath, channels, months):

    """ Grabs X months of data from Slack and formats it for analysis """

    slack = Slacker(oath)

    months = months if months else 6
    download_all_channel_messages(slack, channels, months)
    download_all_profile_names(slack)
    write_cleaned_data()


def analyze_data(users_to_analyze, reactions_to_analyze):
    messages = pd.read_csv('results/cleaned_data/messages.csv')
    profiles = pd.read_csv('results/cleaned_data/profiles.csv')
    reactions = pd.read_csv('results/cleaned_data/reactions.csv')

    write_message_analysis(messages)
    write_reaction_analysis(messages, profiles, reactions, users_to_analyze, reactions_to_analyze)


def _get_root_dir(file):
    return os.path.abspath(file).rsplit('/', 1)[0]


def arg_parser():
    parser = argparse.ArgumentParser(description='Analyze Slack messages and profiles')
    parser.add_argument('--refresh_data', help='Whether to refresh and overwrite raw data from Slack.',
                        action='store_true')
    parser.add_argument('--months', help='How many months of data to poll for from Slack',
                        default=0, type=int)
    parser.add_argument('--users', help='Which users to analyze when looking at user-specific data',
                        nargs='+', default=[])
    parser.add_argument('--reactions', help='Which reaction to analyze when looking at reaction-specific data',
                        nargs='+', default=[])

    return parser

if __name__ == "__main__":
    parser = arg_parser()
    args = parser.parse_args(sys.argv[1:])

    root_dir = _get_root_dir(__file__)
    os.chdir(root_dir)

    if args.refresh_data:
        refresh_data(slack_oath, channels, args.months)

    analyze_data(args.users, args.reactions)
