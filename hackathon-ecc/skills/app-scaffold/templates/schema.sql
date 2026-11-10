-- =============================================================================
-- schema.sql — EXAMPLE schema for an MVP (adapt to your domain)
-- -----------------------------------------------------------------------------
-- This is a reference, not a fixed schema. It shows the patterns you want in
-- every Supabase project:
--   1. A `profiles` table mirroring auth.users (1:1), populated by a trigger.
--   2. A domain table (`items`) owned by a user.
--   3. A join/transaction table (`orders`).
--   4. updated_at maintained by a trigger.
--   5. RLS enabled on every table (policies live in the RLS migration).
--
-- Conventions used:
--   - snake_case table & column names, plural table names.
--   - uuid primary keys with gen_random_uuid().
--   - timestamptz for all timestamps, default now().
--   - foreign keys to auth.users(id) for ownership.
-- =============================================================================

-- Reusable trigger function: keep updated_at fresh on UPDATE.
create or replace function public.handle_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

-- -----------------------------------------------------------------------------
-- profiles: public user data, 1:1 with auth.users.
-- NEVER expose auth.users directly; mirror the bits you need here.
-- -----------------------------------------------------------------------------
create table public.profiles (
  id          uuid primary key references auth.users(id) on delete cascade,
  username    text unique,
  full_name   text,
  avatar_url  text,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

create trigger profiles_updated_at
  before update on public.profiles
  for each row execute function public.handle_updated_at();

-- Auto-create a profile row whenever a new auth user signs up.
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = ''
as $$
begin
  insert into public.profiles (id, full_name, avatar_url)
  values (
    new.id,
    new.raw_user_meta_data ->> 'full_name',
    new.raw_user_meta_data ->> 'avatar_url'
  );
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- -----------------------------------------------------------------------------
-- items: example domain table, owned by a user.
-- -----------------------------------------------------------------------------
create table public.items (
  id          uuid primary key default gen_random_uuid(),
  owner_id    uuid not null references auth.users(id) on delete cascade,
  name        text not null,
  description text,
  price numeric(10,2) not null default 0 check (price >= 0),
  is_published boolean not null default false,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

create index items_owner_id_idx on public.items (owner_id);
create index items_is_published_idx on public.items (is_published) where is_published;

create trigger items_updated_at
  before update on public.items
  for each row execute function public.handle_updated_at();

-- -----------------------------------------------------------------------------
-- orders: example transaction table linking a buyer to an item.
-- -----------------------------------------------------------------------------
create table public.orders (
  id          uuid primary key default gen_random_uuid(),
  item_id   uuid not null references public.items(id) on delete cascade,
  buyer_id    uuid not null references auth.users(id) on delete cascade,
  start_date  date not null,
  end_date    date not null,
  status      text not null default 'pending'
                check (status in ('pending', 'confirmed', 'cancelled')),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  check (end_date > start_date)
);

create index orders_item_id_idx on public.orders (item_id);
create index orders_buyer_id_idx on public.orders (buyer_id);

create trigger orders_updated_at
  before update on public.orders
  for each row execute function public.handle_updated_at();

-- Enable RLS on everything. Policies are defined in the RLS migration.
alter table public.profiles enable row level security;
alter table public.items  enable row level security;
alter table public.orders enable row level security;
