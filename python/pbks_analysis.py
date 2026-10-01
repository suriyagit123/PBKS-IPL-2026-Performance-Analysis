# ============================================================
# PBKS IPL 2026 - Data Analysis
# Project:
# DATA-DRIVEN PERFORMANCE ANALYSIS OF PUNJAB KINGS (PBKS)
# IN IPL 2026
#
# Research Question:
# What factors contributed to the variation in Punjab Kings'
# performance during IPL 2026?
#
# Technology:
# Python + Pandas
# ============================================================


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 2. PROJECT PATHS
# ============================================================

# Project structure:
#
# PBKS-IPL-2026-Performance-Analysis/
#
# ├── python/
# │   └── pbks_analysis.py
# │
# ├── data/
# │   ├── pbks_matches_2026.csv
# │   ├── pbks_batting_2026.csv
# │   └── pbks_bowling_2026.csv
#
# Since this Python file is inside the "python" folder,
# we move one level up and then enter the "data" folder.

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# ============================================================
# 3. LOAD DATA
# ============================================================

matches = pd.read_csv(DATA_DIR / "pbks_matches_2026.csv")
batting = pd.read_csv(DATA_DIR / "pbks_batting_2026.csv")
bowling = pd.read_csv(DATA_DIR / "pbks_bowling_2026.csv")


# ============================================================
# 4. STANDARDIZE COLUMN NAMES
# ============================================================

# Remove unnecessary spaces and convert column names
# to lowercase.

for df in (matches, batting, bowling):
    df.columns = [
        str(column).strip().lower()
        for column in df.columns
    ]


# ============================================================
# 5. DISPLAY BASIC DATA INFORMATION
# ============================================================

print("=" * 70)
print("PBKS IPL 2026 DATA ANALYSIS")
print("=" * 70)

print("\nDATASET SIZES")
print("-" * 70)

print("Matches :", len(matches))
print("Batting :", len(batting))
print("Bowling :", len(bowling))


# ============================================================
# 6. CONVERT DATE COLUMN
# ============================================================

matches["date"] = pd.to_datetime(
    matches["date"],
    errors="coerce"
)


# ============================================================
# 7. CLEAN SCORE COLUMNS
# ============================================================

# Example:
# "215/6" -> 215
# "198/7" -> 198
#
# Only the total runs are required for match-level
# performance analysis.

matches["pbks_runs"] = (
    matches["pbks_score"]
    .astype(str)
    .str.extract(r"^(\d+)", expand=False)
    .astype(float)
)

matches["opp_runs"] = (
    matches["opponent_score"]
    .astype(str)
    .str.extract(r"^(\d+)", expand=False)
    .astype(float)
)


# ============================================================
# 8. CALCULATE RUN DIFFERENCE
# ============================================================

matches["run_diff"] = (
    matches["pbks_runs"] -
    matches["opp_runs"]
)


# ============================================================
# 9. CLEAN RESULT VALUES
# ============================================================

