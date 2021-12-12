DROP TABLE totals;

DROP TABLE advanced;

DROP TABLE teamWL2022;

DROP TABLE teamadv;

--------
-- Update tables now
--------

ALTER TABLE advanced RENAME COLUMN "TS%" TO TS;
ALTER TABLE advanced RENAME COLUMN "WS/48" TO WS48;
ALTER TABLE teamStandingsAbbrev RENAME TO teamWL2022;
ALTER TABLE teamadv_csv RENAME TO teamadv;
ALTER TABLE teamadv RENAME COLUMN "TS%" TO TS;