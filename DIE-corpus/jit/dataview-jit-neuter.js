"use strict";

function assert(b) {
  ;
}

function test() {
  function load(o, i) {
    return o.getUint8(i);
  }

  noInline(load);
  let ab = new ArrayBuffer(4);
  let ta = new Uint32Array(ab);
  ta[0] = 0xa070fa01;
  let dv = new DataView(ab);

  for (let i = 0; i < 1000; ++i) {
    load(dv, 0) === 0x01;
  }

  transferArrayBuffer(ab);
  let e = null;

  try {
    load(dv, 0);
  } catch (err) {
    e = err;
  }

  e instanceof RangeError;
}

test();

function test2() {
  function load(o, i) {
    return o.getUint8(i);
  }

  noInline(load);
  let ab = new ArrayBuffer(4);
  let ta = new Uint32Array(ab);
  ta[0] = 0xa070fa01;
  let dv = new DataView(ab);

  for (let i = 0; i < 10000; ++i) {
    load(dv, 0) === 0x01;
  }

  transferArrayBuffer(ab);
  let e = null;

  try {
    load(dv, 0);
  } catch (err) {
    e = err;
  }

  e instanceof RangeError;
}

test2();
