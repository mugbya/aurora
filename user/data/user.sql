CREATE DATABASE  ull_user

CREATE TABLE public."user"
(
    id SERIAL PRIMARY KEY,
    username VARCHAR(30),
    nickname VARCHAR(30),
    password VARCHAR(50),
    email VARCHAR(100)
);




