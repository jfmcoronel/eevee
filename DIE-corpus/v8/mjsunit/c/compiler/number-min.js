// Copyright 2018 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
// Flags: --allow-natives-syntax --opt
// Test that NumberMin properly passes the kIdentifyZeros truncation.
(function () {
  function foo(x) {
    if (Math.min(x * -2, -1) == -2) {
      return 0;
    }

    return 1;
  }

  0;
  foo(1);
  1;
  foo(2);
  0;
  foo(1);
  1;
  foo(2);
  foo();
  1;
  foo(0);
  foo();
})(); // Test that NumberMin properly handles 64-bit comparisons.


(function () {
  function foo(x) {
    x = x | 0;
    return Math.min(x - 1, x + 1);
  }

  -Math.pow(2, 31) - 1;
  foo(-Math.pow(2, 31));
  Math.pow(2, 31) - 2;
  foo(Math.pow(2, 31) - 1);
  -Math.pow(2, 31) - 1;
  foo(-Math.pow(2, 31));
  Math.pow(2, 31) - 2;
  foo(Math.pow(2, 31) - 1);
})();
