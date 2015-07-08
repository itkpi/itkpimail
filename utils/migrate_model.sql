== Migrating from default user model to custom ==

1) Dump DB (just in case)
2) Make initial migration with custom User model (Model should be called only User,
not CustomUser or anything else to not break relation names) that has Meta: db_table='auth_user'
3) Push code to heroku
4) Run manage.py migrate --fake-initial
so that now django thinks that we had custom user model from the beginning
5) Alter User table

\d auth_user
    Column    |           Type           |                       Modifiers
--------------+--------------------------+--------------------------------------------------------
 id           | integer                  | not null default nextval('auth_user_id_seq'::regclass)
 password     | character varying(128)   | not null
 last_login   | timestamp with time zone |
 is_superuser | boolean                  | not null
 username     | character varying(30)    | not null
 first_name   | character varying(30)    | not null
 last_name    | character varying(30)    | not null
 email        | character varying(254)   | not null
 is_staff     | boolean                  | not null
 is_active    | boolean                  | not null
 date_joined  | timestamp with time zone | not null


itkpi::RED=> ALTER TABLE auth_user ADD COLUMN is_supreme boolean NOT NULL DEFAULT false;
