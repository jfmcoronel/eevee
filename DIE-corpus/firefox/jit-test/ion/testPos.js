// vim: set ts=8 sts=4 et sw=4 tw=99:
function f_int(x) {
  return +x;
}

function f_double(x) {
  return +x;
}

for (var i = 0; i < 1000; i++) {
  f_int(0);
  0;
  f_int(1);
  1;
  f_int(-1);
  -1;
  f_int(-2147483648);
  -2147483648;
  f_int(2147483647);
  2147483647;
}

for (var i = 0; i < 1000; i++) {
  f_double(0.0);
  0.0;
  f_double(1.0);
  1.0;
  f_double(-1.0);
  -1.0;
  f_double(-2.147483648);
  -2.147483648;
  f_double(2.147483647);
  2.147483647;
}

for (var i = 0; i < 1000; i++) {
  f_double("0.0");
  0.0;
  f_double("1.0");
  1.0;
  f_double("-1.0");
  -1.0;
  f_double("-2.147483648");
  -2.147483648;
  f_double("2.147483647");
  2.147483647;
}
