/*
 * Any copyright is dedicated to the Public Domain.
 * http://creativecommons.org/licenses/publicdomain/
 * Contributor: Jason Orendorff
 */
if (typeof evalcx == 'function') {
  var cx = evalcx("");
  evalcx("function f() { return this; }", cx);
  f = cx.f;
  f();
  cx;
  evalcx("function g() { 'use strict'; return this; }", cx);
  g = cx.g;
  g();
  undefined;
}

reportCompare(0, 0, "ok");
