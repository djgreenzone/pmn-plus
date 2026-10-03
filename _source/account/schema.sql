-- PMN+ accounts: run once in Supabase → SQL Editor → New query → Run.
-- Every table has row-level security: a signed-in person can only ever read or change their own rows.

-- 1. Profile (one per account). shopify_customer_id is written by the server only.
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text,
  first_name text,
  last_name text,
  marketing_opt_in boolean not null default true,
  shopify_customer_id text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
alter table public.profiles enable row level security;

drop policy if exists "read own profile" on public.profiles;
create policy "read own profile" on public.profiles for select to authenticated using (auth.uid() = id);
drop policy if exists "update own profile" on public.profiles;
create policy "update own profile" on public.profiles for update to authenticated using (auth.uid() = id) with check (auth.uid() = id);

-- people may edit their name and email preference, never the Shopify link
revoke insert, update, delete on public.profiles from anon, authenticated;
grant select on public.profiles to authenticated;
grant update (first_name, last_name, marketing_opt_in) on public.profiles to authenticated;

create or replace function public.touch_updated_at() returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end $$;
drop trigger if exists profiles_touch on public.profiles;
create trigger profiles_touch before update on public.profiles for each row execute function public.touch_updated_at();

-- new sign-up → profile row (name comes from the sign-up form if given)
create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, email, first_name, marketing_opt_in)
  values (new.id, new.email, nullif(new.raw_user_meta_data->>'first_name', ''),
          coalesce((new.raw_user_meta_data->>'marketing_opt_in')::boolean, true))
  on conflict (id) do nothing;
  return new;
end $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users for each row execute function public.handle_new_user();

-- 2. Saved items (products, reels, articles) for both sides of the site
create table if not exists public.saved_items (
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
drop policy if exists "read own saved" on public.saved_items;
create policy "read own saved" on public.saved_items for select to authenticated using (auth.uid() = user_id);
drop policy if exists "add own saved" on public.saved_items;
create policy "add own saved" on public.saved_items for insert to authenticated with check (auth.uid() = user_id);
drop policy if exists "remove own saved" on public.saved_items;
create policy "remove own saved" on public.saved_items for delete to authenticated using (auth.uid() = user_id);
grant select, insert, delete on public.saved_items to authenticated;
