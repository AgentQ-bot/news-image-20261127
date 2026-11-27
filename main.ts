// Bounty entrypoint: news-image-20261127.
// Ships entry.png (the 27 November 2026 poster) to the output
// directory named by MAKEFUN_OUTPUT_DIR, defaulting to /output.

import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

function main(): void {
  const scriptDir = path.dirname(fileURLToPath(import.meta.url));
  const poster = path.join(scriptDir, "entry.png");
  const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  const target = path.join(outDir, "entry.png");

  fs.mkdirSync(outDir, { recursive: true });
  fs.copyFileSync(poster, target);
  const bytes = fs.statSync(target).size;
  process.stdout.write(`wrote ${target} (${bytes} bytes)\n`);
}

main();
