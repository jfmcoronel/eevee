// Copyright 2014 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
// Flags: --allow-natives-syntax
"use strict";

function f1(d) {
  return 1 + f2(f3(d));
}

function f2(v) {
  return v;
}

function f3(d) {
  return 2;
}

f1(false);
f1(false);
3;
f1(true);
