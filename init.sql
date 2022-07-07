CREATE DATABASE IF NOT EXISTS userparameters;
USE userparameters;
CREATE TABLE IF NOT EXISTS users(username varchar(40) not null primary key);
CREATE TABLE IF NOT EXISTS parameters(
    parametername varchar(40) not null,
    username varchar(40) not null references users,
    ptype varchar(10) not null,
    value varchar(50) not null,
    primary key(parametername, username, ptype)
); 