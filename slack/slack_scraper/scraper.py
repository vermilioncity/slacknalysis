import json
import re

from sqlalchemy import func, select
import arrow

from slack_scraper.models import Channel, User, Message, Reaction, Giphy
from slack_scraper.utils import convert_timestamp_to_est


def _get_oldest_timestamp(resp):

    """ Grab the oldest message's timestamp in returned payload """

    return float(resp['messages'][-1]['ts'])


def create_mention_regex_map(session):

    """

    Creates a dictionary of terms to replace and their expected replacement.
    Maps the cruft surrounding group mentions and channel mentions with a more sensible @,
    and maps user id mentions with user *name* mentions.

    """

    mention_regex_map = {r'<!(?:(\w+))>': r'@\1',  # group mentions
                         r'<#\w+\|(?:(\w+))>': r'@\1',  # channel mentions
                         }

    for user in session.query(User):
        mention_regex_map[f'<@{user.id}>'] = f'@{user.name}'

    return mention_regex_map


def replace_mentions(mention_regex_map, text):

    """

    https://stackoverflow.com/questions/15175142/how-can-i-do-multiple-substitutions-using-regex-in-python

    Replaces a map of regex expressions for a given string.

    this looks so freakin ugly...  i should refactor this to something not gross

    """

    mapped = map(re.escape, mention_regex_map.keys())
    regex = re.compile("(%s)" % "|".join(mapped))

    matches = lambda mo: mention_regex_map[mo.string[mo.start(): mo.end()]]
    text = regex.sub(matches, text)

    return text


def add_message(channel_id, message):

    """ Extracts a given message's slack into a Message instance """

    m = Message(channel_id=channel_id,
                ts=message.get('ts'),
                user_id=message.get('user'),
                text=message.get('text'),
                thread_ts=message.get('thread_ts'),
                reply_count=message.get('reply_count', 0),
                reply_users_count=message.get('reply_users_count', 0)
                )

    return m


def add_giphy(message):

    """ Extracts each giphy's metadata for a given message """

    attachment = next(a for a in message['attachments'])
    giphy = Giphy(message_ts=message['ts'],
                  title=attachment['title'],
                  image_url=attachment['image_url'])

    return giphy


def add_reaction(message):

    """ Extracts each reaction by user for a given message """

    reactions = []
    for r in message.get('reactions'):
        for user in r['users']:
            reaction = Reaction(message_ts=message['ts'],
                                name=r['name'],
                                user_id=user)

            reactions.append(reaction)

    return reactions


def add_message_data_to_db(response, session, channel_id, mention_regex_map):

    """ For each message, update associated tables with requisite slack """

    for message in response['messages']:
        if message.get('subtype') != 'message_join':
            message['text'] = replace_mentions(mention_regex_map, message['text'])
            m = add_message(channel_id, message)
            session.add(m)
            session.flush()

            if message.get('bot_id') == 'B0G5DMLRE':  # giphy!!!!
                giphy = add_giphy(message)
                session.add(giphy)

            if message.get('reactions'):
                reactions = add_reaction(message)
                session.add_all(reactions)

    return session


def download_channel_messages(slack, session, channel_id, mention_regex_map, start_timestamp, end_timestamp):

    """ Repeatedly request messages up until a certain date"""

    latest_timestamp = end_timestamp

    while latest_timestamp >= start_timestamp:
        response = slack.channels.history(channel_id, count=1000, oldest=start_timestamp, latest=latest_timestamp)
        response = json.loads(response.raw)

        if not response['ok']:
            raise Exception(response)

        session = add_message_data_to_db(response, session, channel_id, mention_regex_map)

        if response['has_more']:
            latest_timestamp = _get_oldest_timestamp(response)
            continue

        else:
            session.commit()
            break


def download_users(slack, session):

    """ Queries for all users in workspace """

    response = slack.users.list()
    response = json.loads(response.raw)

    if not response['ok']:
        raise Exception(response)

    for member in response['members']:
        existing_user = session.query(User).filter_by(id=member['id']).first()
        if not existing_user:
            user = User(id=member['id'], name=member['name'])
            session.add(user)

    session.commit()


def validate_timestamp_type(date):

    """ Ensure date is either a timestamp or a format that can be converted into a timestamp """

    try:
        timestamp = float(date)
    except TypeError:
        try:
            timestamp = arrow.get(date).timestamp
        except arrow.parser.ParserError:
            raise TypeError('Was expecting a timestamp or valid time format')

    return timestamp


def validate_start_timestamp(session, start_timestamp):

    """
    Ensures that the supplied start timestamp is not inclusive of already-queried messages.
    Updates to the most recent timestamp if so.

    """

    latest_timestamp = session.query(func.max(Message.ts)).first()[0]

    if latest_timestamp and start_timestamp < latest_timestamp:

        print(f'There is already slack present for messages prior to {convert_timestamp_to_est(start_timestamp)}'
              f'...  updating start_timestamp to {convert_timestamp_to_est(latest_timestamp)}...')

        latest_timestamp = float(latest_timestamp) + 0.01  # add tenth of a second to avoid requerying the last message
        return latest_timestamp

    else:
        return start_timestamp


def download_messages_from_all_channels(slack, session, start_timestamp, end_timestamp):

    """ Validates dates and downloads all channel messages """

    start_timestamp = validate_timestamp_type(start_timestamp)
    end_timestamp = validate_timestamp_type(end_timestamp)

    start_timestamp = validate_start_timestamp(session, start_timestamp)

    mention_regex_map = create_mention_regex_map(session)

    for channel in session.query(Channel):
        print(f'Querying {channel.name}...')
        download_channel_messages(slack, session, channel.id, mention_regex_map, start_timestamp, end_timestamp)
