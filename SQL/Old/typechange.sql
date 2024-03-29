ALTER TABLE playerstats RENAME TO playerstats_backup;

CREATE TABLE playerstats_withtype
(
"ID" INTEGER,
"Player" VARCHAR(50),
"PlayerID" VARCHAR(20),
"Year" VARCHAR(5),
"Pos" TEXT,
"Age" INTEGER,
"Tm" TEXT,
"G" INTEGER,
"GS" INTEGER,
"MP" INTEGER,
"FG" INTEGER,
"FGA" INTEGER,
"FG%" FLOAT(3),
"3P" INTEGER,
"3PA" INTEGER,
"3P%" FLOAT(3),
"FT" INTEGER,
"FTA" INTEGER,
"FT%" FLOAT(3),
"ORB" INTEGER,
"DRB" INTEGER,
"TRB" INTEGER,
"AST" INTEGER,
"STL" INTEGER,
"BLK" INTEGER,
"TOV" INTEGER,
"PF"  INTEGER,
"PTS" INTEGER,
"PER" FLOAT(3),
"TS%" FLOAT(3),
"3PAr" FLOAT(3),
"FTr" FLOAT(3),
"ORB%" FLOAT(3),
"DRB%" FLOAT(3),
"TRB%" FLOAT(3),
"AST%" FLOAT(3),
"STL%" FLOAT(3),
"BLK%" FLOAT(3),
"TOV%" FLOAT(3),
"USG%" FLOAT(3),
"OWS" FLOAT(3),
"DWS" FLOAT(3),
"WS" FLOAT(3),
"WS/48" FLOAT(3),
"OBPM" FLOAT(3),
"DBPM" FLOAT(3),
"BPM" FLOAT(3),
"VORP" FLOAT(3),
"PG%" FLOAT(3),
"SG%" FLOAT(3),
"SF%" FLOAT(3),
"PF%" FLOAT(3),
"C%" FLOAT(3),
"OnCourt" FLOAT(3),
"On-Off" FLOAT(3),
"BadPass" INTEGER,
"LostBall" INTEGER,
"Fouls Committed - Shooting" INTEGER,
"Fouls Committed - Offensive" INTEGER,
"Fouls Drawn - Shooting" INTEGER,
"Fouls Drawn - Offensive" INTEGER,
"PGA" INTEGER,
"And1" INTEGER,
"Blkd" INTEGER
);


INSERT INTO playerstats ("ID", "Player","PlayerID", "Year", "Pos", "Age", "Tm", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV",
	"PF", "PTS", "PER", "TS%", "3PAr", "FTr", "ORB%", "DRB%", "TRB%", "AST%", "STL%", "BLK%", "TOV%", "USG%", "OWS", "DWS", "WS", "WS/48", "OBPM", "DBPM", "BPM", "VORP", "PG%", "SG%", "SF%", "PF%", "C%", "OnCourt",
	"On-Off", "BadPass", "LostBall", "Fouls Committed - Shooting", "Fouls Committed - Offensive" , "Fouls Drawn - Shooting", "Fouls Drawn - Offensive", "PGA", "And1", "Blkd")
	SELECT "ID", "Player"," PlayerID", "Year", "Pos", "Age", "Tm", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV",
	"PF", "PTS", "PER", "TS%", "3PAr", "FTr", "ORB%", "DRB%", "TRB%", "AST%", "STL%", "BLK%", "TOV%", "USG%", "OWS", "DWS", "WS", "WS/48", "OBPM", "DBPM", "BPM", "VORP", "PG%", "SG%", "SF%", "PF%", "C%", "OnCourt",
	"On-Off", "BadPass", "LostBall", "Fouls Committed - Shooting", "Fouls Committed - Offensive" , "Fouls Drawn - Shooting", "Fouls Drawn - Offensive", "PGA", "And1", "Blkd"
	FROM playerstats_backup;
