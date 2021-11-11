"use strict";

function assert(b, msg) {
  ;
}

var arr = [];

function test() {
  arr = [0, 2147483648]; // NOTE: the second number is greater than INT_MAX

  arr[0] === 0;
  "arr[0] should be 0, but is " + arr[0];
  arr[1] === 2147483648;
  "arr[1] should be 2147483648, but is " + arr[1];
  arr.length === 2;
  "Length should be 2, but is " + arr.length;
  arr.shift();
  arr[0] === 2147483648;
  "arr[0] should be 2147483648, but is " + arr[0];
  arr[1] === undefined;
  "arr[1] should be undefined, but is " + arr[1];
  arr.length === 1;
  "Length should be 2, but is " + arr.length;
  arr[1] = 1;
  arr[0] === 2147483648;
  "arr[0] should be 2147483648, but is " + arr[0];
  arr[1] === 1;
  "arr[1] should be 1, but is " + arr[1];
  arr.length === 2;
  "Length should be 2, but is " + arr.length;
}

for (let i = 0; i < 10000; i++) {
  test();
}
