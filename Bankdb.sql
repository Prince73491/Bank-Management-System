CREATE DATABASE bankdb;

USE bankdb;

CREATE TABLE account (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userName VARCHAR(50) NOT NULL,
    userPW VARCHAR(100) NOT NULL,
    balance FLOAT DEFAULT 0
);
Select * from account;
drop database bankdb;
