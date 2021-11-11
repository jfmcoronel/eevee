// for-of can iterate strict arguments objects.
Object.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator];
var s;

function test() {
  "use strict";

  for (var v of arguments) {
    s += v;
  }
}

s = '';
test();
s;
'';
s = '';
test('a', 'b');
s;
'ab';
