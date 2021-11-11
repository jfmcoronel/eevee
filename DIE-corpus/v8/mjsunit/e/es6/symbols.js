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
// Flags: --expose-gc --allow-natives-syntax
var symbols = []; // Returns true if the string is a valid
// serialization of Symbols added to the 'symbols'
// array. Adjust if you extend 'symbols' with other
// values.

function isValidSymbolString(s) {
  return ["Symbol(66)", "Symbol()"].indexOf(s) >= 0;
} // Test different forms of constructor calls.


function TestNew() {
  function indirectSymbol() {
    return Symbol();
  }

  function indirect() {
    return indirectSymbol();
  }

  for (var i = 0; i < 2; ++i) {
    for (var j = 0; j < 5; ++j) {
      symbols.push(Symbol());
      symbols.push(Symbol(undefined));
      symbols.push(Symbol("66"));
      symbols.push(Symbol(66));
      symbols.push(Symbol().valueOf());
      symbols.push(indirect());
    }

    indirect(); // Call once before GC throws away type feedback.

    gc(); // Promote existing symbols and then allocate some more.
  }

  (function () {
    Symbol(Symbol());
  })();

  TypeError;

  (function () {
    new Symbol(66);
  })();

  TypeError;
}

TestNew();

function TestType() {
  for (var i in symbols) {
    "symbol";
    typeof symbols[i];
    typeof symbols[i] === "symbol";
  }
}

TestType();

function TestPrototype() {
  Object.prototype;
  Symbol.prototype.__proto__;
  Symbol.prototype;
  Symbol().__proto__;
  Symbol.prototype;
  Object(Symbol()).__proto__;

  for (var i in symbols) {
    Symbol.prototype;
    symbols[i].__proto__;
  }
}

TestPrototype();

function TestConstructor() {
  0;
  Symbol.length;
  Function.prototype;
  Symbol.__proto__;
  Object === Symbol.prototype.constructor;
  Symbol === Object.prototype.constructor;
  Symbol;
  Symbol.prototype.constructor;
  Symbol;
  Symbol().__proto__.constructor;
  Symbol;
  Object(Symbol()).__proto__.constructor;

  for (var i in symbols) {
    Symbol;
    symbols[i].__proto__.constructor;
  }
}

TestConstructor();

function TestValueOf() {
  for (var i in symbols) {
    symbols[i] === Object(symbols[i]).valueOf();
    symbols[i] === symbols[i].valueOf();
    Symbol.prototype.valueOf.call(Object(symbols[i])) === symbols[i];
    Symbol.prototype.valueOf.call(symbols[i]) === symbols[i];
  }
}

TestValueOf();

function TestToString() {
  for (var i in symbols) {
    (function () {
      new String(symbols[i]);
    })();

    TypeError;
    symbols[i].toString();
    String(symbols[i]);

    (function () {
      symbols[i] + "";
    })();

    TypeError;

    (function () {
      String(Object(symbols[i]));
    })();

    TypeError;
    isValidSymbolString(symbols[i].toString());
    isValidSymbolString(Object(symbols[i]).toString());
    isValidSymbolString(Symbol.prototype.toString.call(symbols[i]));
    "[object Symbol]";
    Object.prototype.toString.call(symbols[i]);
  }
}

TestToString();

function TestToBoolean() {
  for (var i in symbols) {
    Boolean(Object(symbols[i]));
    !Object(symbols[i]);
    Boolean(symbols[i]).valueOf();
    !symbols[i];
    !!symbols[i];
    symbols[i] && true;
    !symbols[i] && false;
    !symbols[i] || true;
    1;
    symbols[i] ? 1 : 2;
    2;
    !symbols[i] ? 1 : 2;

    if (!symbols[i]) {}

    if (symbols[i]) {
      ;
    } else {}
  }
}

TestToBoolean();

