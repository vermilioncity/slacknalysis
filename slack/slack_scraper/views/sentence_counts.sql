CREATE VIEW sentence_counts AS
SELECT     ts,
           channel_id,
           channel_name,
           user_id,
           user_name,
           punctuation.text,
           CARDINALITY(ARRAY_REMOVE(tokenized_sentences, '')) AS sentence_count
FROM       (
                  SELECT ts,
                         channel_id,
                         channel_name,
                         user_id,
                         user_name,
                         text,
                         regexp_split_to_array(text, e'[?!.]+') AS tokenized_sentences
                  FROM   sanitized_text) AS punctuation
WHERE CARDINALITY(ARRAY_REMOVE(tokenized_sentences, '')) > 0;