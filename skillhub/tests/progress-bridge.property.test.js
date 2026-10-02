/**
 * @vitest-environment jsdom
 *
 * Property-based tests for the Progress_Bridge Suspend_Envelope round-trip.
 *
 * Feature: skillhub-scorm-export, Property 4: Suspend-data progress round-trip
 */

import { describe, it, expect, beforeEach } from "vitest";
import fc from "fast-check";
import {
  STORAGE_PREFIX,
  serializeProgress,
  deserializeProgress,
  restoreToLocalStorage,
} from "../js/scorm/progress-bridge.js";

/**
 * Generator for a valid lesson id: a non-empty string. We keep ids reasonably
 * constrained to the kind of slugs the course uses (letters, digits, dashes)
 * so the generated input space mirrors real lesson ids while still exercising
 * dedupe/sort behaviour across arbitrary orderings and repeats.
 */
const lessonId = fc
  .stringMatching(/^[a-zA-Z0-9-]+$/)
  .filter((s) => s.length > 0 && s.length <= 40);

/** A set of lesson ids: an array that may contain duplicates and arbitrary order. */
const lessonIds = fc.array(lessonId, { maxLength: 25 });

/**
 * An arbitrary guardrail value. The guardrail is informational and stored
 * verbatim inside the envelope, so it may be any JSON-serializable value.
 */
const guardrailValue = fc.jsonValue();

/** The expected canonical set (deduped) of ids given a raw input list. */
function expectedSet(ids) {
  return new Set(ids);
}

describe("Progress_Bridge Suspend_Envelope round-trip", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("Feature: skillhub-scorm-export, Property 4: Suspend-data progress round-trip", () => {
    // Validates: Requirements 4.5, 5.1, 5.2, 5.3
    fc.assert(
      fc.property(lessonIds, guardrailValue, (ids, guardrail) => {
        localStorage.clear();

        // Serialize then deserialize.
        const envelope = serializeProgress(ids, guardrail);
        const { ids: roundTripped, guardrail: carried } =
          deserializeProgress(envelope);

        // 5.3 — round-trip yields the same set of ids (serialize dedupes/sorts,
        // so compare as sets).
        expect(new Set(roundTripped)).toEqual(expectedSet(ids));

        // 4.5 — the guardrail value rides inside the envelope. serializeProgress
        // normalizes an absent/undefined guardrail to null; here the generator
        // produces concrete JSON values that must survive verbatim.
        expect(carried).toEqual(guardrail);

        // 5.1 — the envelope is of the documented shape {"v":1,"done":[...],...}.
        const parsed = JSON.parse(envelope);
        expect(parsed.v).toBe(1);
        expect(Array.isArray(parsed.done)).toBe(true);
        expect(new Set(parsed.done)).toEqual(expectedSet(ids));

        // 5.2 — restoring the deserialized ids reproduces exactly the
        // skillhub_lesson_complete_-prefixed localStorage keys for those ids.
        restoreToLocalStorage(roundTripped);

        const restoredKeys = new Set();
        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i);
          if (key && key.startsWith(STORAGE_PREFIX)) {
            restoredKeys.add(key);
          }
        }

        const expectedKeys = new Set(
          [...expectedSet(ids)].map((id) => STORAGE_PREFIX + id),
        );
        expect(restoredKeys).toEqual(expectedKeys);

        return true;
      }),
      { numRuns: 100 },
    );
  });
});
