/**
 * @vitest-environment node
 *
 * Non-invasiveness byte-comparison tests for the SkillHub SCORM 1.2 export.
 *
 * Requirement 7.4 states the Scorm_Runtime SHALL leave the existing course
 * modules `progress.js`, `self-assessment.js`, and `i18n.js` and the lesson HTML
 * files unmodified. This test drives the real `buildScormPackage` into a
 * throwaway temp directory and byte-compares the course files between the source
 * tree (`skillhub/`) and the built Output_Dir.
 *
 * Two kinds of files are checked, reflecting what the build actually does:
 *
 *   1. Course JS modules and other static assets (css/js/images). The build
 *      copies these trees VERBATIM — it never rewrites course logic — so every
 *      byte must match. The three modules named in Req 7.4
 *      (`progress.js`, `self-assessment.js`, `i18n.js`) are checked here: for
 *      each, if the source file exists its output copy must be byte-identical,
 *      and if it is absent in the source it must be equally absent in the output
 *      (the build neither fabricates nor mutates a course module).
 *
 *   2. Lesson / index HTML pages. These are the ONE deliberate exception: the
 *      build's `injectBootstrapScript` step inserts a single
 *      `<script type="module" src=".../js/scorm/scorm-bootstrap.js">` tag before
 *      `</body>` so the SCO can load the runtime. That injected tag is the SCORM
 *      wiring, not a change to course content. To assert non-invasiveness we
 *      verify the ONLY difference is that one injected tag: removing exactly the
 *      injected bootstrap `<script>` fragment from the output HTML must yield a
 *      byte-for-byte match with the source HTML. Any other divergence (edited
 *      copy, rewritten lesson content) would fail this check.
 *
 * The injected fragment is reconstructed from the build's own
 * `bootstrapTagForDepth` helper and the exact insertion format used by
 * `injectBootstrapIntoHtml` (four leading spaces + the tag + a trailing newline,
 * placed immediately before `</body>`), so the test tracks the real build
 * behavior rather than a hand-copied string.
 *
 * Validates: Requirements 7.4
 */

import { afterEach, beforeAll, afterAll, describe, expect, it } from "vitest";
import fs from "node:fs/promises";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";

import {
  buildScormPackage,
  bootstrapTagForDepth,
  BOOTSTRAP_SRC_MARKER,
} from "../../scripts/build-scorm.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** The real SkillHub course source tree (skillhub/). */
const SRC_DIR = path.resolve(__dirname, "..");

/** The three course modules Req 7.4 names explicitly, relative to SRC_DIR. */
const NAMED_COURSE_MODULES = [
  "assets/js/progress.js",
  "assets/js/self-assessment.js",
  "assets/js/i18n.js",
];

/** True when `p` exists and is a regular file. */
async function isFile(p) {
  try {
    return (await fs.stat(p)).isFile();
  } catch {
    return false;
  }
}

/** Read a file as raw bytes, or null when it does not exist. */
async function readBytes(p) {
  try {
    return await fs.readFile(p);
  } catch {
    return null;
  }
}

/**
 * Reconstruct the exact fragment `injectBootstrapScript` inserts into an HTML
 * page at the given folder depth. Mirrors `injectBootstrapIntoHtml`: four spaces,
 * the depth-aware bootstrap <script> tag, then a newline — inserted immediately
 * before `</body>`.
 * @param {number} depth
 * @returns {string}
 */
function injectedFragment(depth) {
  return `    ${bootstrapTagForDepth(depth)}\n`;
}

/**
 * Remove exactly one occurrence of the injected bootstrap fragment that sits
 * immediately before `</body>`, returning the HTML as the source should have
 * looked before injection. Returns the string unchanged when the fragment is
 * absent.
 * @param {string} html   The built (output) HTML.
 * @param {number} depth  The page's folder depth (0 for root, 1 for en//fr/).
 * @returns {string}
 */
function stripInjectedBootstrap(html, depth) {
  const fragment = injectedFragment(depth);
  const needle = `${fragment}</body>`;
  const idx = html.lastIndexOf(needle);
  if (idx === -1) return html;
  return html.slice(0, idx) + "</body>" + html.slice(idx + needle.length);
}

/** Recursively list regular files under `dir` as POSIX paths relative to it. */
async function listFiles(dir, base = dir, out = []) {
  let entries;
  try {
    entries = await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const entry of entries) {
    const abs = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      await listFiles(abs, base, out);
    } else {
      out.push(path.relative(base, abs).split(path.sep).join("/"));
    }
  }
  return out;
}

