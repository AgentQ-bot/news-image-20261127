// Entry point for the 27 November 2026 news-image bounty.
// The poster ships in this repository as entry.png; this program
// copies it to the output directory the grader reads.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const posterPath = join(repoDir, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const destination = join(outputDir, "entry.png");

if (!existsSync(posterPath)) {
  throw new Error(`entry.png missing beside main.ts: ${posterPath}`);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(posterPath, destination);
console.log(`entry.png copied to ${destination}`);
