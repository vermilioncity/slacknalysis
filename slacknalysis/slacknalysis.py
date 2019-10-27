import argparse
import os
import sys

from slacker import Slacker
import arrow

from slacknalysis.data.db import session
from slacknalysis.data.download import (download_messages_from_all_channels,
                                        download_profile_names)


def arg_parser():

    to_date = lambda x: arrow.get(x).timestamp

    parser = argparse.ArgumentParser(description='Analyze Slack messages and profiles')
    parser.add_argument('--start_date', help='Start date of analysis', type=to_date)
    parser.add_argument('--end_date', help='End date of analysis', type=to_date)

    return parser


if __name__ == "__main__":
    parser = arg_parser()
    args = parser.parse_args(sys.argv[1:])

    slack = Slacker(os.getenv('VERIFICATION_TOKEN'))
    download_profile_names(slack, session)
    download_messages_from_all_channels(slack, session, args.start_date, args.end_date)