describe("Non-invasiveness: course files unmodified by build/runtime injection (Req 7.4)", () => {
  /** @type {string} */
  let outDir;

  beforeAll(async () => {
    outDir = await fs.mkdtemp(path.join(os.tmpdir(), "scorm-noninvasive-"));
    await buildScormPackage({ srcDir: SRC_DIR, outDir, labName: "skillhub" });
  });

  afterAll(async () => {
    if (outDir) {
      await fs.rm(outDir, { recursive: true, force: true });
    }
    outDir = undefined;
  });

  describe("named course modules progress.js / self-assessment.js / i18n.js", () => {
    it("each named module is byte-identical in the output, or equally absent in both trees", async () => {
      for (const rel of NAMED_COURSE_MODULES) {
        const srcPath = path.join(SRC_DIR, rel);
        const outPath = path.join(outDir, rel);

        const srcBytes = await readBytes(srcPath);
        const outBytes = await readBytes(outPath);

        if (srcBytes === null) {
          // The module does not exist in the course source. Non-invasiveness
          // means the build must not fabricate it either.
          expect(
            outBytes,
            `${rel} is absent in the source so it must be absent in the output`,
          ).toBeNull();
        } else {
          // The module exists in the source: the build must copy it verbatim.
          expect(
            outBytes,
            `${rel} exists in the source so it must be present in the output`,
          ).not.toBeNull();
          expect(
            outBytes.equals(srcBytes),
            `${rel} must be byte-identical between source and output`,
          ).toBe(true);
        }
      }
    });
  });

  describe("static course assets (css / js / images) copied verbatim", () => {
    it("every file under assets/ is byte-identical between source and output", async () => {
      const assetFiles = await listFiles(path.join(SRC_DIR, "assets"));
      // Guard: there is actually something to compare.
      expect(assetFiles.length).toBeGreaterThan(0);

      for (const rel of assetFiles) {
        const srcBytes = await readBytes(path.join(SRC_DIR, "assets", rel));
        const outBytes = await readBytes(path.join(outDir, "assets", rel));
        expect(outBytes, `assets/${rel} must exist in the output`).not.toBeNull();
        expect(
          outBytes.equals(srcBytes),
          `assets/${rel} must be byte-identical (verbatim copy)`,
        ).toBe(true);
      }
    });

    it("every non-SCORM course JS module under js/ is byte-identical (runtime-only additions aside)", async () => {
      // The build injects the SCORM runtime under js/scorm/. Any OTHER js/ file
      // that exists in the source is course code and must be copied verbatim.
      const jsFiles = await listFiles(path.join(SRC_DIR, "js"));
      for (const rel of jsFiles) {
        const srcBytes = await readBytes(path.join(SRC_DIR, "js", rel));
        const outBytes = await readBytes(path.join(outDir, "js", rel));
        expect(outBytes, `js/${rel} must exist in the output`).not.toBeNull();
        expect(
          outBytes.equals(srcBytes),
          `js/${rel} must be byte-identical (verbatim copy)`,
        ).toBe(true);
      }
    });
  });

  describe("lesson / index HTML pages differ only by the injected bootstrap tag", () => {
    /**
     * Build the list of HTML pages the build injects into, with their folder
     * depth: the root index.html (depth 0) and every .html page under en/ and
     * fr/ (depth 1).
     * @returns {Promise<Array<{rel: string, depth: number}>>}
     */
    async function injectedHtmlPages() {
      const pages = [{ rel: "index.html", depth: 0 }];
      for (const locale of ["en", "fr"]) {
        const localeDir = path.join(SRC_DIR, locale);
        let entries;
        try {
          entries = await fs.readdir(localeDir, { withFileTypes: true });
        } catch {
          continue;
        }
        for (const entry of entries) {
          if (entry.isFile() && entry.name.toLowerCase().endsWith(".html")) {
            pages.push({ rel: `${locale}/${entry.name}`, depth: 1 });
          }
        }
      }
      return pages;
    }

    it("stripping the injected bootstrap <script> makes every HTML page byte-identical to its source", async () => {
      const pages = await injectedHtmlPages();
      // Guard: we really are comparing the index plus both locale lesson sets.
      expect(pages.length).toBeGreaterThan(1);
      expect(pages.some((p) => p.rel.startsWith("en/"))).toBe(true);
      expect(pages.some((p) => p.rel.startsWith("fr/"))).toBe(true);

      for (const { rel, depth } of pages) {
        const srcHtml = await fs.readFile(path.join(SRC_DIR, rel), "utf8");
        const outHtml = await fs.readFile(path.join(outDir, rel), "utf8");

        // The output must carry exactly one bootstrap reference...
        const marker = BOOTSTRAP_SRC_MARKER;
        const occurrences = outHtml.split(marker).length - 1;
        expect(occurrences, `${rel} should reference the bootstrap exactly once`).toBe(1);

        // ...and the source must carry none (the runtime is injected, not authored).
        expect(
          srcHtml.includes(marker),
          `${rel} source must not reference the SCORM bootstrap`,
        ).toBe(false);

        // Removing exactly the injected fragment restores the source byte-for-byte.
        const stripped = stripInjectedBootstrap(outHtml, depth);
        expect(
          stripped,
          `${rel}: the only difference must be the injected bootstrap tag`,
        ).toBe(srcHtml);
      }
    });
  });
});
