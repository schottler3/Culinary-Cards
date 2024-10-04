create extension if not exists pg_trgm;

create table users (
    userid serial primary key,
    username varchar(50) unique not null,
    user_email varchar(255) unique not null,
    fname varchar(40),
    lname varchar(60),
    bio varchar(300)
);

create table recipe (
    recipe_id serial primary key,
    title varchar(255),
    description varchar(255),
    ingredients text[] not null,
    instructions text[] not null,
    created_on timestamp default now(),
    user_email varchar(255),
    title_description_tsv tsvector,
    ingredients_tsv tsvector,
    instructions_tsv tsvector,
    constraint fk_user
        foreign key (user_email)
        references users (user_email)
        on delete cascade
);

-- Used to search db with full text search
create materialized view recipe_search as
select 
    recipe_id,
    title,
    description,
    ingredients,
    instructions,
    to_tsvector('english', title || ' ' || description) as title_description_tsv,
    to_tsvector('english', array_to_string(ingredients, ' ')) as ingredients_tsv,
    to_tsvector('english', array_to_string(instructions, ' ')) as instructions_tsv
from 
    recipe;

-- Materialized view needs update every insert into recipe
refresh materialized view recipe_search;


create table recipe_like (
    likeid serial primary key,
    like_time timestamp default now(),
    recipe_id int,
    user_email varchar(255),
    constraint fk_recipe
        foreign key (recipe_id)
        references recipe (recipe_id)
        on delete cascade,
    constraint fk_user
        foreign key (user_email)
        references users (user_email)
        on delete cascade
);

create table recipe_comment (
    commentid serial primary key,
    comment_time timestamp default now(),
    recipe_id int,
    user_email varchar(255),
    constraint fk_recipe
        foreign key (recipe_id)
        references recipe (recipe_id)
        on delete cascade,
    constraint fk_user
        foreign key (user_email)
        references users (user_email)
        on delete cascade
);



create index idx_title_description_tsv on recipe using gin(title_description_tsv);
create index idx_ingredients_tsv on recipe using gin(ingredients_tsv);
create index idx_instructions_tsv on recipe using gin(instructions_tsv);
