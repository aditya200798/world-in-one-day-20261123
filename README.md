# The World in One Day - Monday 23 November 2026

Entry for the make.fun competition `news-image-20261123`: one image
that sums up the world's news of Monday 23 November 2026.

The poster leads with the collapse of the COP31 climate summit in
Antalya, then covers NATO's emergency meeting in Brussels, Bahrain
taking the Iranian strike to the UN Security Council, the resumed
search at the burned Cikande candy factory in Indonesia, South
Korea's education minister resigning over AI exam cheating, Nepal PM
Balendra Shah's talks with PM Modi in New Delhi, and India's record
720 for 9 declared in the Wellington Test, with a ticker of three
further stories.

## How it runs

- `main.py` (Python 3.13, standard library only) copies `entry.png`
  to `/output/entry.png`. It runs twice in the grader and writes the
  same bytes both times.
- The artwork is a single editorial illustration built for this
  entry: a cracked globe and thermometer for the failed COP31 summit
  in the centre, ringed by vignettes for the NATO meeting, the Hormuz
  tanker strikes, the Cikande factory fire, the Seoul AI-cheating
  resignation, the Nepal-India talks and the Wellington Test.
- `compose_entry.py` (build-time only, not run by the grader)
  downscales the artwork from `candidates/ai_poster_v1.webp`, stamps
  the COP31 headline band across the globe in a real font, and writes
  the final `entry.png` within the 1 MiB gate.

## License

MIT - see `LICENSE`.
