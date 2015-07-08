== Migrating from default user model to custom ==

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
