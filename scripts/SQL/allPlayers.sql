-- Extracts all players who have broken the minutes threshold.


-- Pace adjusted
WITH allPlayers AS
(
	SELECT 
        stats.Player, 
        stats.Year, 
        stats.G,
        stats.MP,
        ROUND(CAST(stats.MP AS REAL)/stats.G, 1) AS MPG,
        ROUND(CAST(stats.TRB AS REAL)/stats.G, 1) AS RPG, 
        ROUND(CAST(stats.AST AS REAL)/stats.G, 1) AS APG, 
        ROUND(CAST((stats.STL + stats.BLK) AS REAL)/stats.G, 1) AS SBPG,
        --ROUND(CAST(stats.TOV AS REAL)/stats.G, 1) AS TOPG, 
        ROUND(CAST(stats.PTS AS REAL)/stats.G, 1) AS PPG, 
        stats.TS, 
        --stats.'3PAr', stats.FTr, 
        stats.WS48,-- stats.BPM, stats.VORP, 
        teamWL.Perc,
        1 - (1 - COALESCE(allstars.Status, 0)) * (1 - COALESCE(allNBA.Status, 0)) AS allLeague
	FROM playerdata_notrades AS stats
	LEFT JOIN allstars ON (stats.Player = allstars.Name AND stats.Year = allstars.Season)
	LEFT JOIN allNBA ON (stats.Player = allNBA.Name AND stats.Year = allNBA.Season)
	LEFT JOIN teamWL ON (stats.Tm = teamWL.Tm AND stats.Year = teamWL.Year)
)
SELECT
    Player,
    Year,
    MP,
    RPG,
    APG,
    SBPG,
    PPG,
    TS,
    WS48,
    Perc,
    allLeague
FROM allPlayers
WHERE (MP > 1500 OR (MPG > 20 AND G > 50)) AND Perc > 0;



-- Pace adjusted, with separate allstar and allNBA columns
WITH allPlayers AS
(
	SELECT 
        stats.Player, 
        stats.Year, 
        stats.G,
        stats.MP,
        ROUND(CAST(stats.MP AS REAL)/stats.G * (100 / teamadv.Pace), 1) AS MPG,
        ROUND(CAST(stats.TRB AS REAL)/stats.G * (100 / teamadv.Pace), 1) AS RPG, 
        ROUND(CAST(stats.AST AS REAL)/stats.G * (100 / teamadv.Pace), 1) AS APG, 
        ROUND(CAST((stats.STL + stats.BLK) AS REAL)/stats.G * (100 / teamadv.Pace), 1) AS SBPG,
        --ROUND(CAST(stats.TOV AS REAL)/stats.G * (100 / teamadv.Pace), 1) AS TOPG, 
        ROUND(CAST(stats.PTS AS REAL)/stats.G * (100 / teamadv.Pace), 1) AS PPG, 
        stats.TS,
        stats.TS - teamadv.TS AS rTS,
        --stats.'3PAr', stats.FTr, 
        stats.WS48,-- stats.BPM, stats.VORP, 
        teamWL.Perc,
        COALESCE(allstars.Status, 0) AS allstarFlag,
        COALESCE(allNBA.Status, 0) AS allnbaFlag,
        1 - (1 - COALESCE(allstars.Status, 0)) * (1 - COALESCE(allNBA.Status, 0)) AS allLeague
	FROM playerdata_notrades AS stats
	LEFT JOIN allstars ON (stats.Player = allstars.Name AND stats.Year = allstars.Season)
	LEFT JOIN allNBA ON (stats.Player = allNBA.Name AND stats.Year = allNBA.Season)
	LEFT JOIN teamWL ON (stats.Tm = teamWL.Tm AND stats.Year = teamWL.Year)
	LEFT JOIN teamadv ON (stats.Year = teamadv.Season)
)
SELECT
    Player,
    Year,
    MP,
    RPG,
    APG,
    SBPG,
    PPG,
    TS,
    rTS,
    WS48,
    Perc,
    allstarFlag,
    allnbaFlag,
    allLeague
FROM allPlayers
WHERE (MP > 1500 OR (MPG > 20 AND G > 50)) AND Perc > 0;


-- Not pace adjusted
WITH allPlayers AS
(
	SELECT 
        stats.Player, 
        stats.MP,
        stats.G,
        ROUND(CAST(stats.MP AS REAL)/stats.G, 1) AS MPG, 
        stats.Year, 
        ROUND(CAST(stats.TRB AS REAL)/stats.G, 1) AS RPG, 
        ROUND(CAST(stats.AST AS REAL)/stats.G, 1) AS APG, 
        ROUND(CAST((stats.STL + stats.BLK) AS REAL)/stats.G, 1) AS SBPG,
        --ROUND(CAST(stats.TOV AS REAL)/stats.G, 1) AS TOPG, 
        ROUND(CAST(stats.PTS AS REAL)/stats.G, 1) AS PPG, 
        stats.TS, 
        --stats.'3PAr', stats.FTr, 
        stats.WS48,-- stats.BPM, stats.VORP, 
        teamWL.Perc,
        1 - (1 - COALESCE(allstars.Status, 0)) * (1 - COALESCE(allNBA.Status, 0)) AS allLeague
	FROM playerdata_notrades AS stats
	LEFT JOIN allstars ON (stats.Player = allstars.Name AND stats.Year = allstars.Season)
	LEFT JOIN allNBA ON (stats.Player = allNBA.Name AND stats.Year = allNBA.Season)
	LEFT JOIN teamWL ON (stats.Tm = teamWL.Tm AND stats.Year = teamWL.Year)
)
SELECT
    Player,
    Year,
    RPG,
    APG,
    SBPG,
    PPG,
    TS,
    WS48,
    Perc,
    allLeague
FROM allPlayers
WHERE (MP > 1500 OR (MPG > 20 AND G > 50)) AND Perc > 0;