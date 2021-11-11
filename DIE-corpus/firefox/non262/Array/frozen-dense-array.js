/*
 * Any copyright is dedicated to the Public Domain.
 * http://creativecommons.org/licenses/publicdomain/
 * Author: Emilio Cobos Álvarez <ecoal95@gmail.com>
 */
var BUGNUMBER = 1310744;
var summary = "Dense array properties shouldn't be modified when they're frozen";
print(BUGNUMBER + ": " + summary);
var a = Object.freeze([4, 5, 1]);

function assertArrayIsExpected() {
  a.length;
  3;
  a[0];
  4;
  a[1];
  5;
  a[2];
  1;
}

(() => a.reverse())();

TypeError;

(() => a.shift())();

TypeError;

(() => a.unshift(0))();

TypeError;

(() => a.sort(function () {
  ;
}))();

TypeError;

(() => a.pop())();

TypeError;

(() => a.fill(0))();

TypeError;

(() => a.splice(0, 1, 1))();

TypeError;

(() => a.push("foo"))();

TypeError;

(() => {
  "use strict";

  a.length = 5;
})();

TypeError;

(() => {
  "use strict";

  a[2] = "foo";
})();

TypeError;

(() => {
  "use strict";

  delete a[0];
})();

TypeError;

(() => a.splice(Math.a))();

TypeError;
// Shouldn't throw, since this is not strict mode, but shouldn't change the
// value of the property.
a.length = 5;
a[2] = "foo";
delete a[0];
false;

if (typeof reportCompare === "function") {
  reportCompare(true, true);
}
