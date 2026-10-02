/**
 * @vitest-environment node
 *
 * Example tests for the SCORM Build_Process: build-error reporting and
 * imsmanifest.xml structure.
 *
 * These tests drive the real build (`buildScormPackage`) against a temporary
 * output directory under the OS temp dir, then parse the emitted
 * `imsmanifest.xml` with jsdom's XML parser and assert its structure. They also
 * exercise the error path (missing required source) and the clean() sibling
 * preservation contract.
 *
 * Covered acceptance criteria:
 *   1.2 clean() leaves sibling `./scorm/*.zip` and `./scorm/*.md` untouched
 *   1.5 a missing required source path throws and names the path (non-zero exit)
 *   2.2 exactly one organization / item / resource
 *   2.3 resource declares adlcp:scormtype="sco" and href="index.html"
 *   2.4 index.html listed as a file dependency of the SCO resource
 *   2.6 manifest references the SCORM 1.2 schema versions matching the schema files
 *   3.5 the built index.html presents a noscript fallback (en/ and fr/ links)
 *
 * Validates: Requirements 1.2, 1.5, 2.2, 2.3, 2.4, 2.6
 */

import { afterAll, afterEach, beforeAll, describe, expect, it } from "vitest";
import { JSDOM } from "jsdom";
import fs from "node:fs/promises";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";

import {
  buildScormPackage,
  copyCourseContent,
  clean,
  renderManifest,
  SCHEMA_FILES,
} from "../../scripts/build-scorm.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
/** The real SkillHub course source tree (skillhub/). */
const SRC_DIR = path.resolve(__dirname, "..");

/** Temp directories created during the run, cleaned up in afterEach. */
const tempDirs = [];

/**
 * Create a unique temporary working directory under the OS temp dir and track
 * it for cleanup.
 * @returns {Promise<string>} absolute path to the created directory.
 */
async function makeTempDir() {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "scorm-build-test-"));
  tempDirs.push(dir);
  return dir;
}

/**
 * Parse an XML string into a Document using jsdom's XML content type so element
 * and attribute lookups (including the adlcp: namespaced attribute) behave like
 * a real XML parser.
 * @param {string} xml
 * @returns {Document}
 */
function parseXml(xml) {
  return new JSDOM(xml, { contentType: "application/xml" }).window.document;
}

afterEach(async () => {
  while (tempDirs.length) {
    const dir = tempDirs.pop();
    await fs.rm(dir, { recursive: true, force: true });
  }
});

describe("Build_Process error reporting (Req 1.5)", () => {
  it("copyCourseContent throws naming the missing path when index.html is absent", async () => {
    // A source tree that is missing the required index.html entry.
    const srcDir = await makeTempDir();
    const outDir = await makeTempDir();

    await expect(copyCourseContent(srcDir, outDir)).rejects.toThrow(
      /index\.html/,
    );
  });

  it("buildScormPackage rejects and names the missing path for a bad source dir", async () => {
    // Point the build at an empty source dir — the first required entry is
    // index.html, so the rejection must name it. A rejected promise here is
    // what drives the CLI's non-zero exit code (Req 1.5).
    const badSrc = await makeTempDir();
    const outDir = await makeTempDir();

    let error;
    try {
      await buildScormPackage({ srcDir: badSrc, outDir, labName: "skillhub" });
    } catch (err) {
      error = err;
    }

    expect(error).toBeInstanceOf(Error);
    expect(error.message).toMatch(/index\.html/);
  });
});

describe("Build_Process clean() preserves siblings (Req 1.2)", () => {
  it("sentinel ./scorm/*.zip and ./scorm/*.md siblings survive a clean", async () => {
    // Model the ./scorm directory: the Output_Dir plus sibling artifacts.
    const scormDir = await makeTempDir();
    const outDir = path.join(scormDir, "skillhub_scorm");
    await fs.mkdir(outDir, { recursive: true });

    // Pre-existing package content that clean() should wipe.
    await fs.writeFile(path.join(outDir, "stale.txt"), "old", "utf8");

    // Sentinel siblings next to the Output_Dir.
    const zipSibling = path.join(scormDir, "skillhub_scorm.zip");
    const mdSibling = path.join(scormDir, "README.md");
    await fs.writeFile(zipSibling, "zip-bytes", "utf8");
    await fs.writeFile(mdSibling, "# notes", "utf8");

    await clean(outDir);

    // Output_Dir exists and is empty (stale content removed).
    const outEntries = await fs.readdir(outDir);
    expect(outEntries).toEqual([]);

    // Siblings are untouched — same content as before.
    await expect(fs.readFile(zipSibling, "utf8")).resolves.toBe("zip-bytes");
    await expect(fs.readFile(mdSibling, "utf8")).resolves.toBe("# notes");

    // And they are still present as siblings in the parent directory.
    const scormEntries = await fs.readdir(scormDir);
    expect(scormEntries).toContain("skillhub_scorm.zip");
    expect(scormEntries).toContain("README.md");
  });
});

