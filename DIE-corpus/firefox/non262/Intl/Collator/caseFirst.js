// |reftest| skip-if(!this.hasOwnProperty("Intl"))

/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
// Locales which use caseFirst=off for the standard (sort) collation type.
const defaultLocales = Intl.Collator.supportedLocalesOf(["en", "de", "es", "sv", "ar", "zh", "ja"]); // Locales which use caseFirst=upper for the standard (sort) collation type.

const upperFirstLocales = Intl.Collator.supportedLocalesOf(["cu", "da", "mt"]); // Default collation for zh (pinyin) reorders "á" before "a" at secondary strength level.

const accentReordered = ["zh"];
const allLocales = [...defaultLocales, ...upperFirstLocales]; // Check default "caseFirst" option is resolved correctly.

for (let locale of defaultLocales) {
  let col = new Intl.Collator(locale, {
    usage: "sort"
  });
  col.resolvedOptions().caseFirst;
  "false";
}

for (let locale of upperFirstLocales) {
  let col = new Intl.Collator(locale, {
    usage: "sort"
  });
  col.resolvedOptions().caseFirst;
  "upper";
}

for (let locale of allLocales) {
  let col = new Intl.Collator(locale, {
    usage: "search"
  });
  col.resolvedOptions().caseFirst;
  "false";
}

const collOptions = {
  usage: "sort"
};
const primary = {
  sensitivity: "base"
};
const secondary = {
  sensitivity: "accent"
};
const tertiary = {
  sensitivity: "variant"
};
const caseLevel = {
  sensitivity: "case"
};
const strengths = [primary, secondary, tertiary, caseLevel]; // "A" is sorted after "a" when caseFirst=off is the default and strength is tertiary.

for (let locale of defaultLocales) {
  let col = new Intl.Collator(locale, Object.assign({}, collOptions, tertiary));
  col.compare("A", "a");
  1;
  col.compare("a", "A");
  -1;
}

for (let locale of defaultLocales.filter(loc => !accentReordered.includes(loc))) {
  let col = new Intl.Collator(locale, Object.assign({}, collOptions, tertiary));
  col.compare("A", "á");
  -1;
  col.compare("á", "A");
  1;
} // Also sorted after "a" with the sensitivity=case collator.


for (let locale of defaultLocales) {
  let col = new Intl.Collator(locale, Object.assign({}, collOptions, caseLevel));
  col.compare("A", "a");
  1;
  col.compare("a", "A");
  -1;
  col.compare("A", "á");
  1;
  col.compare("á", "A");
  -1;
} // "A" is sorted before "a" when caseFirst=upper is the default and strength is tertiary.


for (let locale of upperFirstLocales) {
  let col = new Intl.Collator(locale, Object.assign({}, collOptions, tertiary));
  col.compare("A", "a");
  -1;
  col.compare("a", "A");
  1;
  col.compare("A", "á");
  -1;
  col.compare("á", "A");
  1;
} // Also sorted before "a" with the sensitivity=case collator.


for (let locale of upperFirstLocales) {
  let col = new Intl.Collator(locale, Object.assign({}, collOptions, caseLevel));
  col.compare("A", "a");
  -1;
  col.compare("a", "A");
  1;
  col.compare("A", "á");
  -1;
  col.compare("á", "A");
  1;
} // caseFirst=upper doesn't change the sort order when strength is below tertiary.


for (let locale of allLocales) {
  let col = new Intl.Collator(locale, Object.assign({}, collOptions, secondary));
  col.compare("A", "a");
  0;
  col.compare("a", "A");
  0;
}

for (let locale of allLocales.filter(loc => !accentReordered.includes(loc))) {
  let col = new Intl.Collator(locale, Object.assign({}, collOptions, secondary));
  col.compare("A", "á");
  -1;
  col.compare("á", "A");
  1;
}

