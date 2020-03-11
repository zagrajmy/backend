CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;
CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;
CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;
CREATE TABLE public.cr_user (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean DEFAULT false NOT NULL,
    first_name character varying,
    last_name character varying,
    email character varying(254) NOT NULL,
    is_staff boolean DEFAULT false NOT NULL,
    is_active boolean DEFAULT false NOT NULL,
    date_joined timestamp with time zone DEFAULT now() NOT NULL,
    uuid uuid DEFAULT public.gen_random_uuid() NOT NULL,
    username character varying(255) NOT NULL
);
CREATE TABLE public.cr_user_groups (
    id integer NOT NULL,
    user_id uuid NOT NULL,
    group_id integer NOT NULL
);
CREATE SEQUENCE public.cr_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.cr_user_groups_id_seq OWNED BY public.cr_user_groups.id;
CREATE TABLE public.cr_user_user_permissions (
    id integer NOT NULL,
    user_id uuid NOT NULL,
    permission_id integer NOT NULL
);
CREATE SEQUENCE public.cr_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.cr_user_user_permissions_id_seq OWNED BY public.cr_user_user_permissions.id;
CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id uuid NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;
CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;
CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;
CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
CREATE TABLE public.nb_guild (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    sphere_id integer NOT NULL
);
CREATE SEQUENCE public.nb_guild_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.nb_guild_id_seq OWNED BY public.nb_guild.id;
CREATE TABLE public.nb_guild_user (
    id integer NOT NULL,
    membership_type character varying(31) NOT NULL,
    guild_id integer NOT NULL,
    user_id uuid NOT NULL
);
CREATE SEQUENCE public.nb_guild_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.nb_guild_user_id_seq OWNED BY public.nb_guild_user.id;
CREATE TABLE public.nb_meeting (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    start_time timestamp with time zone,
    end_time timestamp with time zone,
    publication_time timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    location text,
    guild_id integer NOT NULL,
    organizer_id uuid NOT NULL
);
CREATE SEQUENCE public.nb_meeting_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.nb_meeting_id_seq OWNED BY public.nb_meeting.id;
CREATE TABLE public.nb_meeting_user (
    id integer NOT NULL,
    status character varying(31) NOT NULL,
    meeting_id integer NOT NULL,
    user_id uuid NOT NULL
);
CREATE SEQUENCE public.nb_meeting_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.nb_meeting_user_id_seq OWNED BY public.nb_meeting_user.id;
CREATE TABLE public.nb_sphere (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);
CREATE SEQUENCE public.nb_sphere_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.nb_sphere_id_seq OWNED BY public.nb_sphere.id;
CREATE TABLE public.nb_sphere_users (
    id integer NOT NULL,
    sphere_id integer NOT NULL,
    user_id uuid NOT NULL
);
CREATE SEQUENCE public.nb_sphere_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.nb_sphere_users_id_seq OWNED BY public.nb_sphere_users.id;
ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);
ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);
ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);
ALTER TABLE ONLY public.cr_user_groups ALTER COLUMN id SET DEFAULT nextval('public.cr_user_groups_id_seq'::regclass);
ALTER TABLE ONLY public.cr_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.cr_user_user_permissions_id_seq'::regclass);
ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);
ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);
ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);
ALTER TABLE ONLY public.nb_guild ALTER COLUMN id SET DEFAULT nextval('public.nb_guild_id_seq'::regclass);
ALTER TABLE ONLY public.nb_guild_user ALTER COLUMN id SET DEFAULT nextval('public.nb_guild_user_id_seq'::regclass);
ALTER TABLE ONLY public.nb_meeting ALTER COLUMN id SET DEFAULT nextval('public.nb_meeting_id_seq'::regclass);
ALTER TABLE ONLY public.nb_meeting_user ALTER COLUMN id SET DEFAULT nextval('public.nb_meeting_user_id_seq'::regclass);
ALTER TABLE ONLY public.nb_sphere ALTER COLUMN id SET DEFAULT nextval('public.nb_sphere_id_seq'::regclass);
ALTER TABLE ONLY public.nb_sphere_users ALTER COLUMN id SET DEFAULT nextval('public.nb_sphere_users_id_seq'::regclass);
ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.cr_user_groups
    ADD CONSTRAINT cr_user_groups_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.cr_user_groups
    ADD CONSTRAINT cr_user_groups_user_id_group_id_5fe0c458_uniq UNIQUE (user_id, group_id);
ALTER TABLE ONLY public.cr_user
    ADD CONSTRAINT cr_user_pkey PRIMARY KEY (uuid);
ALTER TABLE ONLY public.cr_user_user_permissions
    ADD CONSTRAINT cr_user_user_permissions_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.cr_user_user_permissions
    ADD CONSTRAINT cr_user_user_permissions_user_id_permission_id_8f9f47d3_uniq UNIQUE (user_id, permission_id);
