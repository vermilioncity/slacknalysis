CREATE VIEW response_times AS
SELECT
   ts,
   user_name,
   channel_name,
   (to_timestamp(ts)-LAG(to_timestamp(ts),1) OVER (PARTITION BY channel_id
      ORDER BY ts
   )) response_time,
   LAG(user_name,1) over (PARTITION BY channel_id ORDER BY ts) as previous_user
FROM
   messages;


SELECT user_name AS user_name,
       EXTRACT(EPOCH
               FROM percentile_disc(0.5) within group (
                                                       order by response_time))/60 AS "Median Response Time"
FROM
  (SELECT *
   FROM response_times) AS expr_qry
WHERE previous_user != 'user_name'
  AND ((EXTRACT(EPOCH
                FROM response_time)*1 < 86400))
GROUP BY user_name
HAVING ((count(*) > 5))
ORDER BY "Median Response Time" DESC
LIMIT 20;