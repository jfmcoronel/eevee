// Copyright 2017 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file
// Flags: --allow-natives-syntax
function f() {
  ;
}

function g(o) {
  f();
  return h(o);
}

function h(o) {
  return o.x;
}

g({
  x: 1
});
g({
  x: 2
});
g({
  x: 3
});
g({
  y: 1,
  x: 3
});
