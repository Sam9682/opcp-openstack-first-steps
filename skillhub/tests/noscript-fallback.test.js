/**
 * @vitest-environment jsdom
 *
 * Example test for the SCO noscript fallback.
 *
 * Requirement 3.5: WHERE scripting is disabled, THE SCO SHALL present a
 * noscript fallback that links to the `en/` and `fr/` locale entry points.
 *
 * The SCO entry is `skillhub/index.html`. This test reads that file from disk
 * and parses it with jsdom, then asserts that it contains a <noscript> element
 * whose links point to the English and French locale entry points. The
 * fallback is what a learner sees when JavaScript (and therefore the locale
 * auto-redirect) is unavailable, so it must offer a direct path into each
 * locale.
 *
 * Validates: Requirements 3.5
 */

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

import { describe, expect, it } from "vitest";
import { JSDOM } from "jsdom";

const __dirname = dirname(fileURLToPath(import.meta.url));
const INDEX_HTML_PATH = resolve(__dirname, "..", "index.html");

/**
 * Parse the SCO entry HTML into a document.
 *
 * @returns {Document} The parsed index.html document.
 */
function loadScoDocument() {
  const html = readFileSync(INDEX_HTML_PATH, "utf8");
  return new JSDOM(html).window.document;
}

describe("SCO noscript fallback (Req 3.5)", () => {
  it("index.html contains a <noscript> element", () => {
    const doc = loadScoDocument();
    const noscript = doc.querySelector("noscript");
    expect(noscript).not.toBeNull();
  });

  it("the noscript fallback links to the en/ locale entry point", () => {
    const doc = loadScoDocument();
    const noscript = doc.querySelector("noscript");
    expect(noscript).not.toBeNull();

    // jsdom does not parse the inner markup of <noscript> into live elements,
    // so inspect its text content for the locale entry hrefs.
    const markup = noscript.textContent + noscript.innerHTML;
    expect(markup).toContain("en/index.html");
  });

  it("the noscript fallback links to the fr/ locale entry point", () => {
    const doc = loadScoDocument();
    const noscript = doc.querySelector("noscript");
    expect(noscript).not.toBeNull();

    const markup = noscript.textContent + noscript.innerHTML;
    expect(markup).toContain("fr/index.html");
  });

  it("the noscript fallback links to both locale entry points", () => {
    const doc = loadScoDocument();
    const noscript = doc.querySelector("noscript");
    expect(noscript).not.toBeNull();

    // Re-parse the noscript inner markup as a document fragment so the links
    // are available as real anchor elements, then assert both entry points
    // are present as hrefs.
    const inner = new JSDOM(`<!DOCTYPE html><body>${noscript.innerHTML}</body>`)
      .window.document;
    const hrefs = Array.from(inner.querySelectorAll("a[href]")).map((a) =>
      a.getAttribute("href"),
    );

    expect(hrefs).toContain("en/index.html");
    expect(hrefs).toContain("fr/index.html");
  });
});
