-- Shared, writable sandbox for participants. Run once as a workspace admin / metastore admin.
CREATE CATALOG IF NOT EXISTS playground
  COMMENT 'Shared writable sandbox for hackathon participants. Read-only datasets live in the hackathon catalog.';
CREATE SCHEMA IF NOT EXISTS playground.shared
  COMMENT 'Shared scratch schema. Any workspace user can create, read, change and drop tables here. Prefix table names with your name or team.';
GRANT USE CATALOG, USE SCHEMA, CREATE SCHEMA, CREATE TABLE, CREATE VOLUME, CREATE FUNCTION, CREATE MODEL,
      SELECT, MODIFY, EXECUTE, READ VOLUME, WRITE VOLUME ON CATALOG playground TO `account users`;

-- Read-only access to the loaded datasets (notebook 06 also does this).
GRANT USE CATALOG ON CATALOG hackathon TO `account users`;
GRANT USE SCHEMA, SELECT, READ VOLUME ON SCHEMA hackathon.two_postcodes TO `account users`;
