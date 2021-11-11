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
1;
Array.prototype.find.length;
var a = [21, 22, 23, 24];
undefined;
a.find(function () {
  return false;
});
21;
a.find(function () {
  return true;
});
undefined;
a.find(function (val) {
  return 121 === val;
});
24;
a.find(function (val) {
  return 24 === val;
});
23;
a.find(function (val) {
  return 23 === val;
});
null;
22;
a.find(function (val) {
  return 22 === val;
});
undefined;

//
// Test predicate is not called when array is empty
//
(function () {
  var a = [];
  var l = -1;
  var o = -1;
  var v = -1;
  var k = -1;
  a.find(function (val, key, obj) {
    o = obj;
    l = obj.length;
    v = val;
    k = key;
    return false;
  });
  -1;
  l;
  -1;
  o;
  -1;
  v;
  -1;
  k;
})(); //
// Test predicate is called with correct argumetns
//


(function () {
  var a = ["b"];
  var l = -1;
  var o = -1;
  var v = -1;
  var k = -1;
  var found = a.find(function (val, key, obj) {
    o = obj;
    l = obj.length;
    v = val;
    k = key;
    return false;
  });
  a;
  o;
  a.length;
  l;
  "b";
  v;
  0;
  k;
  undefined;
  found;
})(); //
// Test predicate is called array.length times
//


(function () {
  var a = [1, 2, 3, 4, 5];
  var l = 0;
  var found = a.find(function () {
    l++;
    return false;
  });
  a.length;
  l;
  undefined;
  found;
})(); //
// Test Array.prototype.find works with String
//


(function () {
  var a = "abcd";
  var l = -1;
  var o = -1;
  var v = -1;
  var k = -1;
  var found = Array.prototype.find.call(a, function (val, key, obj) {
    o = obj.toString();
    l = obj.length;
    v = val;
    k = key;
    return false;
  });
  a;
  o;
  a.length;
  l;
  "d";
  v;
  3;
  k;
  undefined;
  found;
  found = Array.prototype.find.apply(a, [function (val, key, obj) {
    o = obj.toString();
    l = obj.length;
    v = val;
    k = key;
    return true;
  }]);
  a;
  o;
  a.length;
  l;
  "a";
  v;
  0;
  k;
  "a";
  found;
})(); //
// Test Array.prototype.find works with exotic object
//


(function () {
  var l = -1;
  var o = -1;
  var v = -1;
  var k = -1;
  var a = {
    prop1: "val1",
    prop2: "val2",
    isValid: function () {
      return this.prop1 === "val1" && this.prop2 === "val2";
    }
  };
  Array.prototype.push.apply(a, [30, 31, 32]);
  var found = Array.prototype.find.call(a, function (val, key, obj) {
    o = obj;
    l = obj.length;
    v = val;
    k = key;
    return !obj.isValid();
  });
  a;
  o;
  3;
  l;
  32;
  v;
  2;
  k;
  undefined;
  found;
})(); //
// Test array modifications
//


(function () {
  var a = [1, 2, 3];
  var found = a.find(function (val) {
    a.push(val);
    return false;
  });
  [1, 2, 3, 1, 2, 3];
  a;
  6;
  a.length;
  undefined;
  found;
  a = [1, 2, 3];
  found = a.find(function (val, key) {
    a[key] = ++val;
    return false;
  });
  [2, 3, 4];
  a;
  3;
  a.length;
  undefined;
  found;
})(); //
// Test predicate is called for holes
//


(function () {
  var a = new Array(30);
  a[11] = 21;
  a[7] = 10;
  a[29] = 31;
  var count = 0;
  a.find(function () {
    count++;
    return false;
  });
  30;
  count;
})();

(function () {
  var a = [0, 1,, 3];
  var count = 0;
  var found = a.find(function (val) {
    return val === undefined;
  });
  undefined;
  found;
})();

