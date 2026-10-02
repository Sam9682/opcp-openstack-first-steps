/**
 * Property-based tests for the defensive SCORM API wrapper.
 *
 * Feature: skillhub-scorm-export, Property 6: LMS error tolerance
 * Validates: Requirements 7.1, 7.3
 */

import { describe, it, expect } from "vitest";
import fc from "fast-check";
import { ScormApiWrapper } from "../js/scorm/scorm-api.js";

const NUM_RUNS = 200;

/**
 * Each wrapper method, paired with the raw LMS method it delegates to and the
 * safe default it must return when the condition (no API / a throwing call) is
 * contained.
 *
 * - initialize/commit/finish/setValue return `false` on failure.
 * - getValue/getLastError return `""`.
 */
const METHODS = [
  { name: "initialize", raw: "LMSInitialize", invoke: (w) => w.initialize(), safe: false },
  { name: "getValue", raw: "LMSGetValue", invoke: (w) => w.getValue("cmi.suspend_data"), safe: "" },
  { name: "setValue", raw: "LMSSetValue", invoke: (w) => w.setValue("cmi.core.lesson_status", "completed"), safe: false },
  { name: "commit", raw: "LMSCommit", invoke: (w) => w.commit(), safe: false },
  { name: "finish", raw: "LMSFinish", invoke: (w) => w.finish(), safe: false },
  { name: "getLastError", raw: "LMSGetLastError", invoke: (w) => w.getLastError(), safe: "" },
];

const methodArb = fc.constantFrom(...METHODS);

/** The full set of raw LMS method names, used to build throwing mock APIs. */
const RAW_NAMES = ["LMSInitialize", "LMSGetValue", "LMSSetValue", "LMSCommit", "LMSFinish", "LMSGetLastError"];

/**
 * Build a mock LMS API where exactly one named raw method throws and every
 * other raw method succeeds with a benign SCORM-shaped return value.
 */
function makeApiWithThrowingMethod(throwingRaw) {
  const api = {};
  for (const raw of RAW_NAMES) {
    if (raw === throwingRaw) {
      api[raw] = () => {
        throw new Error(`${raw} failed`);
      };
    } else if (raw === "LMSGetValue" || raw === "LMSGetLastError") {
      api[raw] = () => "0";
    } else {
      api[raw] = () => "true";
    }
  }
  return api;
}

describe("Feature: skillhub-scorm-export, Property 6: LMS error tolerance", () => {
  it("returns a safe default without raising when api is null (standalone no-op)", () => {
    fc.assert(
      fc.property(methodArb, (method) => {
        const wrapper = new ScormApiWrapper(null);
        expect(wrapper.available).toBe(false);

        let result;
        expect(() => {
          result = method.invoke(wrapper);
        }).not.toThrow();

        expect(result).toBe(method.safe);
      }),
      { numRuns: NUM_RUNS }
    );
  });

  it("contains a throwing raw LMS method and returns a safe default", () => {
    fc.assert(
      fc.property(methodArb, (method) => {
        // A live API in which only the raw method this wrapper call delegates
        // to throws; the wrapper must contain it and return the safe default.
        const api = makeApiWithThrowingMethod(method.raw);
        const wrapper = new ScormApiWrapper(api);
        expect(wrapper.available).toBe(true);

        let result;
        expect(() => {
          result = method.invoke(wrapper);
        }).not.toThrow();

        expect(result).toBe(method.safe);
      }),
      { numRuns: NUM_RUNS }
    );
  });
});
