Skipped Songs by Time Bucket = 
VAR Bucket = SELECTEDVALUE(TimeBuckets[Bucket])
RETURN
SWITCH(
    TRUE(),
    Bucket = "< 5 sec",
        CALCULATE(
            COUNTROWS(SpotifyData),
            SpotifyData[ms_played] < 5000,
            SpotifyData[skipped] = TRUE()
        ),
    Bucket = "5 – 15 sec",
        CALCULATE(
            COUNTROWS(SpotifyData),
            SpotifyData[ms_played] >= 5000,
            SpotifyData[ms_played] < 15000,
            SpotifyData[skipped] = TRUE()
        ),
    Bucket = "15 – 30 sec",
        CALCULATE(
            COUNTROWS(SpotifyData),
            SpotifyData[ms_played] >= 15000,
            SpotifyData[ms_played] < 30000,
            SpotifyData[skipped] = TRUE()
        ),
    BLANK()
)
