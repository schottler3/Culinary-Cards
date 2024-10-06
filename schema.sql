create table users (
    user_email varchar(255) primary key,
    fname varchar(40),
    lname varchar(60),
    bio varchar(300)
);

create table recipe (
    recipe_id serial primary key,
    description varchar(255),
    ingredients text[] not null,
    instructions text[] not null,
    created_on timestamp default now(),
    user_email varchar(255),
    constraint fk_user
        foreign key (user_email)
        references users (user_email)
        on delete cascade
);

create table recipe_like (
    likeid serial primary key,
    like_time timestamp default now(),
    recipe_id int,
    user_email varchar(255),
    constraint fk_recipe
        foreign key (recipe_id)
        references recipe (recipe_id),
    constraint fk_user
        foreign key (user_email)
        references users (user_email)
);
