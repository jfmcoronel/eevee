// Copyright 2017 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
/\w/iu.test('\u017F');
/\w/iu.test('\u212A');
/\W/iu.test('\u017F');
/\W/iu.test('\u212A');
/\W/iu.test('s');
/\W/iu.test('S');
/\W/iu.test('K');
/\W/iu.test('k');
/[\w]/iu.test('\u017F');
/[\w]/iu.test('\u212A');
/[\W]/iu.test('\u017F');
/[\W]/iu.test('\u212A');
/[\W]/iu.test('s');
/[\W]/iu.test('S');
/[\W]/iu.test('K');
/[\W]/iu.test('k');
/\b/iu.test('\u017F');
/\b/iu.test('\u212A');
/\b/iu.test('s');
/\b/iu.test('S');
/\B/iu.test('\u017F');
/\B/iu.test('\u212A');
/\B/iu.test('s');
/\B/iu.test('S');
/\B/iu.test('K');
/\B/iu.test('k');
["abcd", "d"];
/a.*?(.)\b/i.exec('abcd\u017F cd');
["abcd", "d"];
/a.*?(.)\b/i.exec('abcd\u212A cd');
["abcd\u017F", "\u017F"];
/a.*?(.)\b/iu.exec('abcd\u017F cd');
["abcd\u212A", "\u212A"];
/a.*?(.)\b/iu.exec('abcd\u212A cd');
["a\u017F ", " "];
/a.*?\B(.)/i.exec('a\u017F ');
["a\u212A ", " "];
/a.*?\B(.)/i.exec('a\u212A ');
["a\u017F", "\u017F"];
/a.*?\B(.)/iu.exec('a\u017F ');
["a\u212A", "\u212A"];
/a.*?\B(.)/iu.exec('a\u212A ');