ALTER TABLE ONLY public.cr_user
    ADD CONSTRAINT cr_user_uuid_key UNIQUE (uuid);
ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
ALTER TABLE ONLY public.nb_guild
    ADD CONSTRAINT nb_guild_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.nb_guild_user
    ADD CONSTRAINT nb_guild_user_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.nb_meeting
    ADD CONSTRAINT nb_meeting_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.nb_meeting_user
    ADD CONSTRAINT nb_meeting_user_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.nb_sphere
    ADD CONSTRAINT nb_sphere_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.nb_sphere_users
    ADD CONSTRAINT nb_sphere_users_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.nb_sphere_users
    ADD CONSTRAINT nb_sphere_users_sphere_id_user_id_aef2df6d_uniq UNIQUE (sphere_id, user_id);
CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
CREATE INDEX cr_user_groups_group_id_d685bec2 ON public.cr_user_groups USING btree (group_id);
CREATE INDEX cr_user_groups_user_id_ca41ed56 ON public.cr_user_groups USING btree (user_id);
CREATE INDEX cr_user_user_permissions_permission_id_b6a1057d ON public.cr_user_user_permissions USING btree (permission_id);
CREATE INDEX cr_user_user_permissions_user_id_53474536 ON public.cr_user_user_permissions USING btree (user_id);
CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
CREATE INDEX nb_guild_user_guild_id_40ea39d9 ON public.nb_guild_user USING btree (guild_id);
CREATE INDEX nb_guild_user_user_id_8452bced ON public.nb_guild_user USING btree (user_id);
CREATE INDEX nb_meeting_guild_id_da42998c ON public.nb_meeting USING btree (guild_id);
CREATE INDEX nb_meeting_organizer_id_4db9cb61 ON public.nb_meeting USING btree (organizer_id);
CREATE INDEX nb_meeting_user_meeting_id_bc74b8b8 ON public.nb_meeting_user USING btree (meeting_id);
CREATE INDEX nb_meeting_user_user_id_df2ce87b ON public.nb_meeting_user USING btree (user_id);
CREATE INDEX nb_sphere_users_sphere_id_61522e9b ON public.nb_sphere_users USING btree (sphere_id);
CREATE INDEX nb_sphere_users_user_id_9a6b9cb6 ON public.nb_sphere_users USING btree (user_id);
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.cr_user_groups
    ADD CONSTRAINT cr_user_groups_group_id_d685bec2_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.cr_user_groups
    ADD CONSTRAINT cr_user_groups_user_id_ca41ed56_fk_cr_user_uuid FOREIGN KEY (user_id) REFERENCES public.cr_user(uuid) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.cr_user_user_permissions
    ADD CONSTRAINT cr_user_user_permiss_permission_id_b6a1057d_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.cr_user_user_permissions
    ADD CONSTRAINT cr_user_user_permissions_user_id_53474536_fk_cr_user_uuid FOREIGN KEY (user_id) REFERENCES public.cr_user(uuid) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_cr_user_uuid FOREIGN KEY (user_id) REFERENCES public.cr_user(uuid) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.nb_guild
    ADD CONSTRAINT nb_guild_sphere_id_fkey FOREIGN KEY (sphere_id) REFERENCES public.nb_sphere(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.nb_guild_user
    ADD CONSTRAINT nb_guild_user_guild_id_40ea39d9_fk_nb_guild_id FOREIGN KEY (guild_id) REFERENCES public.nb_guild(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.nb_guild_user
    ADD CONSTRAINT nb_guild_user_user_id_8452bced_fk_cr_user_uuid FOREIGN KEY (user_id) REFERENCES public.cr_user(uuid) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.nb_meeting
    ADD CONSTRAINT nb_meeting_guild_id_da42998c_fk_nb_guild_id FOREIGN KEY (guild_id) REFERENCES public.nb_guild(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.nb_meeting
    ADD CONSTRAINT nb_meeting_organizer_id_4db9cb61_fk_cr_user_uuid FOREIGN KEY (organizer_id) REFERENCES public.cr_user(uuid) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.nb_meeting_user
    ADD CONSTRAINT nb_meeting_user_meeting_id_bc74b8b8_fk_nb_meeting_id FOREIGN KEY (meeting_id) REFERENCES public.nb_meeting(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.nb_meeting_user
    ADD CONSTRAINT nb_meeting_user_user_id_df2ce87b_fk_cr_user_uuid FOREIGN KEY (user_id) REFERENCES public.cr_user(uuid) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.nb_sphere_users
    ADD CONSTRAINT nb_sphere_users_sphere_id_61522e9b_fk_nb_sphere_id FOREIGN KEY (sphere_id) REFERENCES public.nb_sphere(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.nb_sphere_users
    ADD CONSTRAINT nb_sphere_users_user_id_9a6b9cb6_fk_cr_user_uuid FOREIGN KEY (user_id) REFERENCES public.cr_user(uuid) DEFERRABLE INITIALLY DEFERRED;
