create extension if not exists pg_trgm;

create table users (
    userid serial primary key,
    username varchar(50) unique not null,
    user_email varchar(255) unique,
    authenticationid varchar(300) unique,
    fname varchar(40),
    lname varchar(60),
    bio varchar(300)
);

create table recipe (
    recipeid serial primary key,
    title varchar(255),
    description varchar(255),
    ingredients text[] not null,
    instructions text[] not null,
    created_on timestamp default now(),
    userid int,
    title_desc tsvector,
    constraint fk_user
        foreign key (userid)
        references users (userid)
        on delete cascade
);

-- Used to search db with full text search
create materialized view recipe_search as
select 
    recipeid,
    title,
    description,
    ingredients,
    instructions,
    to_tsvector('english', title || ' ' || description) as title_desc,
from 
    recipe;

-- Materialized view needs update every insert into recipe
refresh materialized view recipe_search;


create table recipe_like (
    likeid serial primary key,
    like_time timestamp default now(),
    recipeid int,
    userid int,
    constraint fk_recipe
        foreign key (recipeid)
        references recipe (recipeid)
        on delete cascade,
    constraint fk_user
        foreign key (userid)
        references users (userid)
        on delete cascade
);

create table recipe_comment (
    commentid serial primary key,
    comment_time timestamp default now(),
    comment_content varchar(255),
    recipeid int,
    userid int,
    constraint fk_recipe
        foreign key (recipeid)
        references recipe (recipeid)
        on delete cascade,
    constraint fk_user
        foreign key (userid)
        references users (userid)
        on delete cascade
);



create index idx_title_desc on recipe using gin(title_desc);
