# GameDex — releases

Downloads for **GameDex**, a Steam library browser that shows how long each game
takes to finish, how far you got with its achievements, what it costs on your
wishlist today, and which drive it will install to.

- **What it does:** https://wimw85.github.io/GameDex/
- **Full manual:** https://wimw85.github.io/GameDex/manual/
- **Downloads:** [Releases](https://github.com/wimw85/GameDex/releases/latest)

This repository holds **releases, artwork and documentation only** — no source.

## Download and install

1. Download `GameDex.AppImage` from the
   [latest release](https://github.com/wimw85/GameDex/releases/latest).
2. Put it somewhere it can stay, for example `~/Applications`.
3. Make it executable:

   ```bash
   chmod +x ~/Applications/GameDex.AppImage
   ```

4. Run it once from the file manager or the terminal to check it starts.

The file name never changes between versions, so a shortcut to it keeps working
across updates.

## Adding it to Steam

From **Desktop Mode**: Steam → *Games* → *Add a Non-Steam Game to My Library* →
*Browse* → pick `GameDex.AppImage`.

Two settings on the shortcut matter.

### Compatibility: off

Right-click GameDex → *Properties* → *Compatibility*, and leave
**Force the use of a specific Steam Play compatibility tool** unticked. Proton
runs Windows programs; this is a Linux one. Forcing a compatibility tool is the
most common reason it refuses to start.

### Launch options for Game Mode

Not needed for most installs — try it without first. If GameDex opens in Desktop
Mode but shows a black screen or nothing at all in **Game Mode**, put this in
*Properties* → *Shortcut* → *Launch options*:

```
LD_PRELOAD= %command% --appimage-extract-and-run
```

| Part | What it does |
| --- | --- |
| `LD_PRELOAD=` | Empties the variable Steam fills with its overlay library. That library is injected into everything Steam starts, and it can stop an Electron window from ever appearing under gamescope. Emptying it costs you the Steam overlay inside GameDex, which GameDex has no use for. |
| `%command%` | Where Steam substitutes the actual program. Anything before it is environment, anything after it is an argument. |
| `--appimage-extract-and-run` | Unpacks the AppImage to a temporary folder and runs it from there, instead of mounting it through FUSE. Game Mode's session is a poor place to be mounting things. |

You do **not** need `--no-sandbox`. Every build wraps its own executable so the
flag is always passed; adding it by hand changes nothing.

## When it does not start

`~/.config/GameDex/startup.log` is written on every launch and records how far it
got, including the environment it found itself in. That file is the first place
to look, and the fastest thing to send along with a report.

A black screen with no log at all usually means a second copy is already
running: GameDex holds a single-instance lock, and a second launch hands focus to
the first window rather than opening another. Close it from the rail and start
again.

## It updates itself

New versions are fetched in the background and install on restart. A block
appears at the foot of the rail when one is ready. Settings shows the version you
are on and has a **Check for updates** button.

## Artwork for the shortcut

A non-Steam game has no artwork until someone gives it some. Every release
carries a set — capsule, wide capsule, hero and logo. In Steam: right-click
GameDex → *Manage* → *Set custom artwork*, once per slot. The hero deliberately
has no text on it, because Steam draws the logo over it.

The same files, plus a script that installs them for you, are in
[`steam-artwork/`](steam-artwork/).

## Credits

GameDex is a personal project. It is not made by, endorsed by, or connected to
Valve, HowLongToBeat, IsThereAnyDeal, SteamHunters or Google. Steam and the Steam
logo are trademarks of Valve Corporation. The full list of what it reads and who
keeps it is in the app, under Settings → *Thanks & credits*.