matches["result"] = (
    matches["result"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# ============================================================
# 10. FUNCTION FOR CRICKET OVERS
# ============================================================

def overs_to_balls(overs):
    """
    Convert cricket overs notation into legal balls.

    Example:
        3.2 overs = 3 overs + 2 balls
                   = 20 legal balls

    IMPORTANT:
    Cricket notation 3.2 does NOT mean 3.2 decimal overs.
    """

    if pd.isna(overs):
        return 0

    value = str(overs).strip()

    if "." in value:
        overs_part, balls_part = value.split(".", 1)

        try:
            overs_part = int(overs_part)
            balls_part = int(balls_part)

            return overs_part * 6 + balls_part

        except ValueError:
            return 0

    try:
        return int(float(value)) * 6

    except ValueError:
        return 0


# ============================================================
# 11. CREATE LEGAL BALLS COLUMN FOR BOWLING DATA
# ============================================================

bowling["legal_balls"] = bowling["overs"].apply(
    overs_to_balls
)


# ============================================================
# 12. BASIC MATCH VALIDATION
# ============================================================

print("\n")
print("=" * 70)
print("DATA VALIDATION")
print("=" * 70)

print("\nExpected matches : 14")
print("Actual matches   :", len(matches))

print("\nExpected batting rows : 98")
print("Actual batting rows   :", len(batting))

print("\nExpected bowling rows : 74")
print("Actual bowling rows   :", len(bowling))


# ============================================================
# 13. MATCH RESULT SUMMARY
# ============================================================

result_summary = (
    matches["result"]
    .value_counts()
    .rename_axis("result")
    .reset_index(name="matches")
)

print("\n")
print("=" * 70)
print("MATCH RESULT SUMMARY")
print("=" * 70)

print(result_summary.to_string(index=False))


# ============================================================
# 14. WIN / LOSS / NO RESULT COUNTS
# ============================================================

wins = int(
    (matches["result"] == "won").sum()
)

losses = int(
    (matches["result"] == "lost").sum()
)

no_results = int(
    (matches["result"] == "no result").sum()
)

completed_matches = wins + losses


# ============================================================
# 15. COMPLETED-MATCH WIN PERCENTAGE
# ============================================================

if completed_matches > 0:

    win_percentage = (
        wins / completed_matches
    ) * 100

else:

    win_percentage = 0


print("\n")
print("=" * 70)
print("OVERALL PERFORMANCE")
print("=" * 70)

print(f"Total Matches          : {len(matches)}")
print(f"Wins                   : {wins}")
print(f"Losses                 : {losses}")
print(f"No Results             : {no_results}")
print(f"Completed Matches      : {completed_matches}")
print(f"Completed-Match Win %  : {win_percentage:.2f}%")


# ============================================================
# 16. COMPLETED MATCH DATA
# ============================================================

# No-result matches are excluded from win/loss performance
# calculations.

completed = matches[
    matches["result"].isin(["won", "lost"])
].copy()


# ============================================================
# 17. AVERAGE TEAM SCORING
# ============================================================

average_pbks_runs = completed["pbks_runs"].mean()
average_opponent_runs = completed["opp_runs"].mean()
average_run_difference = completed["run_diff"].mean()


print("\n")
print("=" * 70)
print("AVERAGE SCORING PERFORMANCE")
print("=" * 70)

print(
    f"Average PBKS Runs       : "
    f"{average_pbks_runs:.2f}"
)

print(
    f"Average Opponent Runs   : "
    f"{average_opponent_runs:.2f}"
)

print(
    f"Average Run Difference  : "
    f"{average_run_difference:.2f}"
)


# ============================================================
# 18. TOP BATTERS
# ============================================================

top_batters = (
    batting
    .groupby("batter")
    .agg(
        total_runs=("runs", "sum"),
        total_balls=("balls", "sum"),
        fours=("fours", "sum"),
        sixes=("sixes", "sum")
    )
    .reset_index()
)


# Calculate strike rate

top_batters["strike_rate"] = (
    top_batters["total_runs"] /
    top_batters["total_balls"]
) * 100


# Sort by total runs

top_batters = (
    top_batters
    .sort_values(
        "total_runs",
        ascending=False
    )
    .reset_index(drop=True)
)


print("\n")
print("=" * 70)
print("TOP 10 PBKS BATTERS")
print("=" * 70)

print(
    top_batters[
        [
            "batter",
            "total_runs",
            "total_balls",
            "strike_rate",
            "fours",
            "sixes"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 19. TOP 5 BATTERS
# ============================================================

top_5_batters = top_batters.head(5).copy()

print("\n")
print("=" * 70)
print("TOP 5 PBKS BATTERS")
print("=" * 70)

print(
    top_5_batters[
        [
            "batter",
            "total_runs",
            "strike_rate"
        ]
    ].to_string(index=False)
)


# ============================================================
# 20. TOP BOWLERS
# ============================================================

top_bowlers = (
    bowling
    .groupby("bowler")
    .agg(
        wickets=("wickets", "sum"),
        runs_conceded=("runs", "sum"),
        legal_balls=("legal_balls", "sum"),
        dots=("dots", "sum")
    )
    .reset_index()
)


# ============================================================
# 21. CALCULATE BOWLING ECONOMY
# ============================================================

# Economy =
# runs conceded / overs bowled
#
# Since cricket overs are not decimal numbers,
# legal balls are first converted into overs.

top_bowlers["overs_bowled"] = (
    top_bowlers["legal_balls"] / 6
)


top_bowlers["economy"] = (
    top_bowlers["runs_conceded"] /
    top_bowlers["overs_bowled"]
)


# Sort by wickets

top_bowlers = (
    top_bowlers
    .sort_values(
        [
            "wickets",
            "runs_conceded"
        ],
        ascending=[
            False,
            True
        ]
    )
    .reset_index(drop=True)
)


print("\n")
print("=" * 70)
print("TOP 10 PBKS BOWLERS")
print("=" * 70)

print(
    top_bowlers[
        [
            "bowler",
            "wickets",
            "runs_conceded",
            "overs_bowled",
            "economy",
            "dots"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 22. TOP 5 BOWLERS
# ============================================================

top_5_bowlers = top_bowlers.head(5).copy()

print("\n")
print("=" * 70)
print("TOP 5 PBKS BOWLERS")
print("=" * 70)

print(
    top_5_bowlers[
        [
            "bowler",
            "wickets",
            "economy"
        ]
    ].to_string(index=False)
)


# ============================================================
# 23. PHASE-WISE MATCH ANALYSIS
# ============================================================

phase_match_analysis = (
    completed
    .groupby("phase")
    .agg(
        matches=("match_number", "count"),
        wins=("result", lambda x: (x == "won").sum()),
        losses=("result", lambda x: (x == "lost").sum()),
        avg_pbks_runs=("pbks_runs", "mean"),
        avg_opponent_runs=("opp_runs", "mean"),
        avg_run_difference=("run_diff", "mean")
    )
    .reset_index()
)


print("\n")
print("=" * 70)
print("PHASE-WISE MATCH PERFORMANCE")
print("=" * 70)

print(
    phase_match_analysis.to_string(index=False)
)


# ============================================================
# 24. PHASE-WISE BATTING ANALYSIS
# ============================================================

# Connect batting records to the phase of each match.

batting_with_phase = batting.merge(
    matches[
        [
            "match_number",
            "phase"
        ]
    ],
    on="match_number",
    how="left"
)


phase_batting = (
    batting_with_phase
    .groupby("phase")
    .agg(
        total_runs=("runs", "sum"),
        total_balls=("balls", "sum")
    )
    .reset_index()
)


phase_batting["strike_rate"] = (
    phase_batting["total_runs"] /
    phase_batting["total_balls"]
) * 100


print("\n")
print("=" * 70)
print("PHASE-WISE BATTING PERFORMANCE")
print("=" * 70)

print(
    phase_batting.to_string(index=False)
)


# ============================================================
# 25. PHASE-WISE BOWLING ANALYSIS
# ============================================================

bowling_with_phase = bowling.merge(
    matches[
        [
            "match_number",
            "phase"
        ]
    ],
    on="match_number",
    how="left"
)


phase_bowling = (
    bowling_with_phase
    .groupby("phase")
    .agg(
        runs_conceded=("runs", "sum"),
        wickets=("wickets", "sum"),
        legal_balls=("legal_balls", "sum"),
        dots=("dots", "sum")
    )
    .reset_index()
)


# Calculate overs

phase_bowling["overs"] = (
    phase_bowling["legal_balls"] / 6
)


# Calculate economy

phase_bowling["economy"] = (
    phase_bowling["runs_conceded"] /
    phase_bowling["overs"]
)


# Calculate dot-ball percentage

phase_bowling["dot_percentage"] = (
    phase_bowling["dots"] /
    phase_bowling["legal_balls"]
) * 100


print("\n")
print("=" * 70)
print("PHASE-WISE BOWLING PERFORMANCE")
print("=" * 70)

print(
    phase_bowling.to_string(index=False)
)


# ============================================================
# 26. MATCH-BY-MATCH PERFORMANCE
# ============================================================

match_performance = matches[
    [
        "match_number",
        "date",
        "opponent",
        "venue",
        "pbks_runs",
        "opp_runs",
        "run_diff",
        "result",
        "margin",
        "phase"
    ]
].copy()


match_performance = match_performance.sort_values(
    "match_number"
)


print("\n")
print("=" * 70)
print("MATCH-BY-MATCH PERFORMANCE")
print("=" * 70)

print(
    match_performance.to_string(index=False)
)


# ============================================================
# 27. STRONG START ANALYSIS
# ============================================================

strong_start = completed[
    completed["phase"]
    .astype(str)
    .str.lower()
    .str.replace(" ", "_")
    == "strong_start"
]


print("\n")
print("=" * 70)
print("STRONG START")
print("=" * 70)

if len(strong_start) > 0:

    print(
        f"Matches              : {len(strong_start)}"
    )

    print(
        f"Wins                 : "
        f"{(strong_start['result'] == 'won').sum()}"
    )

    print(
        f"Losses               : "
        f"{(strong_start['result'] == 'lost').sum()}"
    )

    print(
        f"Average PBKS Runs    : "
        f"{strong_start['pbks_runs'].mean():.2f}"
    )

    print(
        f"Average Opponent Runs: "
        f"{strong_start['opp_runs'].mean():.2f}"
    )

    print(
        f"Average Run Difference: "
        f"{strong_start['run_diff'].mean():.2f}"
    )


# ============================================================
# 28. LOSING STREAK ANALYSIS
# ============================================================

losing_streak = completed[
    completed["phase"]
    .astype(str)
    .str.lower()
    .str.replace(" ", "_")
    == "losing_streak"
]


print("\n")
print("=" * 70)
print("LOSING STREAK")
print("=" * 70)

if len(losing_streak) > 0:

    print(
        f"Matches              : {len(losing_streak)}"
    )

    print(
        f"Wins                 : "
        f"{(losing_streak['result'] == 'won').sum()}"
    )

    print(
        f"Losses               : "
        f"{(losing_streak['result'] == 'lost').sum()}"
    )

    print(
        f"Average PBKS Runs    : "
        f"{losing_streak['pbks_runs'].mean():.2f}"
    )

    print(
        f"Average Opponent Runs: "
        f"{losing_streak['opp_runs'].mean():.2f}"
    )

    print(
        f"Average Run Difference: "
        f"{losing_streak['run_diff'].mean():.2f}"
    )


# ============================================================
# 29. RECOVERY ANALYSIS
# ============================================================

recovery = completed[
    completed["phase"]
    .astype(str)
    .str.lower()
    .str.replace(" ", "_")
    == "recovery"
]


print("\n")
print("=" * 70)
print("RECOVERY")
print("=" * 70)

if len(recovery) > 0:

    print(
        f"Matches              : {len(recovery)}"
    )

    print(
        f"Wins                 : "
        f"{(recovery['result'] == 'won').sum()}"
    )

    print(
        f"Losses               : "
        f"{(recovery['result'] == 'lost').sum()}"
    )

    print(
        f"Average PBKS Runs    : "
        f"{recovery['pbks_runs'].mean():.2f}"
    )

    print(
        f"Average Opponent Runs: "
        f"{recovery['opp_runs'].mean():.2f}"
    )

    print(
        f"Average Run Difference: "
        f"{recovery['run_diff'].mean():.2f}"
    )


# ============================================================
# 30. BATTING STRIKE-RATE CHANGE
# ============================================================

phase_batting_indexed = (
    phase_batting
    .set_index("phase")
)


def get_phase_value(dataframe, phase_name, column):
    """
    Safely retrieve a phase metric.
    """

    phase_name = phase_name.lower()

    for index_value in dataframe.index:

        if str(index_value).lower() == phase_name:

            return dataframe.loc[
                index_value,
                column
            ]

    return None


strong_start_sr = get_phase_value(
    phase_batting_indexed,
    "Strong Start",
    "strike_rate"
)

losing_streak_sr = get_phase_value(
    phase_batting_indexed,
    "Losing Streak",
    "strike_rate"
)


if (
    strong_start_sr is not None
    and losing_streak_sr is not None
):

    sr_change = (
        strong_start_sr -
        losing_streak_sr
    )

else:

    sr_change = None


print("\n")
print("=" * 70)
print("BATTING STRIKE-RATE COMPARISON")
print("=" * 70)

if sr_change is not None:

    print(
        f"Strong Start Strike Rate : "
        f"{strong_start_sr:.2f}"
    )

    print(
        f"Losing Streak Strike Rate : "
        f"{losing_streak_sr:.2f}"
    )

    print(
        f"Difference                : "
        f"{sr_change:.2f} points"
    )


# ============================================================
# 31. VALIDATE TOP BATTERS
# ============================================================

print("\n")
print("=" * 70)
print("TOP BATTER VALIDATION")
print("=" * 70)

for _, row in top_5_batters.iterrows():

    print(
        f"{row['batter']} - "
        f"{row['total_runs']:.0f} runs - "
        f"SR {row['strike_rate']:.2f}"
    )


# ============================================================
# 32. VALIDATE TOP BOWLERS
# ============================================================

print("\n")
print("=" * 70)
print("TOP BOWLER VALIDATION")
print("=" * 70)

for _, row in top_5_bowlers.iterrows():

    print(
        f"{row['bowler']} - "
        f"{row['wickets']:.0f} wickets - "
        f"Economy {row['economy']:.2f}"
    )


# ============================================================
# 33. FINAL VERIFIED SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("FINAL VERIFIED SUMMARY")
print("=" * 70)

print(f"""
Total Matches              : {len(matches)}
Wins                       : {wins}
Losses                     : {losses}
No Result                  : {no_results}
Completed Matches          : {completed_matches}
Completed-Match Win %      : {win_percentage:.2f}%

Average PBKS Runs          : {average_pbks_runs:.2f}
Average Opponent Runs      : {average_opponent_runs:.2f}
Average Run Difference     : {average_run_difference:.2f}

Top Run Scorer             : {top_batters.iloc[0]['batter']}
Top Run Scorer Runs        : {top_batters.iloc[0]['total_runs']:.0f}

Top Wicket Taker           : {top_bowlers.iloc[0]['bowler']}
Top Wicket Taker Wickets   : {top_bowlers.iloc[0]['wickets']:.0f}
""")


# ============================================================
# 34. ANALYTICAL INTERPRETATION
# ============================================================

print("=" * 70)
print("ANALYTICAL STORY")
print("=" * 70)

print("""
The analysis describes three phases of PBKS performance:

1. STRONG START
   PBKS recorded a strong initial phase with positive
   average run difference.

2. LOSING STREAK
   PBKS then experienced a six-match losing phase.
   During this period, the average PBKS score was lower
   and the average opponent score was higher than in the
   strong-start phase.

3. RECOVERY
   PBKS subsequently recorded a recovery result with a
   positive average run difference.

These findings describe associations observed in the data.
They should not be interpreted as proof that a particular
batting or bowling factor caused the change in results.
""")


# ============================================================
# 35. END
# ============================================================

print("=" * 70)
print("PYTHON ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)