describe("imsmanifest.xml structure (Req 2.2, 2.3, 2.4, 2.6)", () => {
  let outDir;
  let manifestXml;
  let manifestDoc;

  beforeAll(async () => {
    // This directory is shared across every test in the block and is cleaned
    // up in afterAll — it must NOT be registered in the per-test `tempDirs`
    // list, whose entries the afterEach hook removes between tests.
    outDir = await fs.mkdtemp(path.join(os.tmpdir(), "scorm-build-manifest-"));
    await buildScormPackage({ srcDir: SRC_DIR, outDir, labName: "skillhub" });
    manifestXml = await fs.readFile(
      path.join(outDir, "imsmanifest.xml"),
      "utf8",
    );
    manifestDoc = parseXml(manifestXml);
  });

  afterAll(async () => {
    if (outDir) {
      await fs.rm(outDir, { recursive: true, force: true });
    }
  });

  it("defines exactly one organization, one item, and one resource (2.2)", () => {
    expect(manifestDoc.querySelectorAll("organizations > organization")).toHaveLength(1);
    expect(manifestDoc.querySelectorAll("organization > item")).toHaveLength(1);
    expect(manifestDoc.querySelectorAll("resources > resource")).toHaveLength(1);
  });

  it("declares the resource as a SCO launched from index.html (2.3)", () => {
    const resource = manifestDoc.querySelector("resources > resource");
    expect(resource).not.toBeNull();
    expect(resource.getAttribute("adlcp:scormtype")).toBe("sco");
    expect(resource.getAttribute("href")).toBe("index.html");
  });

  it("lists index.html as a file dependency of the SCO resource (2.4)", () => {
    const resource = manifestDoc.querySelector("resources > resource");
    const fileHrefs = Array.from(resource.querySelectorAll("file")).map((f) =>
      f.getAttribute("href"),
    );
    expect(fileHrefs).toContain("index.html");
  });

  it("the single item references the single resource (2.2)", () => {
    const item = manifestDoc.querySelector("organization > item");
    const resource = manifestDoc.querySelector("resources > resource");
    expect(item.getAttribute("identifierref")).toBe(
      resource.getAttribute("identifier"),
    );
  });

  it("references the SCORM 1.2 schema versions matching the copied schema files (2.6)", async () => {
    // The manifest must declare ADL SCORM 1.2 ...
    const schema = manifestDoc.querySelector("metadata > schema");
    const schemaversion = manifestDoc.querySelector("metadata > schemaversion");
    expect(schema.textContent).toBe("ADL SCORM");
    expect(schemaversion.textContent).toBe("1.2");

    // ... and reference the schema files that are actually copied into the
    // package root. The SCORM 1.2 content-packaging and ADL CP schemas are the
    // versioned XSDs the schemaLocation points at.
    const manifestEl = manifestDoc.querySelector("manifest");
    const schemaLocation = manifestEl.getAttribute("xsi:schemaLocation");
    expect(schemaLocation).toContain("imscp_rootv1p1p2.xsd");
    expect(schemaLocation).toContain("adlcp_rootv1p2.xsd");

    // Every schema file named in the manifest's schemaLocation is present in
    // the copied package root, and conversely the versioned CP/ADL schemas are
    // declared — so the referenced versions match the copied files.
    for (const file of SCHEMA_FILES) {
      await expect(fs.access(path.join(outDir, file))).resolves.toBeUndefined();
    }
  });

  it("the built index.html presents a noscript fallback to en/ and fr/ (3.5)", async () => {
    const html = await fs.readFile(path.join(outDir, "index.html"), "utf8");
    const doc = new JSDOM(html).window.document;
    const noscript = doc.querySelector("noscript");
    expect(noscript).not.toBeNull();

    const inner = new JSDOM(
      `<!DOCTYPE html><body>${noscript.innerHTML}</body>`,
    ).window.document;
    const hrefs = Array.from(inner.querySelectorAll("a[href]")).map((a) =>
      a.getAttribute("href"),
    );
    expect(hrefs).toContain("en/index.html");
    expect(hrefs).toContain("fr/index.html");
  });
});

describe("renderManifest pure output (Req 2.3, 2.4)", () => {
  it("renders a single sco resource with index.html as href and dependency", () => {
    const xml = renderManifest({ files: ["en/index.html", "js/app.js"] });
    const doc = parseXml(xml);

    const resources = doc.querySelectorAll("resources > resource");
    expect(resources).toHaveLength(1);

    const resource = resources[0];
    expect(resource.getAttribute("adlcp:scormtype")).toBe("sco");
    expect(resource.getAttribute("href")).toBe("index.html");

    const fileHrefs = Array.from(resource.querySelectorAll("file")).map((f) =>
      f.getAttribute("href"),
    );
    expect(fileHrefs).toContain("index.html");
    expect(fileHrefs).toContain("en/index.html");
    expect(fileHrefs).toContain("js/app.js");
  });
});
