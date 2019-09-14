import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from slacker import Slacker


def _months_ago(months=3):
    """ Get timestamp of some date in the past """

    date = datetime.today() - relativedelta(months=months)
    return date.timestamp()


def _get_oldest_timestamp(resp):
    """ Grab the oldest message's timestamp in returned payload """

    return float(resp['messages'][-1]['ts'])


def save_file(obj, directory, filename):
    """ Save file to a given location as json """

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)

    with open(file_path, 'w') as f:
        print(f'Saving results to {file_path}')
        json.dump(obj, f, indent=4, separators=(',', ': '))


def get_channel_messages(slack, channel_id, months=3):
    """ Repeatedly que for messages up until a certain date"""

    latest_timestamp = datetime.now().timestamp()
    oldest_timestamp = _months_ago(months)

    while latest_timestamp >= oldest_timestamp:
        response = slack.channels.history(
            channel_id, count=1000, latest=latest_timestamp, inclusive=False)
        response = json.loads(response.raw)

        if not response['ok']:
            raise Exception(response)

        yield response['messages']

        if response['has_more']:
            latest_timestamp = _get_oldest_timestamp(response)
            continue

        else:
            break


def download_all_profile_names(slack):
    """ Queries for all users in workspace """

    response = slack.users.list()
    response = json.loads(response.raw)

    if not response['ok']:
        raise Exception(response)

    profiles = {}
    for member in response['members']:
        id = member['id']
        name = member['name']
        profiles[id] = name

    save_file(profiles, 'results/raw/profiles', 'profiles.json')


def download_all_channel_messages(slack, channels, months=3):
    """ Downloads all channel messages """

    for channel_name, channel_id in channels.items():
        print(f'Querying {channel_name}...')

        for number, response in enumerate(get_channel_messages(slack, channel_id, months)):
            filename = f'{channel_name}_{number}.json'

            save_file(response, 'results/raw/messages', filename)
