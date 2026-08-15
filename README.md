# Blyx — releases

Downloads for **Blyx**, a library browser for your games that shows how long
each one takes to finish, how far you got with its achievements or trophies,
what it costs on your wishlist today, and which drive it will install to. It
reads Steam and PlayStation, on a Steam Deck, a desktop and a phone.

- **What it does:** https://wimw85.github.io/Blyx/
- **Full manual:** https://wimw85.github.io/Blyx/manual/
- **Downloads:** [Releases](https://github.com/wimw85/Blyx/releases/latest)

This repository holds **releases, artwork and documentation only** — no source.

> Blyx was called GameDex until August 2026. Everything it had stored comes
> across on its own: the library, the playtime, the pinned matches, the
> settings. Backups made under the old name still import, and the backup folder
> in Google Drive is renamed rather than replaced.

## Which file

| Machine | File |
| --- | --- |
| Steam Deck or any Linux | `Blyx.AppImage` |
| Mac with Apple Silicon | `Blyx-<version>-arm64.dmg` |
| Mac with an Intel processor | `Blyx-<version>-x64.dmg` |
| Android phone or tablet | `Blyx-<version>.apk` |

## Download and install

1. Download `Blyx.AppImage` from the
   [latest release](https://github.com/wimw85/Blyx/releases/latest).
2. Put it somewhere it can stay, for example `~/Applications`.
3. Make it executable:

   ```bash
   chmod +x ~/Applications/Blyx.AppImage
   ```

4. Run it once from the file manager or the terminal to check it starts.

The file name never changes between versions, so a shortcut to it keeps working
across updates.

On a Mac, open the dmg and drag Blyx to Applications. On Android, allow your
browser to install unknown apps once, then open the APK.

## Adding it to Steam

From **Desktop Mode**: Steam → *Games* → *Add a Non-Steam Game to My Library* →
*Browse* → pick `Blyx.AppImage`.

Two settings on the shortcut matter.

### Compatibility: off

Right-click Blyx → *Properties* → *Compatibility*, and leave **Force the use of
a specific Steam Play compatibility tool** unticked. Proton runs Windows
programs; this is a Linux one. Forcing a compatibility tool is the most common
reason it refuses to start.

### Launch options for Game Mode

Not needed for most installs — try it without first. If Blyx opens in Desktop
Mode but shows a black screen or nothing at all in **Game Mode**, put this in
*Properties* → *Shortcut* → *Launch options*:

```
LD_PRELOAD= %command% --appimage-extract-and-run
```

| Part | What it does |
| --- | --- |
| `LD_PRELOAD=` | Empties the variable Steam fills with its overlay library. That library is injected into everything Steam starts, and it can stop an Electron window from ever appearing under gamescope. Emptying it costs you the Steam overlay inside Blyx, which Blyx has no use for. |
| `%command%` | Where Steam substitutes the actual program. Anything before it is environment, anything after it is an argument. |
| `--appimage-extract-and-run` | Unpacks the AppImage to a temporary folder and runs it from there, instead of mounting it through FUSE. Game Mode's session is a poor place to be mounting things. |

You do **not** need `--no-sandbox`. Every build wraps its own executable so the
flag is always passed; adding it by hand changes nothing.

## When it does not start

`~/.config/Blyx/startup.log` is written on every launch and records how far it
got, including the environment it found itself in. That file is the first place
to look, and the fastest thing to send along with a report. Installs that ran
under the old name have a `~/.config/GameDex/` beside it, holding logs from
before the rename.

A black screen with no log at all usually means a second copy is already
running: Blyx holds a single-instance lock, and a second launch hands focus to
the first window rather than opening another. Close it from the rail and start
again.

## It updates itself

New versions are fetched in the background and install on restart. A block
appears at the foot of the rail when one is ready. Settings shows the version
you are on and has a **Check for updates** button.

## Artwork for the shortcut

A non-Steam game has no artwork until someone gives it some. Every release
carries a set — capsule, wide capsule, hero and logo. In Steam: right-click
Blyx → *Manage* → *Set custom artwork*, once per slot. The hero deliberately
has no text on it, because Steam draws the logo over it.

The same files, plus a script that installs them for you, are in
[`steam-artwork/`](steam-artwork/).

## Credits

Blyx is a personal project. It is not made by, endorsed by, or connected to
Valve, Sony, HowLongToBeat, IsThereAnyDeal, SteamGridDB, SteamHunters or Google.
Steam and the Steam logo are trademarks of Valve Corporation; PlayStation is a
trademark of Sony Interactive Entertainment. The full list of what it reads and
who keeps it is in the app, under Settings → *Thanks & credits*.
