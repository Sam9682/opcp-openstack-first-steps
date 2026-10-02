/**
 * @vitest-environment jsdom
 *
 * Integration test for the SCORM bootstrap wiring
 * (`skillhub/js/scorm/scorm-bootstrap.js`).
 *
 * Unlike the adapter lifecycle tests — which construct the adapter directly —
 * these tests drive the *whole* wiring through the exported `bootstrap()` using
 * a mock host window. The mock window carries:
 *
 *  - an `API` object (SCORM 1.2 LMS surface) so `discoverApi(win)` finds it by
 *    walking `win.parent` (the mock is its own parent, which stops the walk);
 *  - a seeded `cmi.suspend_data` envelope so `start()` can resume progress;
 *  - `addEventListener` / `removeEventListener` that capture the registered
 *    handlers so the test can assert the listeners are installed and then fire
 *    them to prove they drive `sync` and `end` respectively;
 *  - a `SkillHub` namespace exposing the injected course functions.
 *
 * Covered behaviours:
 *  - `bootstrap()` initializes the session and restores seeded `suspend_data`
 *    into localStorage before the course renders (Req 5.4).
 *  - `bootstrap()` installs both a `storage` and a `pagehide` listener
 *    (`installListeners`, Req 5.6 / 5.5).
 *  - Firing the captured `storage` handler drives `sync` — a debounced commit
 *    plus the score / status / suspend_data writes (Req 5.6).
 *  - Firing the captured `pagehide` handler drives `end` —
 *    `cmi.core.exit = suspend`, then `Commit`, then `Finish`, in order (Req 5.5).
 *  - `resolveCourseDeps` reads the course functions off `window.SkillHub`.
 *
 * Validates: Requirements 5.4, 5.5, 5.6
 */

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  bootstrap,
  installListeners,
  resolveCourseDeps,
} from "../js/scorm/scorm-bootstrap.js";
import { ScormAdapter, DEFAULT_COMMIT_DEBOUNCE_MS } from "../js/scorm/scorm-adapter.js";
import * as bridge from "../js/scorm/progress-bridge.js";

const { STORAGE_PREFIX } = bridge;

/**
 * Build a recording mock LMS `API` object. Every mutating call is appended to a
 * shared ordered `calls` log so the test can assert the exact SetValue /
 * Commit / Finish sequence. `LMSGetValue("cmi.suspend_data")` returns the
 * seeded envelope so `start()` can resume progress.
 *
 * @param {{ suspendData?: string }} [opts]
 */
function recordingApi({ suspendData = "" } = {}) {
  const calls = [];
  return {
    calls,
    LMSInitialize() {
      calls.push(["Initialize"]);
      return "true";
    },
    LMSGetValue(element) {
      calls.push(["GetValue", element]);
      if (element === "cmi.suspend_data") {
        return suspendData;
      }
      return "";
    },
    LMSSetValue(element, value) {
      calls.push(["SetValue", element, value]);
      return "true";
    },
    LMSCommit() {
      calls.push(["Commit"]);
      return "true";
    },
    LMSFinish() {
      calls.push(["Finish"]);
      return "true";
    },
    LMSGetLastError() {
      return "0";
    },
  };
}

/**
 * Build a mock host window with everything the bootstrap wiring touches:
 *
 *  - `API` directly on the window so `findApiInChain(win)` returns it on the
 *    first hop; `parent === self` stops the parent walk, `opener` is absent.
 *  - capturing `addEventListener` / `removeEventListener`, recording handlers
 *    into a `listeners` map keyed by event type.
 *  - a `SkillHub` namespace carrying the injected course functions, so
 *    `resolveCourseDeps(win)` resolves real functions (not no-ops).
 *
 * @param {{ api?: object, skillHub?: object }} [opts]
 */
