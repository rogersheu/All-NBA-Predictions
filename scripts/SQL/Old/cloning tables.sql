CREATE TABLE playerstats_backup AS SELECT * FROM playerstats WHERE 0;

INSERT INTO playerstats_backup SELECT * FROM playerstats;

--DROP TABLE playerstats_backup