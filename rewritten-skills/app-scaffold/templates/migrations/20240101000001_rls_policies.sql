-- =============================================================================
-- Migration: 20240101000001_rls_policies
-- Row Level Security policies.
-- -----------------------------------------------------------------------------
-- KEY MENTAL MODEL:
--   * RLS is enabled per-table (done in the init migration).
--   * With RLS ON and NO policy, the table denies all access to anon/auth roles.
--   * Each policy grants access for a specific command (select/insert/update/delete).
--   * `auth.uid()` returns the id of the currently authenticated user (or null).
--   * `to authenticated` / `to anon` scope a policy to a role.
--   * USING (...)  → which existing rows the user may read/affect.
--   * WITH CHECK (...) → which new/updated row values are allowed to be written.
--   * The service_role key BYPASSES all of this — server-side only.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- profiles
-- -----------------------------------------------------------------------------
-- Anyone (even logged-out) can read profiles (public directory).
create policy "Profiles are viewable by everyone"
  on public.profiles for select
  using (true);

-- A user can insert their own profile row (id must equal their uid).
create policy "Users can insert their own profile"
  on public.profiles for insert
  to authenticated
  with check (auth.uid() = id);

-- A user can update only their own profile.
create policy "Users can update their own profile"
  on public.profiles for update
  to authenticated
  using (auth.uid() = id)
  with check (auth.uid() = id);

-- -----------------------------------------------------------------------------
-- items
-- -----------------------------------------------------------------------------
-- Published items are visible to everyone; owners always see their own.
create policy "Published items are viewable by everyone"
  on public.items for select
  using (is_published = true or auth.uid() = owner_id);

-- Owners can create items they own.
create policy "Owners can insert their own items"
  on public.items for insert
  to authenticated
  with check (auth.uid() = owner_id);

-- Owners can update their own items.
create policy "Owners can update their own items"
  on public.items for update
  to authenticated
  using (auth.uid() = owner_id)
  with check (auth.uid() = owner_id);

-- Owners can delete their own items.
create policy "Owners can delete their own items"
  on public.items for delete
  to authenticated
  using (auth.uid() = owner_id);

-- -----------------------------------------------------------------------------
-- orders
-- -----------------------------------------------------------------------------
-- An order is visible to the buyer who made it OR the owner of the item.
create policy "Orders visible to buyer and item owner"
  on public.orders for select
  to authenticated
  using (
    auth.uid() = buyer_id
    or auth.uid() = (select owner_id from public.items where id = item_id)
  );

-- Buyers can create orders for themselves.
create policy "Buyers can create their own orders"
  on public.orders for insert
  to authenticated
  with check (auth.uid() = buyer_id);

-- Buyers can update (e.g. cancel) their own orders;
-- item owners can update orders on their items (e.g. confirm).
create policy "Buyer or owner can update an order"
  on public.orders for update
  to authenticated
  using (
    auth.uid() = buyer_id
    or auth.uid() = (select owner_id from public.items where id = item_id)
  )
  with check (
    auth.uid() = buyer_id
    or auth.uid() = (select owner_id from public.items where id = item_id)
  );
