/**
 * Property-based test for the SCORM adapter's score mapping.
 *
 * Feature: skillhub-scorm-export, Property 3: Score equals completion percentage
 * Validates: Requirements 4.1
 *
 * For any Completion_Percentage in the range 0–100, `ScormAdapter.sync()` sets
 * `cmi.core.score.raw` to exactly that integer percentage. The assertion is
 * made against a recording mock wrapper that captures ordered
 * `setValue(key, value)` calls.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import fc from "fast-check";
import { ScormAdapter } from "../js/scorm/scorm-adapter.js";

const NUM_RUNS = 200;

/**
 * A recording mock over the ScormApiWrapper surface used by the adapter. It
 * captures every `setValue(key, value)` call in order and stubs the remaining
 * methods the adapter touches with safe defaults.
 */
function makeRecordingWrapper() {
  const calls = [];
  return {
    calls,
    getValue: () => "",
    setValue: (key, value) => {
      calls.push({ key, value });
      return true;
    },
    commit: () => true,
    finish: () => true,
    /** Return the value of the most recent setValue for `key`, or undefined. */
    lastValue(key) {
      for (let i = calls.length - 1; i >= 0; i--) {
        if (calls[i].key === key) {
          return calls[i].value;
        }
      }
      return undefined;
    },
  };
}

describe("Feature: skillhub-scorm-export, Property 3: Score equals completion percentage", () => {
  beforeEach(() => {
    // sync() schedules a debounced commit via setTimeout; fake timers keep each
    // iteration isolated and prevent leaked timers from firing later.
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.clearAllTimers();
    vi.useRealTimers();
  });

  it("sets cmi.core.score.raw to exactly the integer completion percentage", () => {
    fc.assert(
      fc.property(fc.integer({ min: 0, max: 100 }), (pct) => {
        const wrapper = makeRecordingWrapper();
        const adapter = new ScormAdapter(wrapper, null, {
          getCompletionPercentage: () => pct,
          getCompletedLessons: () => [],
          evaluateGuardrailChecklist: () => null,
        });

        adapter.sync();

        expect(wrapper.lastValue("cmi.core.score.raw")).toBe(pct);
      }),
      { numRuns: NUM_RUNS }
    );
  });
});
