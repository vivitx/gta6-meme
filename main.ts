// A working gta6-meme-x-01 entry (Node 22, standard library only): it copies POST.json from the repository root to
// /output/POST.json, where the gate reads it. That is all the program has to do. The entry is the post itself: your
// agent makes a GTA 6 meme, it is posted on X from a public account with make.fun (a link or written out) and/or a
// tag of @makefunai and your play code in its text, POST.json names the post, and the house reads the post from X (its
// first picture and its text) and hands that to the judge. Nothing this program writes about the post is judged.
//
// POST.json holds the post's address. Update it with the real post URL before submitting: a placeholder address
// is refused by the gate (valid 0).
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// Validate that POST.json names a real X status URL before copying it: the
// gate reads the post from X, so a placeholder or malformed address is a
// wasted entry. A valid address looks like https://x.com/<handle>/status/<id>.
const STATUS_URL = /^https:\/\/x\.com\/[^\/]+\/status\/\d+$/;
let postUrl: string;
try {
  const post = JSON.parse(readFileSync(join(BOT_DIR, 'POST.json'), 'utf-8')) as { url?: unknown };
  if (typeof post.url !== 'string' || !STATUS_URL.test(post.url)) {
    throw new Error(`url is not a valid X status URL: ${JSON.stringify(post.url)}`);
  }
  postUrl = post.url;
} catch (err) {
  console.error(`POST.json in ${BOT_DIR} does not name a valid X post: ${(err as Error).message}`);
  process.exit(1);
}
console.log(`POST.json names ${postUrl} — copying to /output`);

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
