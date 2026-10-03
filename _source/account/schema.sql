-- PMN+ accounts schema. Already applied to Supabase project pmn-plus (zacfssfjlmixnqhjuoed) on 2026-10-03
-- as migrations pmn_accounts_tables + pmn_accounts_grants. Kept here for reference / a fresh project.
-- Every table has row-level security: a signed-in person can only read or change their own rows.

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text,
  first_name text,
  last_name text,
  country text,                                   -- "where you rep from"
  favourite_team text,                            -- toa-samoa | mate-maa-tonga | both | other
  marketing_opt_in boolean not null default true,
  tier text not null default 'member' check (tier in ('member','plus','vip')),   -- room for paid tiers; server-only
  signup_source text,                             -- account | google | apple | ...
  shopify_customer_id text,                       -- server-only
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
alter table public.profiles enable row level security;
create policy "read own profile" on public.profiles for select to authenticated using ((select auth.uid()) = id);
create policy "update own profile" on public.profiles for update to authenticated using ((select auth.uid()) = id) with check ((select auth.uid()) = id);

create table public.saved_items (
  id bigint generated always as identity primary key,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  kind text not null check (kind in ('product', 'reel', 'article')),
  ref text not null,
  title text,
  image text,
  url text,
  created_at timestamptz not null default now(),
  unique (user_id, kind, ref)
);
alter table public.saved_items enable row level security;
create policy "read own saved" on public.saved_items for select to authenticated using ((select auth.uid()) = user_id);
create policy "add own saved" on public.saved_items for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "remove own saved" on public.saved_items for delete to authenticated using ((select auth.uid()) = user_id);
create index saved_items_user_idx on public.saved_items (user_id, created_at desc);

create function public.touch_updated_at() returns trigger
language plpgsql set search_path = '' as $$
begin new.updated_at = now(); return new; end $$;
create trigger profiles_touch before update on public.profiles for each row execute function public.touch_updated_at();

-- new sign-up -> profile row (email code, Google or Apple)
create function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  insert into public.profiles (id, email, first_name, marketing_opt_in, signup_source)
  values (new.id, lower(new.email),
          coalesce(nullif(new.raw_user_meta_data->>'first_name', ''), nullif(split_part(coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name', ''), ' ', 1), '')),
          coalesce((new.raw_user_meta_data->>'marketing_opt_in')::boolean, true),
          coalesce(nullif(new.raw_user_meta_data->>'signup_source', ''), new.raw_app_meta_data->>'provider'))
  on conflict (id) do nothing;
  return new;
end $$;
create trigger on_auth_user_created after insert on auth.users for each row execute function public.handle_new_user();

-- people may edit their own name, country, team and email preference; never tier or the Shopify link
revoke all on public.profiles from anon, authenticated;
grant select on public.profiles to authenticated;
grant update (first_name, last_name, country, favourite_team, marketing_opt_in) on public.profiles to authenticated;
revoke all on public.saved_items from anon, authenticated;
grant select, insert, delete on public.saved_items to authenticated;
revoke execute on function public.handle_new_user() from public, anon, authenticated;
