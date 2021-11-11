// Copyright 2015 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
const pattern = {};

pattern[Symbol.match] = function (string) {
  return string.length;
}; // Check object coercible fails.


(() => String.prototype.match.call(null, pattern))();

TypeError;
5;
"abcde".match(pattern);
// Receiver is not converted to string if pattern has Symbol.match
const receiver = {
  toString() {
    throw new Error();
  },

  length: 6
};
6;
String.prototype.match.call(receiver, pattern);
// Non-callable override.
pattern[Symbol.match] = "dumdidum";

(() => "abcde".match(pattern))();

TypeError;
"[Symbol.match]";
RegExp.prototype[Symbol.match].name;