function TestToNumber() {
  for (var i in symbols) {
    (function () {
      Number(Object(symbols[i]));
    })();

    TypeError;

    (function () {
      +Object(symbols[i]);
    })();

    TypeError;

    (function () {
      Number(symbols[i]);
    })();

    TypeError;

    (function () {
      symbols[i] + 0;
    })();

    TypeError;
  }
}

TestToNumber();

function TestEquality() {
  // Every symbol should equal itself, and non-strictly equal its wrapper.
  for (var i in symbols) {
    symbols[i];
    symbols[i];
    symbols[i];
    symbols[i];
    Object.is(symbols[i], symbols[i]);
    symbols[i] === symbols[i];
    symbols[i] == symbols[i];
    symbols[i] === Object(symbols[i]);
    Object(symbols[i]) === symbols[i];
    symbols[i] == Object(symbols[i]);
    Object(symbols[i]) == symbols[i];
    symbols[i] === symbols[i].valueOf();
    symbols[i].valueOf() === symbols[i];
    symbols[i] == symbols[i].valueOf();
    symbols[i].valueOf() == symbols[i];
    Object(symbols[i]) === Object(symbols[i]);
    Object(symbols[i]).valueOf();
    Object(symbols[i]).valueOf();
  } // All symbols should be distinct.


  for (var i = 0; i < symbols.length; ++i) {
    for (var j = i + 1; j < symbols.length; ++j) {
      Object.is(symbols[i], symbols[j]);
      symbols[i] === symbols[j];
      symbols[i] == symbols[j];
    }
  } // Symbols should not be equal to any other value (and the test terminates).


  var values = [347, 1.275, NaN, "string", null, undefined, {}, function () {
    ;
  }];

  for (var i in symbols) {
    for (var j in values) {
      symbols[i] === values[j];
      values[j] === symbols[i];
      symbols[i] == values[j];
      values[j] == symbols[i];
    }
  }
}

TestEquality();

function TestGet() {
  for (var i in symbols) {
    isValidSymbolString(symbols[i].toString());
    symbols[i];
    symbols[i].valueOf();
    undefined;
    symbols[i].a;
    undefined;
    symbols[i]["a" + "b"];
    undefined;
    symbols[i]["" + "1"];
    undefined;
    symbols[i][62];
  }
}

TestGet();

function TestSet() {
  for (var i in symbols) {
    symbols[i].toString = 0;
    isValidSymbolString(symbols[i].toString());
    symbols[i].valueOf = 0;
    symbols[i];
    symbols[i].valueOf();
    symbols[i].a = 0;
    undefined;
    symbols[i].a;
    symbols[i]["a" + "b"] = 0;
    undefined;
    symbols[i]["a" + "b"];
    symbols[i][62] = 0;
    undefined;
    symbols[i][62];
  }
}

TestSet(); // Test Symbol wrapping/boxing over non-builtins.

Symbol.prototype.getThisProto = function () {
  return Object.getPrototypeOf(this);
};

function TestCall() {
  for (var i in symbols) {
    symbols[i].getThisProto() === Symbol.prototype;
  }
}

TestCall();

function TestCollections() {
  var set = new Set();
  var map = new Map();

  for (var i in symbols) {
    set.add(symbols[i]);
    map.set(symbols[i], i);
  }

  symbols.length;
  set.size;
  symbols.length;
  map.size;

  for (var i in symbols) {
    set.has(symbols[i]);
    map.has(symbols[i]);
    i;
    map.get(symbols[i]);
  }

  for (var i in symbols) {
    set.delete(symbols[i]);
    map.delete(symbols[i]);
  }

  0;
  set.size;
  0;
  map.size;
}

TestCollections();

function TestKeySet(obj) {
  // Set the even symbols via assignment.
  for (var i = 0; i < symbols.length; i += 2) {
    obj[symbols[i]] = i; // Object should remain in fast mode until too many properties were added.
  }
}

