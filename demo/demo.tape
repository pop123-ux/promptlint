# promptlint demo — renders a clean GIF with VHS (https://github.com/charmbracelet/vhs)
#
#   1. Install VHS:  winget install charmbracelet.vhs   (or: brew install vhs)
#   2. From the repo root, run:  vhs demo/demo.tape
#   3. Output: demo/promptlint-demo.gif
#
# Run from the repository root so the examples/ path resolves.

Output demo/promptlint-demo.gif

Set Shell bash
Set FontSize 18
Set Width 1200
Set Height 700
Set Theme "Catppuccin Mocha"
Set Padding 24
Set TypingSpeed 55ms

Type "# promptlint — ESLint for your LLM prompts"
Enter
Sleep 900ms

Type "FORCE_COLOR=1 python -m promptlint examples/bad_prompt.py"
Sleep 600ms
Enter
Sleep 4.5s

Type 'echo "exit code: $?"'
Enter
Sleep 2.5s
