--Gets players who made either the All-Star or all-NBA team.

WITH topPlayers AS
(
	SELECT
        stats.Player,
        stats.Year,
        stats.MP,
        stats.G,
        ROUND(CAST(stats.MP AS REAL)/stats.G, 1) AS MPG,
        ROUND(CAST(stats.TRB AS REAL)/stats.G, 1) AS RPG,
        ROUND(CAST(stats.AST AS REAL)/stats.G, 1) AS APG,
        ROUND(CAST((stats.STL + stats.BLK) AS REAL)/stats.G, 1) AS SBPG,
        ROUND(CAST(stats.PTS AS REAL)/stats.G, 1) AS PPG,
        stats.TS,
        stats.WS48,
        teamWL.Perc,
        1 - (1 - COALESCE(allstars.Status, 0)) * (1 - COALESCE(allNBA.Status, 0)) AS allLeague
		FROM playerdata_notrades AS stats
	LEFT JOIN allstars ON (stats.Player = allstars.Name AND stats.Year = allstars.Season)
	LEFT JOIN allNBA ON (stats.Player = allNBA.Name AND stats.Year = allNBA.Season)
	LEFT JOIN teamWL ON (stats.Tm = teamWL.Tm AND stats.Year = teamWL.Year)
)
SELECT * FROM topPlayers
WHERE allLeague = 1 AND topPlayers.Perc > 0;