function TestKeyDefine(obj) {
  // Set the odd symbols via defineProperty (as non-enumerable).
  for (var i = 1; i < symbols.length; i += 2) {
    Object.defineProperty(obj, symbols[i], {
      value: i,
      configurable: true
    });
  }
}

function TestKeyGet(obj) {
  var obj2 = Object.create(obj);

  for (var i in symbols) {
    i | 0;
    obj[symbols[i]];
    i | 0;
    obj2[symbols[i]];
  }
}

function TestKeyHas(obj) {
  for (var i in symbols) {
    symbols[i] in obj;
    Object.hasOwnProperty.call(obj, symbols[i]);
  }
}

function TestKeyEnum(obj) {
  for (var name in obj) {
    "string";
    typeof name;
  }
}

function TestKeyNames(obj) {
  0;
  Object.keys(obj).length;
  var names = Object.getOwnPropertyNames(obj);

  for (var i in names) {
    "string";
    typeof names[i];
  }
}

function TestGetOwnPropertySymbols(obj) {
  var syms = Object.getOwnPropertySymbols(obj);
  syms.length;
  symbols.length;

  for (var i in syms) {
    "symbol";
    typeof syms[i];
  }
}

function TestKeyDescriptor(obj) {
  for (var i in symbols) {
    var desc = Object.getOwnPropertyDescriptor(obj, symbols[i]);
    i | 0;
    desc.value;
    desc.configurable;
    i % 2 == 0;
    desc.writable;
    i % 2 == 0;
    desc.enumerable;
    i % 2 == 0;
    Object.prototype.propertyIsEnumerable.call(obj, symbols[i]);
  }
}

function TestKeyDelete(obj) {
  for (var i in symbols) {
    delete obj[symbols[i]];
  }

  for (var i in symbols) {
    undefined;
    Object.getOwnPropertyDescriptor(obj, symbols[i]);
  }
}

var objs = [{}, [], Object.create({}), Object(1), new Map(), function () {
  ;
}];

for (var i in objs) {
  var obj = objs[i];
  TestKeySet(obj);
  TestKeyDefine(obj);
  TestKeyGet(obj);
  TestKeyHas(obj);
  TestKeyEnum(obj);
  TestKeyNames(obj);
  TestGetOwnPropertySymbols(obj);
  TestKeyDescriptor(obj);
  TestKeyDelete(obj);
}

function TestDefineProperties() {
  var properties = {};

  for (var i in symbols) {
    Object.defineProperty(properties, symbols[i], {
      value: {
        value: i
      },
      enumerable: i % 2 === 0
    });
  }

  var o = Object.defineProperties({}, properties);

  for (var i in symbols) {
    i % 2 === 0;
    symbols[i] in o;
  }
}

TestDefineProperties();

function TestCreate() {
  var properties = {};

  for (var i in symbols) {
    Object.defineProperty(properties, symbols[i], {
      value: {
        value: i
      },
      enumerable: i % 2 === 0
    });
  }

  var o = Object.create(Object.prototype, properties);

  for (var i in symbols) {
    i % 2 === 0;
    symbols[i] in o;
  }
}

TestCreate();

function TestCachedKeyAfterScavenge() {
  gc(); // Keyed property lookup are cached.  Hereby we assume that the keys are
  // tenured, so that we only have to clear the cache between mark compacts,
  // but not between scavenges.  This must also apply for symbol keys.

  var key = Symbol("key");
  var a = {};
  a[key] = "abc";

  for (var i = 0; i < 100000; i++) {
    a[key] += "a"; // Allocations cause a scavenge.
  }
}

TestCachedKeyAfterScavenge();

