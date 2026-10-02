/**
 * Property-based tests for Api_Discovery (`skillhub/js/scorm/api-discovery.js`).
 *
 * Feature: skillhub-scorm-export, Property 5: LMS API discovery across parent
 * and opener chains.
 *
 * Validates: Requirements 6.1, 6.2, 6.3, 6.4
 */

import { describe, it, expect } from "vitest";
import fc from "fast-check";
import { MAX_DEPTH, discoverApi } from "../js/scorm/api-discovery.js";

/** A sentinel LMS API object: anything exposing an LMSInitialize function. */
function makeApi() {
  return { LMSInitialize: () => "true", __marker: "lms-api" };
}

/**
 * A mock window node. A "cross-origin" node throws when its `API` property is
 * read, mirroring a real SecurityError. The discovery code reads `win.API`
 * inside a try/catch, so such a node must be skipped without terminating the
 * walk — the chain link (`.parent` / `.opener`) itself stays traversable.
 */
function makeWindow({ api = null, crossOrigin = false } = {}) {
  const node = {};
  if (crossOrigin) {
    Object.defineProperty(node, "API", {
      configurable: true,
      get() {
        throw new Error("SecurityError: cross-origin API access");
      },
    });
  } else {
    node.API = api;
  }
  return node;
}

/**
 * Build a chain of `length` windows linked via `linkKey` (`parent` or
 * `opener`). The API, if provided, is placed on the node at `apiDepth`
 * (0 = the start window). Interior nodes at the given `throwingDepths` are
 * marked cross-origin: reading their `API` throws, but the chain link stays
 * traversable so the API beyond them is still discoverable. The node that
 * hosts the API is never made cross-origin (its API must be readable).
 *
 * Returns the head window of the chain.
 */
function buildChain({ length, linkKey, apiDepth, throwingDepths }) {
  const nodes = [];
  for (let i = 0; i < length; i += 1) {
    const isApiNode = apiDepth !== null && i === apiDepth;
    const crossOrigin = !isApiNode && throwingDepths.has(i);
    nodes.push(
      makeWindow({ api: isApiNode ? makeApi() : null, crossOrigin })
    );
  }

  // The top of a chain is its own link target (self-referential), which the
  // discovery code uses as the stop condition.
  for (let i = 0; i < length; i += 1) {
    const node = nodes[i];
    const next = i + 1 < length ? nodes[i + 1] : node; // top links to itself
    Object.defineProperty(node, linkKey, {
      configurable: true,
      get() {
        return next;
      },
    });
  }

  return nodes[0];
}

/** Attach `openerHead` to `parentHead` via a guarded `opener` getter. */
function attachOpener(parentHead, openerHead) {
  Object.defineProperty(parentHead, "opener", {
    configurable: true,
    get() {
      return openerHead;
    },
  });
  return parentHead;
}

describe("Feature: skillhub-scorm-export, Property 5: LMS API discovery across parent and opener chains", () => {
  it("locates the API when it lives at a bounded depth in the parent chain, tolerating cross-origin nodes", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: MAX_DEPTH }), // chain length
        fc.integer({ min: 0, max: MAX_DEPTH - 1 }), // candidate api depth
        fc.array(fc.integer({ min: 0, max: MAX_DEPTH }), { maxLength: 6 }),
        (length, apiDepthRaw, throwingArr) => {
          const apiDepth = apiDepthRaw % length;
          const throwingDepths = new Set(throwingArr);
          const head = buildChain({
            length,
            linkKey: "parent",
            apiDepth,
            throwingDepths,
          });
          // No opener chain here.
          attachOpener(head, null);

          const found = discoverApi(head);
          expect(found).not.toBeNull();
          expect(found.__marker).toBe("lms-api");
        }
      ),
      { numRuns: 150 }
    );
  });

  it("locates the API via the opener chain when the parent chain has none", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: MAX_DEPTH }), // parent chain length (no api)
        fc.integer({ min: 1, max: MAX_DEPTH }), // opener chain length
        fc.integer({ min: 0, max: MAX_DEPTH - 1 }), // opener api depth
        fc.array(fc.integer({ min: 0, max: MAX_DEPTH }), { maxLength: 6 }),
        (parentLen, openerLen, openerApiRaw, throwingArr) => {
          const openerApiDepth = openerApiRaw % openerLen;
          const throwingDepths = new Set(throwingArr);

          const parentHead = buildChain({
            length: parentLen,
            linkKey: "parent",
            apiDepth: null, // no API anywhere in the parent chain
            throwingDepths,
          });
          const openerHead = buildChain({
            length: openerLen,
            linkKey: "parent",
            apiDepth: openerApiDepth,
            throwingDepths,
          });
          attachOpener(parentHead, openerHead);

          const found = discoverApi(parentHead);
          expect(found).not.toBeNull();
          expect(found.__marker).toBe("lms-api");
        }
      ),
      { numRuns: 150 }
    );
  });

  it("returns null when no API exists in either the parent or opener chain", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: MAX_DEPTH }), // parent chain length
        fc.integer({ min: 0, max: MAX_DEPTH }), // opener chain length (0 => none)
        fc.array(fc.integer({ min: 0, max: MAX_DEPTH }), { maxLength: 6 }),
        (parentLen, openerLen, throwingArr) => {
          const throwingDepths = new Set(throwingArr);
          const parentHead = buildChain({
            length: parentLen,
            linkKey: "parent",
            apiDepth: null,
            throwingDepths,
          });

          if (openerLen === 0) {
            attachOpener(parentHead, null);
          } else {
            const openerHead = buildChain({
              length: openerLen,
              linkKey: "parent",
              apiDepth: null,
              throwingDepths,
            });
            attachOpener(parentHead, openerHead);
          }

          expect(discoverApi(parentHead)).toBeNull();
        }
      ),
      { numRuns: 150 }
    );
  });

  it("returns null when reading the opener itself throws cross-origin and the parent chain has no API", () => {
    fc.assert(
      fc.property(fc.integer({ min: 1, max: MAX_DEPTH }), (parentLen) => {
        const parentHead = buildChain({
          length: parentLen,
          linkKey: "parent",
          apiDepth: null,
          throwingDepths: new Set(),
        });
        Object.defineProperty(parentHead, "opener", {
          configurable: true,
          get() {
            throw new Error("SecurityError: cross-origin opener");
          },
        });

        expect(discoverApi(parentHead)).toBeNull();
      }),
      { numRuns: 100 }
    );
  });
});
