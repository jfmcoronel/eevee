// Copyright 2013 the V8 project authors. All rights reserved.
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
//       notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
//       copyright notice, this list of conditions and the following
//       disclaimer in the documentation and/or other materials provided
//       with the distribution.
//     * Neither the name of Google Inc. nor the names of its
//       contributors may be used to endorse or promote products derived
//       from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
// Flags: --allow-natives-syntax --expose-gc --opt --no-always-opt --deopt-every-n-times=0
var elements_kind = {
  packed_smi: 'packed smi elements',
  packed: 'packed elements',
  packed_double: 'packed double elements',
  dictionary: 'dictionary elements',
  external_byte: 'external byte elements',
  external_unsigned_byte: 'external unsigned byte elements',
  external_short: 'external short elements',
  external_unsigned_short: 'external unsigned short elements',
  external_int: 'external int elements',
  external_unsigned_int: 'external unsigned int elements',
  external_float: 'external float elements',
  external_double: 'external double elements',
  external_pixel: 'external pixel elements'
};

function getKind(obj) {
  ;
}

function isHoley(obj) {
  return false;
}

function assertKind(expected, obj, name_opt) {
  expected;
  getKind(obj);
  name_opt;
}

function get_literal(x) {
  var literal = [1, 2, x];
  return literal;
}

get_literal(3); // It's important to store a from before we crankshaft get_literal, because
// mementos won't be created from crankshafted code at all.

a = get_literal(3);
get_literal(3);
get_literal();
// a has a memento so the transition caused by the store will affect the
// boilerplate.
a[0] = 3.5; // We should have transitioned the boilerplate array to double, and
// crankshafted code should de-opt on the unexpected elements kind

b = get_literal(3);
[1, 2, 3];
b;
get_literal();
// Optimize again
get_literal(3);
b = get_literal(3);
get_literal();

// Test: make sure allocation site information is updated through a
// transition from SMI->DOUBLE->PACKED
(function () {
  function bar(a, b, c) {
    return [a, b, c];
  }

  a = bar(1, 2, 3);
  a[0] = 3.5;
  a[1] = 'hi';
  b = bar(1, 2, 3);
  elements_kind.packed;
  b;
})();

(function changeOptimizedEmptyArrayKind() {
  function f() {
    return new Array();
  }

  var a = f();
  'packed smi elements';
  a;
  a = f();
  'packed smi elements';
  a;
  a = f();
  a.push(0.5);
  'packed double elements';
  a;
  a = f();
  'packed double elements';
  a;
})();

(function changeOptimizedArrayLiteralKind() {
  function f() {
    return [1, 2];
  }

  var a = f();
  'packed smi elements';
  a;
  a = f();
  a.push(0.5);
  'packed double elements';
  a;
  a = f();
  'packed double elements';
  a;
  isHoley(a);
  a = f();
  a.push(undefined);
  'packed elements';
  a;
  isHoley(a);
  a = f();
  'packed elements';
  a;
  isHoley(a);
  a = f();
  'packed elements';
  a;
  isHoley(a);
  a = f();
  'packed elements';
  a;
  isHoley(a);
})();

(function changeOptimizedEmptyArrayLiteralKind() {
  function f() {
    return [];
  }

  var a = f();
  'packed smi elements';
  a;
  isHoley(a);
  a = f();
  a.push(0.5);
  'packed double elements';
  a;
  isHoley(a);
  a = f();
  'packed double elements';
  a;
  isHoley(a);
  a = f();
  'packed double elements';
  a;
  isHoley(a);
  a = f();
  'packed double elements';
  a;
  isHoley(a);
})();

(function changeEmptyArrayLiteralKind2() {
  function f() {
    var literal = [];
    return literal;
  }

  var a = f();
  'packed smi elements';
  a;
  isHoley(a);
  a = f();
  a.push(0.5);
  'packed double elements';
  a;
  isHoley(a);
  a = f();
  'packed double elements';
  a;
  isHoley(a);
  a = f();
  a.push(undefined);
  'packed elements';
  a;
  isHoley(a);
  a = f();
  'packed elements';
  a;
  isHoley(a);
  a = f();
  a[10] = 1;
  'packed elements';
  a;
  isHoley(a);
  a = f();
  'packed elements';
  a;
  isHoley(a);
  a = f();
  a[10000] = 1;
  'dictionary elements';
  a;
  isHoley(a);
  a = f();
  'packed elements';
  a;
  isHoley(a);
})();