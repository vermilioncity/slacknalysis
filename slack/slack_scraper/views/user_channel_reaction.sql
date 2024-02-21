CREATE VIEW user_channel_reaction AS
SELECT
  ts,
  channel_name,
  reactions.user_name,
  reaction_name
FROM reactions
INNER JOIN messages on messages.ts = reactions.message_ts;