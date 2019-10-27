import arrow


def convert_timestamp_to_est(timestamp):

    """

    Converts a timestamp into nice 12-hour timestamp with EST.  Yeah, yeah, UTC is 'standard'...  but
    EST/EDT is more reader-friendly in my brain.

    I'd never be a savage who stored 12-hour EST/EDT in a database anyway.  Come on, now.

    """

    dt = arrow.get(float(timestamp)) \
              .to('US/Eastern') \
              .strftime('%Y-%m-%d %I:%M %p EST')

    return dt
