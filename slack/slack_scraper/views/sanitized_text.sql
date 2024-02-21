CREATE VIEW sanitized_text 
AS 
  SELECT ts,
                           channel_id,
                         channel_name,
                         user_id,
                         user_name,
         Trim(text) AS text
  FROM   (SELECT ts,
                           channel_id,
                         channel_name,
                         user_id,
                         user_name,
                 REGEXP_REPLACE(text, '[^A-Za-z?!.\s\d'']', '', 'g') AS text
          FROM   (SELECT ts,
                                   channel_id,
                         channel_name,
                         user_id,
                         user_name,
                         REGEXP_REPLACE(text, '…', '...', 'g') AS text
                  FROM   (SELECT ts,
                                           channel_id,
                         channel_name,
                         user_id,
                         user_name,
                                 REGEXP_REPLACE(text, '\:\w+\:', '', 'g') AS
                                 text
                          FROM   (SELECT ts,
                                                   channel_id,
                         channel_name,
                         user_id,
                         user_name,
                                         REGEXP_REPLACE(text, '(@[a-z]+\.[a-z]+(\.[a-z]+)?)|(\<\!here\>)', '', 'g') AS
                         text -- @first.last or here mentions 
                                  FROM   messages) AS mentions) AS reactions) AS 
                 ellipses 
         ) AS alphanumeric;