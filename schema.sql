CREATE TABLE user(
    user_email varchar(255) primary key,
    Fname varchar(40),
    Lname varchar(60),
    bio varchar(300)
);

CREATE TABLE recipe(
    recipe_id serial primary key,
    description varchar(255);
    ingredients text[] not null,
    instructions text[] not null,
    created_on timestamp default NOW(),
    constraint fk_user
        foreign key (user_email)
        references user (user_email)
        on delete cascade
);

create table recipe_like(
    likeID serial primary key,
    like_time timestamp default NOW(),
    constraint fk_like
    foreign key (recipe_id) references recipe(recipe_id)
    foreign key (user_email) references user(user_email)
);