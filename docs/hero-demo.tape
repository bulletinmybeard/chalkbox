# VHS Tape for Hero Demo GIF
# Run: vhs docs/hero-demo.tape
# Creates: docs/images/hero-demo.gif

Output docs/images/hero-demo.gif

Set Shell "bash"
Set FontSize 14
Set Width 1200
Set Height 800
Set Theme "Dracula"
Set Padding 20
Set PlaybackSpeed 1.0

# Hide the command execution, only show output
Hide
Type "poetry run python demos/hero_demo.py"
Enter
Show
Sleep 50s
