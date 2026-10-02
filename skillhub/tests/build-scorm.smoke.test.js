/**
 * Build smoke tests for the SkillHub SCORM 1.2 export.
 *
 * Runs the real `buildScormPackage` against a throwaway temp output directory
 * (node:os tmpdir) with the repo's `skillhub/` folder as the source, then
 * asserts the assembled package has the structure a SCORM 1.2 LMS expects:
 *
 *  - the required content trees are copied             (Req 1.3)
 *  - the js/scorm/* runtime modules are present        (Req 1.4)
 *  - imsmanifest.xml is written at the root            (Req 2.1)
 *  - the four SCORM 1.2 schema files sit at the root   (Req 2.5)
 *  - both en/ and fr/ locale trees are included        (Req 3.4)
 *  - a successful build resolves without throwing      (Req 1.6)
 *
 * It also guards the `cmi.suspend_data` 4096-character SCORM 1.2 ceiling: the
 * worst-case Suspend_Envelope (every lesson complete + a full five-layer
 * guardrail payload), serialized through the real progress bridge, must stay
 * within the limit so resume data never overflows (Req 5.1).
 *
 * Validates: Requirements 1.3, 1.4, 1.6, 2.1, 2.5, 3.4, 5.1
 */

import { mkdtemp, rm, stat, readdir } from "node:fs/promises";
import { tmpdir } from "node:os";
import { fileURLToPath } from "node:url";
import { dirname, resolve, join } from "node:path";

import { afterEach, beforeEach, describe, expect, it } from "vitest";

import { buildScormPackage } from "../../scripts/build-scorm.mjs";
import { serializeProgress } from "../js/scorm/progress-bridge.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

/** The repo's SkillHub course source tree (two levels up: skillhub/tests -> repo). */
const SRC_DIR = resolve(__dirname, "..");

/** SCORM 1.2 cmi.suspend_data ceiling in characters. */
const SUSPEND_DATA_LIMIT = 4096;

/** The four SCORM 1.2 schema files that must land at the package root (Req 2.5). */
const SCHEMA_FILES = [
  "adlcp_rootv1p2.xsd",
  "imscp_rootv1p1p2.xsd",
  "imsmd_rootv1p2p1.xsd",
  "ims_xml.xsd",
];

/** True when `path` exists and is a directory. */
async function isDir(path) {
  try {
    return (await stat(path)).isDirectory();
  } catch {
    return false;
  }
}

/** True when `path` exists and is a regular file. */
async function isFile(path) {
  try {
    return (await stat(path)).isFile();
  } catch {
    return false;
  }
}

describe("buildScormPackage smoke test (Req 1.3, 1.4, 1.6, 2.1, 2.5, 3.4)", () => {
  /** @type {string} */
  let outDir;
  /** @type {Awaited<ReturnType<typeof buildScormPackage>>} */
  let result;

  beforeEach(async () => {
    const tmpRoot = await mkdtemp(join(tmpdir(), "skillhub-scorm-smoke-"));
    outDir = join(tmpRoot, "skillhub_scorm");
    // Req 1.6: a successful build resolves without throwing.
    result = await buildScormPackage({ srcDir: SRC_DIR, outDir });
  });

  afterEach(async () => {
    // Clean up the throwaway temp tree (its parent, created by mkdtemp).
    if (outDir) {
      await rm(dirname(outDir), { recursive: true, force: true });
    }
    outDir = undefined;
    result = undefined;
  });

  it("resolves successfully and reports the output directory (Req 1.6)", async () => {
    expect(result).toBeTruthy();
    expect(result.outDir).toBe(outDir);
    expect(await isDir(outDir)).toBe(true);
  });

  it("copies the required course trees into the package (Req 1.3)", async () => {
    expect(await isFile(join(outDir, "index.html"))).toBe(true);
    expect(await isFile(join(outDir, "404.html"))).toBe(true);
    expect(await isDir(join(outDir, "en"))).toBe(true);
    expect(await isDir(join(outDir, "fr"))).toBe(true);
    expect(await isDir(join(outDir, "js"))).toBe(true);
    expect(await isDir(join(outDir, "assets"))).toBe(true);
  });

  it("includes the js/scorm/* runtime modules (Req 1.4)", async () => {
    const scormDir = join(outDir, "js", "scorm");
    expect(await isDir(scormDir)).toBe(true);

    const entries = await readdir(scormDir);
    const modules = entries.filter((name) => name.endsWith(".js"));
    expect(modules.length).toBeGreaterThan(0);

    // The runtime seams the package depends on at launch.
    for (const mod of [
      "api-discovery.js",
      "scorm-api.js",
      "progress-bridge.js",
      "scorm-adapter.js",
    ]) {
      expect(await isFile(join(scormDir, mod))).toBe(true);
    }
  });

  it("writes imsmanifest.xml at the package root (Req 2.1)", async () => {
    expect(await isFile(join(outDir, "imsmanifest.xml"))).toBe(true);
  });

  it("places the four SCORM 1.2 schema files at the root (Req 2.5)", async () => {
    for (const schema of SCHEMA_FILES) {
      expect(await isFile(join(outDir, schema))).toBe(true);
    }
  });

  it("includes both the en/ and fr/ locale trees (Req 3.4)", async () => {
    expect(await isFile(join(outDir, "en", "index.html"))).toBe(true);
    expect(await isFile(join(outDir, "fr", "index.html"))).toBe(true);
  });
});

describe("worst-case Suspend_Envelope size (Req 5.1)", () => {
  /**
   * Every lesson id the SkillHub course exposes as a completable page. These
   * mirror the `en/`/`fr/` lesson HTML filenames (minus the extension) and are
   * the ids the course's progress module records as
   * `skillhub_lesson_complete_<id>`. The worst case for suspend_data is "all of
   * them complete at once".
   */
  const ALL_LESSON_IDS = [
    "index",
    "prerequisites",
    "core-concepts",
    "authentication",
    "user-management",
    "networking",
    "lacp",
    "software-raid",
    "compute",
    "cleanup",
    "appendix",
    "appendix-trunk-setup",
    "cheat-sheet",
    "glossary",
    "summary",
  ];

  /**
   * A full, five-layer guardrail payload — the informational Guardrail_Assessment
   * folded into the envelope at its heaviest. Each layer carries a label and a
   * checked flag, mirroring the five guardrail layers the course evaluates, plus
   * a coverage count, so the serialized envelope reflects a realistic maximum.
   */
  const FULL_GUARDRAIL = {
    layers: [
      { id: "layer-1-input-validation", label: "Input validation", checked: true },
      { id: "layer-2-authn-authz", label: "Authentication & authorization", checked: true },
      { id: "layer-3-data-protection", label: "Data protection", checked: true },
      { id: "layer-4-monitoring-logging", label: "Monitoring & logging", checked: true },
      { id: "layer-5-incident-response", label: "Incident response", checked: true },
    ],
    covered: 5,
    total: 5,
  };

  it("the fully-populated envelope stays within the 4096-char suspend_data limit (Req 5.1)", () => {
    const envelope = serializeProgress(ALL_LESSON_IDS, FULL_GUARDRAIL);

    // Sanity: it really is the documented Suspend_Envelope shape and carries
    // every lesson id plus the guardrail payload (i.e. a genuine worst case).
    const parsed = JSON.parse(envelope);
    expect(parsed.v).toBe(1);
    expect(new Set(parsed.done)).toEqual(new Set(ALL_LESSON_IDS));
    expect(parsed.guardrail.layers).toHaveLength(5);

    expect(envelope.length).toBeLessThanOrEqual(SUSPEND_DATA_LIMIT);
  });
});
