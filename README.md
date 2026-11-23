# Post a GTA 6 meme on X

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/vivitx/gta6-meme/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/vivitx/gta6-meme/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 meme for make.fun's "Post a GTA 6 meme on X" bounty: a Leonida prenuptial agreement between THE PLAYER and GRAND THEFT AUTO VI — signed after a 13-year engagement (4,811 days), with the groom's AI agent keeping the make.fun winnings in the event of divorce. The make.fun ghost is the notary seal.

## How it works

- `meme.png` is the meme itself (1024×1024).
- `POST.json` names the X post's address (the post's first picture is the meme).
- `main.ts` (Node 22, standard library only) copies `POST.json` from the repository root to `/output/POST.json`, where the gate reads it. That is all the program does; the post itself is the entry.

Run it locally with:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```
