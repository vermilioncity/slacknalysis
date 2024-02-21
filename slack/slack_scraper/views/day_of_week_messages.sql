CREATE VIEW day_of_week_messages AS
SELECT ts,
extract(dow from to_timestamp(ts)) ||' - '|| to_char(to_timestamp(ts), 'day') as day_of_week,
to_char(to_timestamp(ts) at time zone 'US/Eastern', 'HH24:00') as hour_of_day,
user_name,
channel_name
FROM messages;