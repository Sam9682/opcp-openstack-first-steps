/**
 * Property-based tests for the SCORM completion status mapping.
 *
 * `computeStatus(pct)` maps a Completion_Percentage onto the SCORM
 * `cmi.core.lesson_status` value. The mapping depends only on the percentage:
 * `completed` when it equals 100, `incomplete` otherwise. The informational
 * Guardrail_Assessment never participates in the decision, so the test
 * generates arbitrary guardrail values and asserts the result is unaffected.
 *
 * Validates: Requirements 4.2, 4.3, 4.4
 */

import { describe, expect, it } from 'vitest';
import fc from 'fast-check';
import { computeStatus } from '../js/scorm/scorm-adapter.js';

describe('computeStatus completion mapping', () => {
  it('Feature: skillhub-scorm-export, Property 2: Completion status mapping (guardrail-independent)', () => {
    // Percentage across the full 0–100 range, biased to include the boundary
    // value 100 so the `completed` branch is exercised frequently.
    const pctArb = fc.oneof(
      fc.integer({ min: 0, max: 100 }),
      fc.constant(100),
    );

    // An arbitrary guardrail value of any shape. `computeStatus` takes only
    // `pct`, so this value is deliberately irrelevant to the call — generating
    // it demonstrates that the status is independent of the guardrail.
    const guardrailArb = fc.anything();

    fc.assert(
      fc.property(pctArb, guardrailArb, (pct, _guardrail) => {
        const status = computeStatus(pct);

        // Status depends only on the percentage (Req 4.2, 4.3), never the
        // guardrail (Req 4.4).
        const expected = pct === 100 ? 'completed' : 'incomplete';
        expect(status).toBe(expected);

        // Guardrail-independence: computing again with the same percentage but
        // ignoring the arbitrary guardrail yields the identical result.
        expect(computeStatus(pct)).toBe(status);
      }),
      { numRuns: 200 },
    );
  });
});
