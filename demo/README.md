# Recording the promptlint demo GIF

A short demo GIF at the top of the README is the single biggest star-converter
for a dev tool. Two ways to make one — pick whichever is easier for you.

## Option A — VHS (reproducible, recommended)

[VHS](https://github.com/charmbracelet/vhs) records a terminal from a script,
so the result is crisp and identical every time.

```bash
# 1. Install VHS
winget install charmbracelet.vhs      # Windows
# brew install vhs                    # macOS

# 2. From the repo root, render the tape
vhs demo/demo.tape

# 3. Output lands at demo/promptlint-demo.gif
```

The script (`demo/demo.tape`) is already written. Tweak font size, theme, or
timing in that file if you want a different look.

## Option B — ScreenToGif (point-and-click, Windows)

1. Install [ScreenToGif](https://www.screentogif.com/) (free).
2. Open a clean terminal in the repo folder, maximize font size for legibility.
3. Hit **Record**, then run:
   ```bash
   FORCE_COLOR=1 python -m promptlint examples/bad_prompt.py
   ```
   (or just `promptlint examples/bad_prompt.py` if installed)
4. Stop after the output + a 2s pause. In the editor, trim to ~12–15s and
   **File → Save as → GIF**. Save it as `demo/promptlint-demo.gif`.

## Tips for a good demo

- Keep it **under ~15 seconds** — people scan, they don't watch.
- Big font (18–22pt), dark theme, high contrast.
- Show the *payoff*: the colored PL001–PL006 findings and the non-zero exit code.
- Once saved, it auto-appears in the README (the image link already points to it).
- Optional: also drop the GIF into the GitHub Release and the Show HN comment.
