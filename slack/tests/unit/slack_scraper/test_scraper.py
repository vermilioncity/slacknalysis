from unittest.mock import Mock, patch

import pytest

from slack_scraper.scraper import _get_oldest_timestamp, create_mention_regex_map, replace_mentions
from slack_scraper.models import User


@pytest.fixture(scope='function')
def mock_session():
    return Mock()


def test_get_oldest_timestamp():

    response = {'messages': [{'ts': 1511679543.013}, {'ts': 1546300800.01000}, {'ts': 1572200096.093}]}

    actual = _get_oldest_timestamp(response)

    expected = 1572200096.093

    assert actual == expected


@patch('slack_scraper.db.session')
def test_create_mention_regex_map(mock_session):

    u1 = User(id='abc', name='foo')
    u2 = User(id='def', name='bar')

    mock_session.query.return_value = [u1, u2]

    actual = create_mention_regex_map(mock_session)

    expected = {r'<!(?:(\w+))>': r'@\1',  # group mentions
                r'<#\w+\|(?:(\w+))>': r'@\1',  # channel mentions
                r'<@abc>': '@foo',
                r'<@def>': '@bar'
                }

    assert actual == expected


@pytest.mark.parametrize("input,expected", [(1546300800, '2018-12-31 07:00 PM EST'),
                                            (1572200096, '2019-10-27 02:14 PM EST'),
                                            (1511679543, '2017-11-26 01:59 AM EST')])
def test_replace_mentions(input, expected):
    mention_regex_map = {r'<!(?:(\w+))>': r'@\1',  # group mentions
                         r'<#\w+\|(?:(\w+))>': r'@\1',  # channel mentions
                         r'<@abc>': '@foo',
                         r'<@def>': '@bar'
                        }

    actual = replace_mentions(mention_regex_map, input)

    assert False
    assert actual == expected


def test_add_message():
    assert False


def test_add_giphy():
    assert False


def test_add_reaction():
    assert False


def test_add_message_data_to_db():
    assert False


def test_download_channel_messages():
    assert False


def test_download_users():
    assert False


def test_validate_timestamp_type():
    assert False


def test_validate_start_timestamp():
    assert False
