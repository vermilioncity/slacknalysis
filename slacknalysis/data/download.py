import json
from slacknalysis.data.models import Channel, User, Message, Reaction, Giphy
import re


def _get_oldest_timestamp(resp):
    """ Grab the oldest message's timestamp in returned payload """

    return float(resp['messages'][-1]['ts'])


def create_mention_regex_map(session):
    """

    Creates a dictionary of terms to replace and their expected replacement.
    Maps the cruft surrounding group mentions and channel mentions with a more sensible @,
    and maps user id mentions with user *name* mentions.

    """
    mention_regex_map = {'<!(?:(\w+))>': r'@\1',  # group mentions
                         '<#\w+\|(?:(\w+))>': r'@\1',  # channel mentions
                         }

    for user in session.query(User):
        mention_regex_map[f'<@{user.id}>'] = f'@{user.name}'

    return mention_regex_map


def replace_mentions(mention_regex_map, text):
    # https://stackoverflow.com/questions/15175142/how-can-i-do-multiple-substitutions-using-regex-in-python
    # this looks so freakin ugly...  i should refactor this to something not gross
    mapped = map(re.escape, mention_regex_map.keys())
    regex = re.compile("(%s)" % "|".join(mapped))

    matches = lambda mo: mention_regex_map[mo.string[mo.start(): mo.end()]]
    text = regex.sub(matches, text)

    return text


def add_message(channel_id, message):

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
    attachment = next(a for a in message['attachments'])
    giphy = Giphy(message_ts=message['ts'],
                  title=attachment['title'],
                  image_url=attachment['image_url'])

    return giphy


def add_reaction(message):
    reactions = []
    for r in message.get('reactions'):
        for user in r['users']:
            reaction = Reaction(message_ts=message['ts'],
                                name=r['name'],
                                user_id=user)

            reactions.append(reaction)

    return reactions


def add_message_data_to_db(response, session, channel_id, mention_regex_map):
    for message in response['messages']:
        if message.get('subtype') != 'message_join':
            message['text'] = replace_mentions(message['text'], mention_regex_map)
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


def download_profile_names(slack, session):
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


def download_messages_from_all_channels(slack, session, start_timestamp, end_timestamp):
    """ Downloads all channel messages """

    mention_regex_map = create_mention_regex_map(session)

    for channel in session.query(Channel):
        download_channel_messages(slack, session, mention_regex_map, channel.id, start_timestamp, end_timestamp)
