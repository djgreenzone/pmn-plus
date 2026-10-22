-- PMN+ Content Team applications (the roster). Run once in Supabase > SQL Editor (project pmn-plus).
-- /api/join writes here with the service-role key; nobody can read it from the browser (RLS on, no policies).
create table if not exists public.content_team_applications (
  id            bigint generated always as identity primary key,
  ref           text unique not null,
  created_at    timestamptz not null default now(),
  status        text not null default 'applied',   -- applied, shortlisted, conversation, roster, not_now
  first_name    text not null,
  last_name     text not null,
  email         text not null,
  phone         text,
  roles         text[] not null default '{}',
  city          text,
  age           text,
  portfolio     text,
  instagram     text,
  photo_types   text[] default '{}',
  photo_gear    text,
  photo_edit    text,
  video_types   text[] default '{}',
  video_gear    text,
  video_edit    text,
  height        text,
  tee_size      text,
  model_exp     text,
  guardian_name  text,
  guardian_email text,
  availability  text[] default '{}',
  why           text,
  newsletter    boolean default false,
  photos        text[] default '{}',   -- paths in the private Storage bucket "content-team"
  notes         text
);
create index if not exists content_team_applications_created_idx on public.content_team_applications (created_at desc);
create index if not exists content_team_applications_status_idx  on public.content_team_applications (status);
alter table public.content_team_applications enable row level security;
