# Steam artwork

Four images for the GameDex shortcut in Steam, generated from the app's own icon
and the wordmark lifted out of its splash screen — so the type is the real thing
rather than something close to it.

| File | Slot | Size |
| --- | --- | --- |
| `grid-portrait-600x900.png` | The tall capsule in the library list | 600 × 900 |
| `grid-landscape-920x430.png` | The wide capsule | 920 × 430 |
| `hero-1920x620.png` | The banner on the game's page | 1920 × 620 |
| `logo.png` | The wordmark Steam lays over the hero | 1000 × 217, transparent |

The hero deliberately carries no text: Steam draws the logo over it, and two
wordmarks in one banner collide.

## Steam will not find these on its own

A non-Steam shortcut has no artwork until someone gives it some. Steam reads a
folder of PNGs named after the shortcut's own id — that is the only hook, and
nothing inside an AppImage can reach it.

Two ways to fill it:

**By hand.** In Steam, right-click GameDex → *Manage* → *Set custom artwork*, once
per slot.

**In one command.** On the Deck, in Desktop Mode, after adding GameDex to Steam:

```bash
python3 install-artwork.py
```

It finds the shortcut, works out its id and copies all four files into
`userdata/<account>/config/grid/`. Restart Steam afterwards. It never touches the
shortcut itself — the worst it can do is leave four files in a cache folder.

## Regenerating

The images are built from `docs/gamedex-icon-1024.png` and
`docs/splash_1440x2560_v2.png`. The wordmark is cut out by turning its own
brightness into transparency, which keeps the antialiasing intact; a threshold
would leave ragged edges.
