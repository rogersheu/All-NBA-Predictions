CREATE TABLE allstars
("Name" TEXT,
"Season" YEAR,
"Status" INTEGER);

INSERT INTO allstars
SELECT * FROM allstar_full_csv;

SELECT * FROM allstars;

SELECT * FROM playerdata_notrades;

SELECT stats.Player, stats.Year, stats.Age, (stats.ORB/stats.G) AS ORPG, (stats.DRB/stats.G) AS DRPG, (stats.TRB/stats.G) AS RPG, (stats.AST/stats.G) AS APG,
	(stats.STL/stats.G) AS SPG, (stats.BLK/stats.G) AS BPG, (stats.TOV/stats.G) AS TOPG, (stats.PTS/stats.G) AS PPG, stats.PER, stats.TS, stats.'3PAr', stats.FTr,
	stats.OWS, stats.DWS, stats.WS, stats.WS48, stats.OBPM, stats.DBPM, stats.BPM, stats.VORP,
	COALESCE(allstars.Status, 0) AS allstarFlag, COALESCE(allNBA.Status, 0) AS allNBAFlag, 
	teamWL.Perc FROM playerdata_notrades AS stats
LEFT JOIN allstars ON (stats.Player = allstars.Name AND stats.Year = allstars.Season)
LEFT JOIN allNBA ON (stats.Player = allNBA.Name AND stats.Year = allNBA.Season)
LEFT JOIN teamWL ON (stats.Tm = teamWL.Tm AND stats.Year = teamWL.Year)
WHERE allNBAFlag = 1 AND allstarFlag = 1 AND teamWL.Perc > 0
ORDER BY ID ASC;

SELECT * FROM listofallNBAteams_csv;

SELECT * FROM teamWL;



WITH topPlayers AS
(
	SELECT stats.Player, stats.Year, stats.Age, (stats.ORB/stats.G) AS ORPG, (stats.DRB/stats.G) AS DRPG, (stats.TRB/stats.G) AS RPG, (stats.AST/stats.G) AS APG,
		(stats.STL/stats.G) AS SPG, (stats.BLK/stats.G) AS BPG, (stats.TOV/stats.G) AS TOPG, (stats.PTS/stats.G) AS PPG, stats.PER, stats.TS, stats.'3PAr', stats.FTr,
		stats.OWS, stats.DWS, stats.WS, stats.WS48, stats.OBPM, stats.DBPM, stats.BPM, stats.VORP,
		COALESCE(allstars.Status, 0) AS allstarFlag, COALESCE(allNBA.Status, 0) AS allNBAFlag, 
		teamWL.Perc 
		FROM playerdata_notrades AS stats
	LEFT JOIN allstars ON (stats.Player = allstars.Name AND stats.Year = allstars.Season)
	LEFT JOIN allNBA ON (stats.Player = allNBA.Name AND stats.Year = allNBA.Season)
	LEFT JOIN teamWL ON (stats.Tm = teamWL.Tm AND stats.Year = teamWL.Year)
)
SELECT * FROM topPlayers
WHERE allNBAFlag = 1 AND allstarFlag = 1 AND topPlayers.Perc > 0;




WITH topPlayers AS
(
	SELECT stats.Player, stats.Year, stats.Age, ROUND(CAST(stats.TRB AS REAL)/stats.G, 1) AS RPG, ROUND(CAST(stats.AST AS REAL)/stats.G, 1) AS APG, ROUND(CAST(stats.STL AS REAL)/stats.G, 1) AS SPG, ROUND(CAST(stats.BLK AS REAL)/stats.G, 1) AS BPG, 
		ROUND(CAST(stats.TOV AS REAL)/stats.G, 1) AS TOPG, ROUND(CAST(stats.PTS AS REAL)/stats.G, 1) AS PPG, stats.TS, stats.'3PAr', stats.FTr, stats.WS48,-- stats.BPM, stats.VORP, 
		teamWL.Perc,
		COALESCE(allstars.Status, 0) AS allstarFlag, COALESCE(allNBA.Status, 0) AS allNBAFlag
		FROM playerdata_notrades AS stats
	LEFT JOIN allstars ON (stats.Player = allstars.Name AND stats.Year = allstars.Season)
	LEFT JOIN allNBA ON (stats.Player = allNBA.Name AND stats.Year = allNBA.Season)
	LEFT JOIN teamWL ON (stats.Tm = teamWL.Tm AND stats.Year = teamWL.Year)
)
SELECT * FROM topPlayers
WHERE allNBAFlag = 1 AND allstarFlag = 1 AND topPlayers.Perc > 0;



WITH topPlayers AS
(
	SELECT stats.Player, stats.Year, ROUND(CAST(stats.TRB AS REAL)/stats.G, 1) AS RPG, ROUND(CAST(stats.AST AS REAL)/stats.G, 1) AS APG, ROUND(CAST((stats.STL + stats.BLK) AS REAL)/stats.G, 1) AS SBPG,
		ROUND(CAST(stats.PTS AS REAL)/stats.G, 1) AS PPG, stats.TS, stats.WS48,-- stats.BPM, stats.VORP, 
		teamWL.Perc,
		COALESCE(allstars.Status, 0) AS allstarFlag, COALESCE(allNBA.Status, 0) AS allNBAFlag
		FROM playerdata_notrades AS stats
	LEFT JOIN allstars ON (stats.Player = allstars.Name AND stats.Year = allstars.Season)
	LEFT JOIN allNBA ON (stats.Player = allNBA.Name AND stats.Year = allNBA.Season)
	LEFT JOIN teamWL ON (stats.Tm = teamWL.Tm AND stats.Year = teamWL.Year)
)
SELECT * FROM topPlayers
WHERE (allNBAFlag = 1 OR allstarFlag = 1) AND topPlayers.Perc > 0;