# GameDex — releases

Downloads for **GameDex**, a Steam library browser that shows how long each game
takes to finish, how far you got with its achievements, and what you have
already put into it.

This repository holds **releases only** — no source. Grab the newest build from
the [Releases](https://github.com/wimw85/GameDex/releases) page.

## Linux and Steam Deck

1. Download `GameDex-<version>.AppImage`.
2. Make it executable: `chmod +x GameDex-*.AppImage`
3. Run it.

On a Steam Deck, add it from Desktop Mode as a non-Steam game and it appears in
your library like anything else.

**It updates itself.** Every launch it checks here for a newer build, downloads
it in the background and applies it the next time you start. No connection, or
this page unreachable? It carries on with the version you have.

## What it needs from you

A Steam profile link and a free Steam Web API key — the app explains where to
get one. Everything is stored on your own machine: there is no account, no
server, and nothing leaves the device except the calls it makes to Steam on your
behalf.
