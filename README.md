# GameDex — releases

Downloads for **GameDex**, a Steam library browser that shows how long each game
takes to finish, how far you got with its achievements, and what you have
already put into it.

This repository holds **releases and artwork only** — no source. Grab the newest
build from the [Releases](https://github.com/wimw85/GameDex/releases) page.

## Running it

1. Download `GameDex.AppImage`.
2. Make it executable: `chmod +x GameDex.AppImage`
3. Run it.

The file name never changes, so a shortcut to it keeps working across updates.

## Adding it to Steam, including a Steam Deck

Add the AppImage from Desktop Mode as a non-Steam game, then set two things on
the shortcut:

**Compatibility: off.** Proton runs Windows programs; this is a Linux one.
Forcing a compatibility tool is the most common reason it will not start.

**Launch options:**

```
LD_PRELOAD= %command% --appimage-extract-and-run
```

`LD_PRELOAD=` drops Steam's overlay for this app. The overlay is injected into
every game Steam starts, and on this one it stopped the window from ever
appearing — the app ran, Steam spun, and even Steam's own stop button could not
end it. `--appimage-extract-and-run` sidesteps FUSE, which Game Mode does not
always provide.

With those two set, it runs in Desktop Mode and in Game Mode alike — measured on
a real Deck.

**If it still shows nothing**, `~/.config/GameDex/startup.log` is written on
every launch and says how far it got.

## Artwork for the shortcut

A non-Steam game has no artwork until someone gives it some. Every release
carries a set — capsule, wide capsule, hero and logo. In Steam: right-click
GameDex → *Manage* → *Set custom artwork*, once per slot. The hero deliberately
has no text on it, because Steam draws the logo over it.

The same files, plus a script that installs them for you, are in
[`steam-artwork/`](steam-artwork/).

## It updates itself

Every launch it checks here for a newer build, downloads it in the background and
applies it the next time you start. Settings shows which version is running and
can check on demand. No connection, or this page unreachable? It carries on with
the version you have.

## What it needs from you

A Steam profile link and a free Steam Web API key — the app explains where to get
one. On a desktop it reads the account you are already signed in as, so there is
nothing to look up.

Everything is stored on your own machine: there is no account, no server, and
nothing leaves the device except the calls it makes to Steam on your behalf.
