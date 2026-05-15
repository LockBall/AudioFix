# ToDo

## Vorbis Peak Refinement
- Compare Vorbis output using quality mode (`-q:a`, for example `5` or `6`) instead of source bitrate mode (`-b:a`) to see whether encoded peak behavior is more stable.
- Keep source sample rate and channel count fixed while testing encoder changes.
- Replace simple peak-error correction with a candidate gain sweep around the first-pass gain.
- Decide the selection rule for candidate gains: closest to `0.00 dB`, or closest without exceeding `0.00 dB`.
- Revisit the default headroom/tolerance/search-step values after testing more Ogg Vorbis source files.
- Compare AudioFix results against GoldWave after each encoder/refinement change using the same source file.
