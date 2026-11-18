-- F-plyny Přeškolení – pokrok studia
-- Osobní Supabase projekt mtb-servis (klpcgnivfvczvvyoqzal), vlastní schéma fplyny.
-- Lze spustit opakovaně. Každý uživatel vidí a mění jen svůj řádek.
create schema if not exists fplyny;

create table if not exists fplyny.pokrok (
  user_id    uuid primary key default auth.uid() references auth.users(id) on delete cascade,
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table fplyny.pokrok enable row level security;

drop policy if exists "pokrok_cteni" on fplyny.pokrok;
create policy "pokrok_cteni" on fplyny.pokrok
  for select to authenticated using (user_id = (select auth.uid()));

drop policy if exists "pokrok_vlozeni" on fplyny.pokrok;
create policy "pokrok_vlozeni" on fplyny.pokrok
  for insert to authenticated with check (user_id = (select auth.uid()));

drop policy if exists "pokrok_uprava" on fplyny.pokrok;
create policy "pokrok_uprava" on fplyny.pokrok
  for update to authenticated using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

grant usage on schema fplyny to authenticated;
grant select, insert, update on fplyny.pokrok to authenticated;