function makeMockWindow({ api, skillHub } = {}) {
  /** @type {Record<string, Function[]>} */
  const listeners = {};
  const win = {
    API: api,
    opener: null,
    SkillHub: skillHub,
    listeners,
    addEventListener(type, handler) {
      (listeners[type] ??= []).push(handler);
    },
    removeEventListener(type, handler) {
      const arr = listeners[type];
      if (!arr) return;
      const i = arr.indexOf(handler);
      if (i >= 0) arr.splice(i, 1);
    },
  };
  // A window at the top of the chain is its own parent — this stops the
  // discovery walk after inspecting `win` itself.
  win.parent = win;
  return win;
}

/** Fire every captured handler registered for an event type. */
function fire(win, type) {
  for (const handler of win.listeners[type] ?? []) {
    handler({ type });
  }
}

beforeEach(() => {
  localStorage.clear();
});

afterEach(() => {
  vi.useRealTimers();
  localStorage.clear();
});

describe("scorm-bootstrap integration wiring", () => {
  it("resolveCourseDeps reads course functions off window.SkillHub", () => {
    const getCompletionPercentage = () => 42;
    const win = makeMockWindow({
      skillHub: { getCompletionPercentage },
    });

    const deps = resolveCourseDeps(win);

    expect(typeof deps.getCompletionPercentage).toBe("function");
    expect(deps.getCompletionPercentage()).toBe(42);
    // Absent course functions fall back to safe no-ops (do not throw).
    expect(typeof deps.getCompletedLessons).toBe("function");
    expect(() => deps.getCompletedLessons()).not.toThrow();
  });

  it("installListeners registers both a storage and a pagehide listener and the disposer removes them", () => {
    const win = makeMockWindow();
    const synced = [];
    const ended = [];
    const adapter = { sync: () => synced.push(1), end: () => ended.push(1) };

    const dispose = installListeners(adapter, win);

    expect(win.listeners.storage).toHaveLength(1);
    expect(win.listeners.pagehide).toHaveLength(1);

    // The handlers drive the adapter's sync / end.
    fire(win, "storage");
    fire(win, "pagehide");
    expect(synced).toHaveLength(1);
    expect(ended).toHaveLength(1);

    // The disposer tears both listeners down.
    dispose();
    expect(win.listeners.storage).toHaveLength(0);
    expect(win.listeners.pagehide).toHaveLength(0);
  });

  it("bootstrap() initializes, restores seeded suspend_data into localStorage, and installs both listeners (Req 5.4)", () => {
    vi.useFakeTimers();
    const envelope = bridge.serializeProgress(["core-concepts", "compute"], null);
    const api = recordingApi({ suspendData: envelope });
    const win = makeMockWindow({
      api,
      skillHub: {
        getCompletionPercentage: () => 50,
        getCompletedLessons: () => ["core-concepts", "compute"],
      },
    });

    const { wrapper, adapter, dispose } = bootstrap(win);

    // The session was initialized through the discovered API.
    expect(wrapper.available).toBe(true);
    expect(api.calls.some((c) => c[0] === "Initialize")).toBe(true);

    // start() restored the seeded completed ids into localStorage before any
    // course render — the course would read these keys on first paint.
    expect(localStorage.getItem(STORAGE_PREFIX + "core-concepts")).toBe("true");
    expect(localStorage.getItem(STORAGE_PREFIX + "compute")).toBe("true");

    // Both lifecycle listeners are installed on the host window.
    expect(win.listeners.storage).toHaveLength(1);
    expect(win.listeners.pagehide).toHaveLength(1);

    // The wiring is a real adapter driven through the real wrapper.
    expect(adapter).toBeInstanceOf(ScormAdapter);

    dispose();
  });

  it("firing the storage listener drives sync — score/status/suspend_data writes and a debounced commit (Req 5.6)", () => {
    vi.useFakeTimers();
    const api = recordingApi();
    let pct = 50;
    const win = makeMockWindow({
      api,
      skillHub: {
        getCompletionPercentage: () => pct,
        getCompletedLessons: () => ["core-concepts"],
        evaluateGuardrailChecklist: () => ({ layers: ["a"], covered: 1 }),
      },
    });

    const { dispose } = bootstrap(win);

    // Flush the commit scheduled by the initial start()->sync() so we observe
    // the storage-driven sync in isolation.
    vi.advanceTimersByTime(DEFAULT_COMMIT_DEBOUNCE_MS);
    const commitsAfterStart = api.calls.filter((c) => c[0] === "Commit").length;

    // Progress advances, then a storage event fires (as a cross-tab/localStorage
    // write would). This must drive a fresh sync.
    pct = 100;
    api.calls.length = 0; // isolate the writes produced by this sync
    fire(win, "storage");

    const scoreWrite = api.calls.find(
      (c) => c[0] === "SetValue" && c[1] === "cmi.core.score.raw",
    );
    const statusWrite = api.calls.find(
      (c) => c[0] === "SetValue" && c[1] === "cmi.core.lesson_status",
    );
    const suspendWrite = api.calls.find(
      (c) => c[0] === "SetValue" && c[1] === "cmi.suspend_data",
    );

    expect(scoreWrite[2]).toBe("100");
    expect(statusWrite[2]).toBe("completed");
    expect(suspendWrite).toBeTruthy();
    const decoded = bridge.deserializeProgress(suspendWrite[2]);
    expect(decoded.ids).toEqual(["core-concepts"]);
    expect(decoded.guardrail).toEqual({ layers: ["a"], covered: 1 });

    // The commit is debounced: none immediately after the storage event.
    expect(api.calls.filter((c) => c[0] === "Commit")).toHaveLength(0);
    vi.advanceTimersByTime(DEFAULT_COMMIT_DEBOUNCE_MS);
    expect(api.calls.filter((c) => c[0] === "Commit")).toHaveLength(1);

    expect(commitsAfterStart).toBeGreaterThanOrEqual(1);
    dispose();
  });

  it("a burst of storage events collapses into a single debounced commit (Req 5.6)", () => {
    vi.useFakeTimers();
    const api = recordingApi();
    const win = makeMockWindow({
      api,
      skillHub: {
        getCompletionPercentage: () => 30,
        getCompletedLessons: () => [],
      },
    });

    const { dispose } = bootstrap(win);
    vi.advanceTimersByTime(DEFAULT_COMMIT_DEBOUNCE_MS); // flush start's commit
    api.calls.length = 0;

    // Three storage events inside one debounce window.
    fire(win, "storage");
    fire(win, "storage");
    fire(win, "storage");

    expect(api.calls.filter((c) => c[0] === "Commit")).toHaveLength(0);
    vi.advanceTimersByTime(DEFAULT_COMMIT_DEBOUNCE_MS);
    expect(api.calls.filter((c) => c[0] === "Commit")).toHaveLength(1);

    dispose();
  });

  it("firing the pagehide listener drives end — exit=suspend, then Commit, then Finish in order (Req 5.5)", () => {
    vi.useFakeTimers();
    const api = recordingApi();
    const win = makeMockWindow({
      api,
      skillHub: {
        getCompletionPercentage: () => 100,
        getCompletedLessons: () => [],
      },
    });

    const { dispose } = bootstrap(win);
    vi.advanceTimersByTime(DEFAULT_COMMIT_DEBOUNCE_MS); // flush start's commit
    api.calls.length = 0;

    fire(win, "pagehide");

    const exitIdx = api.calls.findIndex(
      (c) =>
        c[0] === "SetValue" &&
        c[1] === "cmi.core.exit" &&
        c[2] === "suspend",
    );
    const commitIdx = api.calls.findIndex((c) => c[0] === "Commit");
    const finishIdx = api.calls.findIndex((c) => c[0] === "Finish");

    expect(exitIdx).toBeGreaterThanOrEqual(0);
    expect(commitIdx).toBeGreaterThan(exitIdx);
    expect(finishIdx).toBeGreaterThan(commitIdx);

    // Finish is the final interaction of the session.
    expect(api.calls.at(-1)[0]).toBe("Finish");

    dispose();
  });
});
