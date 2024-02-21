import pytest

from slack_scraper.utils import convert_timestamp_to_est


@pytest.mark.parametrize("timestamp_input,expected", [(1546300800, '2018-12-31 07:00 PM EST'),
                                                      (1572200096, '2019-10-27 02:14 PM EST'),
                                                      (1511679543, '2017-11-26 01:59 AM EST')])
def test_convert_timestamp_to_est(timestamp_input, expected):
    actual = convert_timestamp_to_est(timestamp_input)
    assert actual == expected
