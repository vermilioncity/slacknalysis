import arrow


def _six_months_ago():
    """ Get timestamp of some date in the past """

    date = arrow.utcnow().shift(months=-6)
    return date.timestamp


def convert_timestamp_to_est(timestamp):
    dt = arrow.get(float(timestamp)) \
              .to('US/Eastern') \
              .strftime('%Y-%m-%d %I:%m %p EST')

    return dt
