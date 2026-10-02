// @vitest-environment jsdom
/**
 * Property-based tests for locale resolution precedence.
 *
 * Validates: Requirements 3.1, 3.2, 3.3
 */

import { afterEach, describe, expect, it, vi } from 'vitest';
import fc from 'fast-check';
import {
  resolveLocale,
  SUPPORTED_LOCALES,
  DEFAULT_LOCALE,
  STORAGE_KEY,
} from '../js/scorm/locale.js';

/**
 * Install a localStorage stub whose `getItem(STORAGE_KEY)` returns `stored`.
 * A `null` value models an absent stored locale.
 *
 * @param {string|null} stored - The value the stub returns for STORAGE_KEY.
 */
function stubStoredLocale(stored) {
  vi.spyOn(window.localStorage.__proto__, 'getItem').mockImplementation((key) =>
    key === STORAGE_KEY ? stored : null,
  );
}

/**
 * Stub `navigator.language` to the given browser language string.
 *
 * @param {string} lang - The browser language string to expose.
 */
function stubBrowserLanguage(lang) {
  vi.spyOn(window.navigator, 'language', 'get').mockReturnValue(lang);
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe('resolveLocale precedence', () => {
  it('Feature: skillhub-scorm-export, Property 1: Locale resolution precedence', () => {
    // Arbitrary stored value: either absent (null) or an arbitrary string,
    // biased to also cover the supported locales so the "valid stored wins"
    // branch is exercised frequently.
    const storedArb = fc.oneof(
      fc.constant(null),
      fc.constantFrom(...SUPPORTED_LOCALES),
      fc.string(),
    );

    // Arbitrary browser language, biased to include `fr`-prefixed strings in
    // varied casing so the fr branch is exercised, plus arbitrary strings.
    const browserArb = fc.oneof(
      fc.string(),
      fc.constantFrom('fr', 'fr-FR', 'FR', 'fr-CA', 'frisian', 'en', 'en-US', 'de'),
      fc
        .tuple(fc.constantFrom('fr', 'FR', 'Fr', 'fR'), fc.string())
        .map(([p, s]) => p + s),
    );

    fc.assert(
      fc.property(storedArb, browserArb, (stored, browserLang) => {
        stubStoredLocale(stored);
        stubBrowserLanguage(browserLang);

        const result = resolveLocale();

        const storedIsValid =
          stored != null && SUPPORTED_LOCALES.indexOf(stored) !== -1;
        const browserIsFr = browserLang.toLowerCase().indexOf('fr') === 0;

        let expected;
        if (storedIsValid) {
          // 1. A valid stored value wins (Req 3.2).
          expected = stored;
        } else if (browserIsFr) {
          // 2. Browser language beginning with `fr` resolves to `fr` (Req 3.1).
          expected = 'fr';
        } else {
          // 3. Otherwise the resolved locale is `en` (Req 3.3).
          expected = DEFAULT_LOCALE;
        }

        expect(result).toBe(expected);

        vi.restoreAllMocks();
      }),
      { numRuns: 200 },
    );
  });
});
