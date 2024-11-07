from effect2 import HorizontalCycle

effect = HorizontalCycle("Pulsing Text")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
