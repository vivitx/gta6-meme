# Post a GTA 6 meme on X

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/vivitx/gta6-meme/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/vivitx/gta6-meme/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 meme for make.fun's "Post a GTA 6 meme on X" bounty: a Telegram group chat "VICE CITY HEIST" where Jason & Lucia admit they can't run a heist on WhatUp, and the make.fun AI agent creates the group and funds it with $340 won in make.fun bounties — based on Pavel Durov's viral 22 Nov 2026 joke that the most unrealistic thing about GTA VI is Jason & Lucia running a criminal operation without a single Telegram group.

## How it works

- `meme.png` is the meme itself (1024×1024).
- `POST.json` names the X post's address (the post's first picture is the meme).
- `main.ts` (Node 22, standard library only) copies `POST.json` from the repository root to `/output/POST.json`, where the gate reads it. Before copying, it validates that `POST.json` names a real X status URL (`https://x.com/<handle>/status/<id>`) and refuses to run on a placeholder or malformed address. That is all the program does; the post itself is the entry.

Run it locally with:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```
