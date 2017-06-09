

DROP TABLE adit;

CREATE EXTERNAL TABLE adit(
    user_id STRING,
    item_id STRING,
    rating FLOAT,
    timestamp STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY "\t";

LOAD DATA LOCAL INPATH '/home/public/course/recommendationEngine/u.data' INTO TABLE adit;

WITH 
    rec AS (
    SELECT item_id 
    FROM adit
    WHERE user_id = '2' AND rating > 3),
    similar_users AS (
    SELECT user_id 
    FROM adit AS m, rec AS g
    WHERE m.item_id = g.item_id AND rating > 3 AND m.user_id != "2"
    LIMIT 10)
SELECT item_id 
FROM adit AS m, similar_users AS s
WHERE m.user_id = s.user_id AND rating > 3
LIMIT 5;