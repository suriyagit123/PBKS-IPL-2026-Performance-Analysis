USE pbks_ipl_2026;

SHOW TABLES;

DESCRIBE matches;
DESCRIBE batting;
DESCRIBE bowling;

SELECT COUNT(*) AS total_matches FROM matches;
SELECT COUNT(*) AS total_batting_records FROM batting;
SELECT COUNT(*) AS total_bowling_records FROM bowling;

SELECT result, COUNT(*) AS matches
FROM matches
GROUP BY result;

SELECT COUNT(*) AS wins
FROM matches
WHERE result = 'won';

SELECT COUNT(*) AS losses
FROM matches
WHERE result = 'lost';

SELECT COUNT(*) AS no_result
FROM matches
WHERE result = 'no result';

SELECT COUNT(*) AS completed_matches
FROM matches
WHERE result IN ('won','lost');

SELECT ROUND(
    100.0 * SUM(CASE WHEN result = 'won' THEN 1 ELSE 0 END) /
    NULLIF(SUM(CASE WHEN result IN ('won','lost') THEN 1 ELSE 0 END),0),2
) AS completed_match_win_percentage
FROM matches;

SELECT
    ROUND(AVG(pbks_runs),2) AS average_pbks_runs,
    ROUND(AVG(opp_runs),2) AS average_opponent_runs,
    ROUND(AVG(run_diff),2) AS average_run_difference
FROM matches
WHERE result IN ('won','lost');

SELECT
    match_number,
    date,
    opponent,
    venue,
    pbks_runs,
    opp_runs,
    run_diff,
    result,
    margin,
    phase
FROM matches
ORDER BY match_number;

SELECT
    match_number,
    date,
    opponent,
    pbks_runs,
    result
FROM matches
ORDER BY pbks_runs DESC
LIMIT 1;

SELECT
    match_number,
    date,
    opponent,
    pbks_runs,
    result
FROM matches
ORDER BY pbks_runs ASC
LIMIT 1;

SELECT
    match_number,
    date,
    opponent,
    opp_runs,
    result
FROM matches
ORDER BY opp_runs DESC
LIMIT 1;

SELECT
    match_number,
    date,
    opponent,
    pbks_runs,
    opp_runs,
    run_diff,
    result
FROM matches
WHERE result = 'won'
ORDER BY run_diff DESC
LIMIT 1;

SELECT
    phase,
    COUNT(*) AS matches,
    SUM(CASE WHEN result = 'won' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN result = 'lost' THEN 1 ELSE 0 END) AS losses,
    ROUND(AVG(pbks_runs),2) AS average_pbks_runs,
    ROUND(AVG(opp_runs),2) AS average_opponent_runs,
    ROUND(AVG(run_diff),2) AS average_run_difference
FROM matches
WHERE result IN ('won','lost')
GROUP BY phase
ORDER BY CASE phase
    WHEN 'Strong Start' THEN 1
    WHEN 'Losing Streak' THEN 2
    WHEN 'Recovery' THEN 3
    ELSE 4
END;

SELECT
    batter,
    SUM(runs) AS total_runs,
    SUM(balls) AS total_balls,
    SUM(fours) AS total_fours,
    SUM(sixes) AS total_sixes,
    ROUND(100.0 * SUM(runs) / NULLIF(SUM(balls),0),2) AS strike_rate
FROM batting
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;

SELECT
    batter,
    SUM(runs) AS total_runs,
    SUM(balls) AS total_balls,
    ROUND(100.0 * SUM(runs) / NULLIF(SUM(balls),0),2) AS strike_rate
FROM batting
GROUP BY batter
ORDER BY strike_rate DESC;

SELECT
    bowler,
    SUM(wickets) AS total_wickets,
    SUM(runs) AS runs_conceded,
    SUM(dots) AS total_dot_balls
FROM bowling
GROUP BY bowler
ORDER BY total_wickets DESC
LIMIT 10;

