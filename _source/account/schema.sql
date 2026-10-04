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

-- ---------- behaviour tracking (applied 2026-10-04 as migration events_tracking) ----------
-- Every page view, product view, size pick, bag add, save, checkout start and content view,
-- written from the browser (anon key) with a per-browser anon_id; claim_events() stitches it to the member on sign-in.
create table if not exists public.events (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users(id) on delete cascade,
  anon_id text not null,
  session_id text,
  name text not null,          -- page_view, view_item, view_collection, select_size, view_size_guide, add_to_cart, add_to_wishlist, bundle_add, select_promotion, begin_checkout, view_content, select_content
  ref text,                    -- product slug / site id, collection key, path, reel id
  title text, image text, url text,
  value numeric,
  meta jsonb not null default '{}'::jsonb,   -- size, qty, price, team, device, path, landing, utm_*, referrer, content_type
  created_at timestamptz not null default now()
);
create index if not exists events_user_idx on public.events(user_id, created_at desc);
create index if not exists events_anon_idx on public.events(anon_id, created_at desc);
create index if not exists events_name_ref_idx on public.events(name, ref);
alter table public.events enable row level security;
create policy "events insert" on public.events for insert to anon, authenticated with check (user_id is null or user_id = auth.uid());
create policy "events read own" on public.events for select to authenticated using (user_id = auth.uid());
create or replace function public.claim_events(p_anon text) returns integer
language plpgsql security definer set search_path = public as $$
declare n integer;
begin
  if auth.uid() is null then return 0; end if;
  update public.events set user_id = auth.uid() where anon_id = p_anon and user_id is null;
  get diagnostics n = row_count; return n;
end $$;
revoke all on function public.claim_events(text) from public;
grant execute on function public.claim_events(text) to authenticated;
-- "Keep shopping for": products this member looked at / put in the bag, newest first
create or replace function public.my_product_affinity(p_days integer default 90, p_limit integer default 24)
returns table(ref text, title text, image text, url text, views integer, carts integer, last_at timestamptz)
language sql security invoker stable as $$
  select ref, max(title) filter (where title<>''), max(image) filter (where image<>''), max(url) filter (where url<>''),
         count(*) filter (where name in ('view_item','select_size','view_size_guide'))::int,
         count(*) filter (where name='add_to_cart')::int, max(created_at)
  from public.events
  where user_id = auth.uid() and ref is not null and name in ('view_item','select_size','view_size_guide','add_to_cart')
    and created_at > now() - make_interval(days => p_days)
  group by ref order by max(created_at) desc limit p_limit
$$;
grant execute on function public.my_product_affinity(integer,integer) to authenticated;
