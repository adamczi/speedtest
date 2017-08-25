create table users(
id serial primary key not null,
name char(50) unique not null,
password text not null,
api char(24) unique not null);


create table data(
id serial primary key not null,
datetime timestamp not null,
download numeric(6,3) default 0.0,
upload numeric(6,3) default 0.0,
ping numeric(8,3) default 0.0,
api char(24) references users(api));