SELECT
    bowler,
    SUM(wickets) AS total_wickets,
    SUM(runs) AS runs_conceded,
    ROUND(
        SUM(runs) /
        NULLIF(
            SUM(
                FLOOR(overs) * 6 +
                ROUND((overs - FLOOR(overs)) * 10)
            ) / 6.0,
            0
        ),
        2
    ) AS economy
FROM bowling
GROUP BY bowler
ORDER BY total_wickets DESC, economy ASC
LIMIT 5;

SELECT
    m.phase,
    SUM(b.runs) AS total_runs,
    SUM(b.balls) AS total_balls,
    ROUND(
        100.0 * SUM(b.runs) / NULLIF(SUM(b.balls),0),
        2
    ) AS strike_rate
FROM matches m
INNER JOIN batting b
    ON m.match_number = b.match_number
GROUP BY m.phase
ORDER BY CASE m.phase
    WHEN 'Strong Start' THEN 1
    WHEN 'Losing Streak' THEN 2
    WHEN 'Recovery' THEN 3
    ELSE 4
END;

SELECT
    m.phase,
    SUM(b.runs) AS runs_conceded,
    SUM(b.wickets) AS wickets,
    SUM(b.dots) AS dot_balls
FROM matches m
INNER JOIN bowling b
    ON m.match_number = b.match_number
GROUP BY m.phase
ORDER BY CASE m.phase
    WHEN 'Strong Start' THEN 1
    WHEN 'Losing Streak' THEN 2
    WHEN 'Recovery' THEN 3
    ELSE 4
END;

SELECT
    opponent,
    COUNT(*) AS matches,
    SUM(CASE WHEN result = 'won' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN result = 'lost' THEN 1 ELSE 0 END) AS losses,
    ROUND(AVG(pbks_runs),2) AS average_pbks_runs,
    ROUND(AVG(opp_runs),2) AS average_opponent_runs,
    ROUND(AVG(run_diff),2) AS average_run_difference
FROM matches
WHERE result IN ('won','lost')
GROUP BY opponent;

SELECT
    venue,
    COUNT(*) AS matches,
    SUM(CASE WHEN result = 'won' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN result = 'lost' THEN 1 ELSE 0 END) AS losses,
    ROUND(AVG(pbks_runs),2) AS average_pbks_runs,
    ROUND(AVG(opp_runs),2) AS average_opponent_runs
FROM matches
WHERE result IN ('won','lost')
GROUP BY venue;

SELECT
    toss_decision,
    COUNT(*) AS matches,
    SUM(CASE WHEN result = 'won' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN result = 'lost' THEN 1 ELSE 0 END) AS losses
FROM matches
WHERE result IN ('won','lost')
GROUP BY toss_decision;

SELECT
    pbks_batting_first,
    COUNT(*) AS matches,
    SUM(CASE WHEN result = 'won' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN result = 'lost' THEN 1 ELSE 0 END) AS losses,
    ROUND(AVG(pbks_runs),2) AS average_pbks_runs,
    ROUND(AVG(opp_runs),2) AS average_opponent_runs
FROM matches
WHERE result IN ('won','lost')
GROUP BY pbks_batting_first;

SELECT
    m.match_number,
    m.date,
    m.opponent,
    b.batter,
    b.runs,
    b.balls,
    b.fours,
    b.sixes,
    b.strike_rate
FROM matches m
INNER JOIN batting b
    ON m.match_number = b.match_number
ORDER BY b.runs DESC
LIMIT 20;

SELECT
    m.match_number,
    m.date,
    m.opponent,
    b.bowler,
    b.overs,
    b.runs,
    b.wickets,
    b.economy,
    b.dots
FROM matches m
INNER JOIN bowling b
    ON m.match_number = b.match_number
ORDER BY b.wickets DESC, b.economy ASC
LIMIT 20;

SELECT
    match_number,
    date,
    opponent,
    venue,
    toss_winner,
    toss_decision,
    winner,
    pbks_score,
    pbks_overs,
    opponent_score,
    opponent_overs,
    pbks_runs,
    opp_runs,
    run_diff,
    pbks_batting_first,
    result,
    margin,
    phase
FROM matches
ORDER BY match_number;
