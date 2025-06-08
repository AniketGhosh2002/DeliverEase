% Skipped by Timeframe = 
VAR Bucket = SELECTEDVALUE(SkipTimeFrame[Bucket])
VAR Total = 
    CALCULATE(
        COUNTROWS(Spotify),
        Spotify[ms_played] < 30000
    )
VAR SkippedCount =
    SWITCH(
        TRUE(),
        Bucket = "< 5 sec",
            CALCULATE(
                COUNTROWS(Spotify),
                Spotify[skipped] = TRUE(),
                Spotify[ms_played] < 5000
            ),
        Bucket = "5 – 15 sec",
            CALCULATE(
                COUNTROWS(Spotify),
                Spotify[skipped] = TRUE(),
                Spotify[ms_played] >= 5000,
                Spotify[ms_played] < 15000
            ),
        Bucket = "15 – 30 sec",
            CALCULATE(
                COUNTROWS(Spotify),
                Spotify[skipped] = TRUE(),
                Spotify[ms_played] >= 15000,
                Spotify[ms_played] < 30000
            ),
        BLANK()
    )
RETURN 
DIVIDE(SkippedCount, Total, 0)
