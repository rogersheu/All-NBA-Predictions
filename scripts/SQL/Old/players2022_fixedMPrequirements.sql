-- FOR DAILY UPDATES
WITH Players2022 AS
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
        adv.TS,
        adv.TS - teamadv.TS AS rTS,
        --stats.'3PAr', stats.FTr,
        adv.WS48,-- stats.BPM, stats.VORP,
        teamWL2022.Perc--,
        --1 - (1 - COALESCE(allstars.Status, 0)) * (1 - COALESCE(allNBA.Status, 0)) AS allLeague
		FROM totals AS stats
	LEFT JOIN advanced AS adv ON (stats.Player = adv.Player AND stats.Year = adv.Year)
	LEFT JOIN allstars ON (stats.Player = allstars.Name AND stats.Year = allstars.Season)
	LEFT JOIN allNBA ON (stats.Player = allNBA.Name AND stats.Year = allNBA.Season)
	LEFT JOIN teamWL2022 ON (stats.Tm = teamWL2022.Tm AND stats.Year = teamWL2022.Year)
	LEFT JOIN teamadv ON (stats.Year = teamadv.Season)
)
SELECT * FROM Players2022
WHERE Year = 2022 AND Perc > 0 AND ((MPG > 25 AND G > 12) OR MP > 500);
