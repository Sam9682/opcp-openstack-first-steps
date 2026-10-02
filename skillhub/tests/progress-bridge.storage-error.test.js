/**
 * @vitest-environment jsdom
 *
 * Unit test for graceful storage-error handling in the Progress_Bridge.
 *
 * Requirement 7.2: IF localStorage access raises an error, THEN THE
 * Progress_Bridge SHALL complete its operation without raising an error.
 *
 * These tests install a localStorage stub whose every member throws, then
 * assert that `readCompletedIds`, `restoreToLocalStorage`, and
 * `deserializeProgress` each degrade gracefully — completing without
 * propagating the storage error and returning the documented safe defaults.
 *
 * Validates: Requirements 7.2
 */

import { afterEach, describe, expect, it } from "vitest";
import {
  readCompletedIds,
  restoreToLocalStorage,
  deserializeProgress,
  STORAGE_PREFIX,
} from "../js/scorm/progress-bridge.js";

const originalLocalStorage = Object.getOwnPropertyDescriptor(
  globalThis,
  "localStorage",
);

/**
 * Build a localStorage stub whose every access path throws, simulating an
 * environment where storage is disabled (e.g. privacy mode) or otherwise
 * raising on access.
 */
function throwingStorage() {
  const boom = () => {
    throw new Error("storage access denied");
  };
  return {
    get length() {
      throw new Error("storage access denied");
    },
    key: boom,
    getItem: boom,
    setItem: boom,
    removeItem: boom,
    clear: boom,
  };
}

function installStorage(stub) {
  Object.defineProperty(globalThis, "localStorage", {
    value: stub,
    configurable: true,
    writable: true,
  });
}

afterEach(() => {
  if (originalLocalStorage) {
    Object.defineProperty(globalThis, "localStorage", originalLocalStorage);
  } else {
    delete globalThis.localStorage;
  }
});

describe("Progress_Bridge graceful storage-error handling (Req 7.2)", () => {
  it("readCompletedIds returns [] without raising when localStorage throws", () => {
    installStorage(throwingStorage());

    let result;
    expect(() => {
      result = readCompletedIds();
    }).not.toThrow();
    expect(result).toEqual([]);
  });

  it("restoreToLocalStorage completes without raising when every setItem throws", () => {
    const stub = throwingStorage();
    installStorage(stub);

    expect(() => {
      restoreToLocalStorage(["core-concepts", "compute", "networking"]);
    }).not.toThrow();
  });

  it("restoreToLocalStorage tolerates a storage that throws only on some writes", () => {
    const calls = [];
    installStorage({
      length: 0,
      key: () => null,
      getItem: () => null,
      removeItem: () => {},
      clear: () => {},
      setItem: (key) => {
        calls.push(key);
        // Simulate a quota-exceeded error partway through the restore.
        if (calls.length === 2) {
          throw new Error("QuotaExceededError");
        }
      },
    });

    expect(() => {
      restoreToLocalStorage(["a", "b", "c"]);
    }).not.toThrow();
    // All ids were attempted even though the second write threw.
    expect(calls).toEqual([
      STORAGE_PREFIX + "a",
      STORAGE_PREFIX + "b",
      STORAGE_PREFIX + "c",
    ]);
  });

  it("deserializeProgress returns a safe default without raising when localStorage throws", () => {
    installStorage(throwingStorage());

    let result;
    expect(() => {
      result = deserializeProgress('{"v":1,"done":["core-concepts"],"guardrail":null}');
    }).not.toThrow();
    // deserializeProgress never touches storage, so it still decodes correctly.
    expect(result).toEqual({ ids: ["core-concepts"], guardrail: null });
  });

  it("deserializeProgress yields ids=[] for malformed input while storage throws", () => {
    installStorage(throwingStorage());

    let result;
    expect(() => {
      result = deserializeProgress("not valid json {");
    }).not.toThrow();
    expect(result).toEqual({ ids: [], guardrail: null });
  });
});
