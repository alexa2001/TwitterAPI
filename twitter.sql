CREATE DATABASE twitter_data;

USE twitter_data;

CREATE TABLE user_info(
  username VARCHAR(255) NOT NULL,
  name TEXT default NULL,
  description TEXT default NULL,
  created_at TEXT default NULL,
  pinned_tweet_id INT(11) default NULL,
  id INT(11) default NULL
  PRIMARY KEY (username) 
)