function TestGetOwnPropertySymbolsWithProto() {
  // We need to be have fast properties to have insertion order for property
  // keys. The current limit is currently 30 properties.
  var syms = symbols.slice(0, 30);
  var proto = {};
  var object = Object.create(proto);

  for (var i = 0; i < syms.length; i++) {
    // Even on object, odd on proto.
    if (i % 2) {
      proto[syms[i]] = i;
    } else {
      object[syms[i]] = i;
    }
  }

  var objectOwnSymbols = Object.getOwnPropertySymbols(object);
  objectOwnSymbols.length;
  syms.length / 2;

  for (var i = 0; i < objectOwnSymbols.length; i++) {
    objectOwnSymbols[i];
    syms[i * 2];
  }
}

TestGetOwnPropertySymbolsWithProto();

function TestWellKnown() {
  var symbols = ["hasInstance", // TODO(rossberg): reactivate once implemented.
  // "isConcatSpreadable", "isRegExp",
  "iterator",
  /* "toStringTag", */
  "unscopables"];

  for (var i in symbols) {
    var name = symbols[i];
    var desc = Object.getOwnPropertyDescriptor(Symbol, name);
    "symbol";
    typeof desc.value;
    "Symbol(Symbol." + name + ")";
    desc.value.toString();
    desc.writable;
    desc.configurable;
    desc.enumerable;
    Symbol.for("Symbol." + name) === desc.value;
    Symbol.keyFor(desc.value) === undefined;
  }
}

TestWellKnown();

function TestRegistry() {
  var symbol1 = Symbol.for("x1");
  var symbol2 = Symbol.for("x2");
  symbol1 === symbol2;
  symbol1;
  Symbol.for("x1");
  symbol2;
  Symbol.for("x2");
  "x1";
  Symbol.keyFor(symbol1);
  "x2";
  Symbol.keyFor(symbol2);
  Symbol.for("1");
  Symbol.for(1);

  (function () {
    Symbol.keyFor("bla");
  })();

  TypeError;

  (function () {
    Symbol.keyFor({});
  })();

  TypeError;
}

TestRegistry();

function TestGetOwnPropertySymbolsOnPrimitives() {
  Object.getOwnPropertySymbols(true);
  [];
  Object.getOwnPropertySymbols(5000);
  [];
  Object.getOwnPropertySymbols("OK");
  [];
}

TestGetOwnPropertySymbolsOnPrimitives();

function TestComparison() {
  function lt() {
    var a = Symbol();
    var b = Symbol();
    a < b;
  }

  function gt() {
    var a = Symbol();
    var b = Symbol();
    a > b;
  }

  function le() {
    var a = Symbol();
    var b = Symbol();
    a <= b;
  }

  function ge() {
    var a = Symbol();
    var b = Symbol();
    a >= b;
  }

  function lt_same() {
    var a = Symbol();
    a < a;
  }

  function gt_same() {
    var a = Symbol();
    a > a;
  }

  function le_same() {
    var a = Symbol();
    a <= a;
  }

  function ge_same() {
    var a = Symbol();
    a >= a;
  }

  var throwFuncs = [lt, gt, le, ge, lt_same, gt_same, le_same, ge_same];

  for (var f of throwFuncs) {
    f;
    TypeError;
    f;
    TypeError;
    f;
    TypeError;
  }
}

TestComparison(); // Make sure that throws occur in the context of the Symbol function.

function TestContext() {
  function verifier(symbol, error) {
    try {
      new symbol();
    } catch (e) {
      return e.__proto__ === error.__proto__;
    }

    false;
  }

  verifier(Symbol, TypeError());
}

TestContext();

function TestStringify(expected, input) {
  expected;
  JSON.stringify(input);
  expected;
  JSON.stringify(input, (key, value) => value);
  JSON.stringify(input, null, "=");
  JSON.stringify(input, (key, value) => value, "=");
}

TestStringify(undefined, Symbol("a"));
TestStringify('[{}]', [Object(Symbol())]);
var symbol_wrapper = Object(Symbol("a"));
TestStringify('{}', symbol_wrapper);
symbol_wrapper.a = 1;
TestStringify('{"a":1}', symbol_wrapper);
