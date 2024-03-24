create table users.builder
(
    builder_id   serial
        constraint builder_pk
            primary key,
    builder_name text not null
);

alter table users.builder
    owner to root;

create table events.buildings
(
    event_id   serial
        constraint buildings_pk
            primary key,
    builder_id integer               not null
        constraint buildings_builder_builder_id_fk
            references users.builder
            on update cascade on delete cascade,
    has_built  boolean default false not null,
    last_date  timestamp
);

alter table events.buildings
    owner to root;

create table users.user_info
(
    id           serial
        constraint user_info_pk
            primary key,
    name         text not null,
    general_info json not null,
    address      text,
    post_address text,
    meta_info    json,
    user_type    text not null
);

comment on column users.user_info.name is 'ФИО/Наименование';

comment on column users.user_info.general_info is 'Паспортные данные/Инфо о компании';

alter table users.user_info
    owner to root;

create table users.payments
(
    id       serial
        constraint payments_pk
            primary key,
    user_id  integer
        constraint payments_user_info_id_fk
            references users.user_info
            on update cascade on delete cascade,
    money    double precision not null,
    event_id integer
        constraint payments_buildings_event_id_fk
            references events.buildings
            on update cascade on delete cascade
);

alter table users.payments
    owner to root;

create table platform.roles
(
    role_id   serial
        constraint roles_pk
            primary key,
    role_name text not null
);

alter table platform.roles
    owner to root;

create table platform.user_info
(
    login     text not null
        constraint user_info_pk
            unique,
    password  text not null,
    user_role integer
        constraint user_info_roles_role_id_fk
            references platform.roles
            on update cascade on delete cascade,
    user_id   serial
        constraint user_info_pk_2
            primary key
);

alter table platform.user_info
    owner to root;

create view platform.user_with_roles(login, user_id, password, user_role, role_id, role_name) as
SELECT user_info.login,
       user_info.user_id,
       user_info.password,
       user_info.user_role,
       r.role_id,
       r.role_name
FROM platform.user_info
         LEFT JOIN platform.roles r ON r.role_id = user_info.user_role;

alter table platform.user_with_roles
    owner to root;

create view users.users_with_events
            (user_id, money, name, general_info, address, post_address, meta_info, user_type, builder_id, has_built,
             last_date) as
SELECT pay.user_id,
       pay.money,
       ui.name,
       ui.general_info,
       ui.address,
       ui.post_address,
       ui.meta_info,
       ui.user_type,
       bu.builder_id,
       bu.has_built,
       bu.last_date
FROM users.payments pay
         LEFT JOIN users.user_info ui ON ui.id = pay.user_id
         LEFT JOIN events.buildings bu ON pay.event_id = bu.event_id;

alter table users.users_with_events
    owner to root;

