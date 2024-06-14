-- migrate:up

create extension if not exists "uuid-ossp";

drop table if exists reciept_site.reciepts cascade;
drop schema if exists reciept_site cascade;
create schema reciept_site;


create table reciept_site.reciepts
(
    id uuid primary key default uuid_generate_v4(),
    name text,
    description text,
    products text
);


insert into reciept_site.reciepts(name, description, products) values
  ('test_soup', 'test', 'meat, pasta, potatoes, onions'),
  ('test_bolonyeze', 'test', 'pasta, minced meat, tomato sauce');


-- migrate:down