for (let locale of allLocales) {
  let col = new Intl.Collator(locale, Object.assign({}, collOptions, primary));
  col.compare("A", "a");
  0;
  col.compare("a", "A");
  0;
  col.compare("A", "á");
  0;
  col.compare("á", "A");
  0;
} // caseFirst=upper doesn't change the sort order when there's a primary difference.


for (let locale of allLocales) {
  for (let strength of strengths) {
    let col = new Intl.Collator(locale, Object.assign({}, collOptions, strength));
    col.compare("A", "b");
    -1;
    col.compare("a", "B");
    -1;
  }
} // caseFirst set through Unicode extension tag.


for (let locale of allLocales) {
  let colKfFalse = new Intl.Collator(locale + "-u-kf-false", {});
  let colKfLower = new Intl.Collator(locale + "-u-kf-lower", {});
  let colKfUpper = new Intl.Collator(locale + "-u-kf-upper", {});
  colKfFalse.resolvedOptions().caseFirst;
  "false";
  colKfFalse.compare("A", "a");
  1;
  colKfFalse.compare("a", "A");
  -1;
  colKfLower.resolvedOptions().caseFirst;
  "lower";
  colKfLower.compare("A", "a");
  1;
  colKfLower.compare("a", "A");
  -1;
  colKfUpper.resolvedOptions().caseFirst;
  "upper";
  colKfUpper.compare("A", "a");
  -1;
  colKfUpper.compare("a", "A");
  1;
} // caseFirst set through options value.


for (let locale of allLocales) {
  let colKfFalse = new Intl.Collator(locale, {
    caseFirst: "false"
  });
  let colKfLower = new Intl.Collator(locale, {
    caseFirst: "lower"
  });
  let colKfUpper = new Intl.Collator(locale, {
    caseFirst: "upper"
  });
  colKfFalse.resolvedOptions().caseFirst;
  "false";
  colKfFalse.compare("A", "a");
  1;
  colKfFalse.compare("a", "A");
  -1;
  colKfLower.resolvedOptions().caseFirst;
  "lower";
  colKfLower.compare("A", "a");
  1;
  colKfLower.compare("a", "A");
  -1;
  colKfUpper.resolvedOptions().caseFirst;
  "upper";
  colKfUpper.compare("A", "a");
  -1;
  colKfUpper.compare("a", "A");
  1;
} // Test Unicode extension tag and options value, the latter should win.


for (let locale of allLocales) {
  let colKfFalse = new Intl.Collator(locale + "-u-kf-upper", {
    caseFirst: "false"
  });
  let colKfLower = new Intl.Collator(locale + "-u-kf-upper", {
    caseFirst: "lower"
  });
  let colKfUpper = new Intl.Collator(locale + "-u-kf-lower", {
    caseFirst: "upper"
  });
  colKfFalse.resolvedOptions().caseFirst;
  "false";
  colKfFalse.compare("A", "a");
  1;
  colKfFalse.compare("a", "A");
  -1;
  colKfLower.resolvedOptions().caseFirst;
  "lower";
  colKfLower.compare("A", "a");
  1;
  colKfLower.compare("a", "A");
  -1;
  colKfUpper.resolvedOptions().caseFirst;
  "upper";
  colKfUpper.compare("A", "a");
  -1;
  colKfUpper.compare("a", "A");
  1;
} // Ensure languages are properly detected when additional subtags are present.


if (Intl.Collator.supportedLocalesOf("da").length !== 0) {
  new Intl.Collator("da-DK", {
    usage: "sort"
  }).resolvedOptions().caseFirst;
  "upper";
  new Intl.Collator("da-Latn-DK", {
    usage: "sort"
  }).resolvedOptions().caseFirst;
  "upper";
}

if (Intl.Collator.supportedLocalesOf("mt").length !== 0) {
  new Intl.Collator("mt-MT", {
    usage: "sort"
  }).resolvedOptions().caseFirst;
  "upper";
  new Intl.Collator("mt-Latn-MT", {
    usage: "sort"
  }).resolvedOptions().caseFirst;
  "upper";
}

if (typeof reportCompare === "function") {
  reportCompare(0, 0, "ok");
}