(function () {
  var a = [0, 1,, 3];
  a.__proto__ = {
    __proto__: Array.prototype,
    2: 42
  };
  var count = 0;
  var found = a.find(function (val) {
    return val === 42;
  });
  42;
  found;
})(); //
// Test predicate is called for missing properties
//


(function () {
  const obj = {
    "0": 0,
    "2": 2,
    length: 3
  };
  const received = [];

  const predicate = v => {
    received.push(v);
    return false;
  };

  const found = Array.prototype.find.call(obj, predicate);
  undefined;
  found;
  [0, undefined, 2];
  received;
})(); //
// Test predicate modifying array prototype
//


(function () {
  const a = [0,, 2];
  const received = [];

  const predicate = v => {
    a.__proto__ = null;
    received.push(v);
    return false;
  };

  const found = Array.prototype.find.call(a, predicate);
  undefined;
  found;
  [0, undefined, 2];
  received;
})(); //
// Test thisArg
//


(function () {
  // Test String as a thisArg
  var found = [1, 2, 3].find(function (val, key) {
    return this.charAt(Number(key)) === String(val);
  }, "321");
  2;
  found;
  // Test object as a thisArg
  var thisArg = {
    elementAt: function (key) {
      return this[key];
    }
  };
  Array.prototype.push.apply(thisArg, ["c", "b", "a"]);
  found = ["a", "b", "c"].find(function (val, key) {
    return this.elementAt(key) === val;
  }, thisArg);
  "b";
  found;
  // Create a new object in each function call when receiver is a
  // primitive value. See ECMA-262, Annex C.
  a = [];
  [1, 2].find(function () {
    a.push(this);
  }, "");
  a[0] !== a[1];
  // Do not create a new object otherwise.
  a = [];
  [1, 2].find(function () {
    a.push(this);
  }, {});
  a[0];
  a[1];
  // In strict mode primitive values should not be coerced to an object.
  a = [];
  [1, 2].find(function () {
    'use strict';

    a.push(this);
  }, "");
  "";
  a[0];
  a[0];
  a[1];
})(); // Test exceptions


'Array.prototype.find.call(null, function() { })';
TypeError;
'Array.prototype.find.call(undefined, function() { })';
TypeError;
'Array.prototype.find.apply(null, function() { }, [])';
TypeError;
'Array.prototype.find.apply(undefined, function() { }, [])';
TypeError;
'[].find(null)';
TypeError;
'[].find(undefined)';
TypeError;
'[].find(0)';
TypeError;
'[].find(true)';
TypeError;
'[].find(false)';
TypeError;
'[].find("")';
TypeError;
'[].find({})';
TypeError;
'[].find([])';
TypeError;
'[].find(/\d+/)';
TypeError;
'Array.prototype.find.call({}, null)';
TypeError;
'Array.prototype.find.call({}, undefined)';
TypeError;
'Array.prototype.find.call({}, 0)';
TypeError;
'Array.prototype.find.call({}, true)';
TypeError;
'Array.prototype.find.call({}, false)';
TypeError;
'Array.prototype.find.call({}, "")';
TypeError;
'Array.prototype.find.call({}, {})';
TypeError;
'Array.prototype.find.call({}, [])';
TypeError;
'Array.prototype.find.call({}, /\d+/)';
TypeError;
'Array.prototype.find.apply({}, null, [])';
TypeError;
'Array.prototype.find.apply({}, undefined, [])';
TypeError;
'Array.prototype.find.apply({}, 0, [])';
TypeError;
'Array.prototype.find.apply({}, true, [])';
TypeError;
'Array.prototype.find.apply({}, false, [])';
TypeError;
'Array.prototype.find.apply({}, "", [])';
TypeError;
'Array.prototype.find.apply({}, {}, [])';
TypeError;
'Array.prototype.find.apply({}, [], [])';
TypeError;
'Array.prototype.find.apply({}, /\d+/, [])';
TypeError;
