CREATE VIEW reaction_to_message AS
SELECT
SELECT
  ts,
  channel_name,
  messages.user_name as author,
  reactions.user_name,
  reaction_name
FROM messages
LEFT JOIN reactions on messages.ts = reactions.message_ts;

SELECT
reaction_to_message.*,
message_count
FROM reaction_to_message
INNER JOIN (SELECT DISTINCT count(ts) as message_count, user_name
            FROM messages
            GROUP BY user_name) as msg
on msg.user_name = reaction_to_message.user_name;
