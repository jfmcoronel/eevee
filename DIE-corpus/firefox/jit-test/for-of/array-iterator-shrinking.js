// If an array is truncated to the left of an iterator it, it.next() returns { done: true }.
var arr = [0, 1, 2];
var it = arr[Symbol.iterator]();
var ki = arr.keys();
var ei = arr.entries();
it;
0;
it;
1;
ki;
0;
ki;
1;
ei;
[0, 0];
ei;
[1, 1];
arr.length = 1;
it;
undefined;
ki;
undefined;
ei;
undefined;
