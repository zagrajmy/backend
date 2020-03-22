CREATE FUNCTION public.set_current_timestamp_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  _new record;
BEGIN
  _new := NEW;
  _new."updated_at" = NOW();
  RETURN _new;
END;
$$;
CREATE TABLE public.guild (
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    name text NOT NULL,
    description text
);
CREATE SEQUENCE public.guild_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.guild_id_seq OWNED BY public.guild.id;
CREATE TABLE public.guild_member (
    guild_id integer NOT NULL,
    member_id uuid NOT NULL
);
CREATE TABLE public.meeting (
    id integer NOT NULL,
    description text DEFAULT '""'::text NOT NULL,
    location text,
    publication_time timestamp with time zone,
    start_time timestamp with time zone,
    end_time timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    organizer_id uuid NOT NULL,
    guild_id integer,
    title text NOT NULL,
    sphere_id integer NOT NULL
);
CREATE SEQUENCE public.meeting_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.meeting_id_seq OWNED BY public.meeting.id;
CREATE TABLE public.meeting_participant (
    meeting_id integer NOT NULL,
    participant_id uuid NOT NULL
);
CREATE TABLE public.sphere (
    id integer NOT NULL,
    name text NOT NULL,
    domain text
);
CREATE SEQUENCE public.sphere_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.sphere_id_seq OWNED BY public.sphere.id;
CREATE TABLE public."user" (
    uuid uuid DEFAULT public.gen_random_uuid() NOT NULL,
    name text NOT NULL,
    email text NOT NULL,
    last_login timestamp with time zone,
    auth0_id text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);
ALTER TABLE ONLY public.guild ALTER COLUMN id SET DEFAULT nextval('public.guild_id_seq'::regclass);
ALTER TABLE ONLY public.meeting ALTER COLUMN id SET DEFAULT nextval('public.meeting_id_seq'::regclass);
ALTER TABLE ONLY public.sphere ALTER COLUMN id SET DEFAULT nextval('public.sphere_id_seq'::regclass);
ALTER TABLE ONLY public.guild_member
    ADD CONSTRAINT guild_member_pkey PRIMARY KEY (guild_id, member_id);
ALTER TABLE ONLY public.guild
    ADD CONSTRAINT guild_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.meeting_participant
    ADD CONSTRAINT meeting_participant_pkey PRIMARY KEY (meeting_id, participant_id);
ALTER TABLE ONLY public.meeting
    ADD CONSTRAINT meeting_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.sphere
    ADD CONSTRAINT sphere_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);
ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (uuid);
CREATE TRIGGER set_public_guild_updated_at BEFORE UPDATE ON public.guild FOR EACH ROW EXECUTE FUNCTION public.set_current_timestamp_updated_at();
COMMENT ON TRIGGER set_public_guild_updated_at ON public.guild IS 'trigger to set value of column "updated_at" to current timestamp on row update';
CREATE TRIGGER set_public_meeting_updated_at BEFORE UPDATE ON public.meeting FOR EACH ROW EXECUTE FUNCTION public.set_current_timestamp_updated_at();
COMMENT ON TRIGGER set_public_meeting_updated_at ON public.meeting IS 'trigger to set value of column "updated_at" to current timestamp on row update';
ALTER TABLE ONLY public.guild_member
    ADD CONSTRAINT guild_member_guild_id_fkey FOREIGN KEY (guild_id) REFERENCES public.guild(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY public.guild_member
    ADD CONSTRAINT guild_member_member_id_fkey FOREIGN KEY (member_id) REFERENCES public."user"(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY public.meeting
    ADD CONSTRAINT meeting_guild_id_fkey FOREIGN KEY (guild_id) REFERENCES public.guild(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.meeting
    ADD CONSTRAINT meeting_organizer_id_fkey FOREIGN KEY (organizer_id) REFERENCES public."user"(uuid) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.meeting_participant
    ADD CONSTRAINT meeting_participant_meeting_id_fkey FOREIGN KEY (meeting_id) REFERENCES public.meeting(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY public.meeting_participant
    ADD CONSTRAINT meeting_participant_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES public."user"(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY public.meeting
    ADD CONSTRAINT meeting_sphere_id_fkey FOREIGN KEY (sphere_id) REFERENCES public.sphere(id) ON UPDATE CASCADE ON DELETE CASCADE;
