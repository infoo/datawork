create database if not exists datawork;
use datawork;
CREATE TABLE IF NOT EXISTS url (
  id  INT AUTO_INCREMENT,
  url VARCHAR(512),
  PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS url_out (
  id        INT PRIMARY KEY AUTO_INCREMENT,
  st_url_id INT,
  ed_url_id INT
);
CREATE TABLE IF NOT EXISTS page (
  id      INT PRIMARY KEY AUTO_INCREMENT,
  url_id  INT,
  content TEXT
);
create table if not exists seg(
  id int primary key auto_increment,
  seg varchar(32)
);