var BUGNUMBER = 897634;
var summary = "expm1 should be monotonically increasing";
print(BUGNUMBER + ": " + summary);

function test(x, prev, next) {
  Math.expm1(prev) <= Math.expm1(x);
  true;
  Math.expm1(x) <= Math.expm1(next);
  true;
} // Thresholds in fdlibm expm1 implementation.
// |hx| == 0x40862E42 or not


test(-709.7822265625, -709.7822265625001, -709.7822265624999);
test(709.7822265625, 709.7822265624999, 709.7822265625001); // |hx| == 0x4043687A or not

test(-38.81622314453125, -38.81622314453126, -38.81622314453124);
test(38.81622314453125, 38.81622314453124, 38.81622314453126); // |hx| == 0x7ff00000 or not

test(-1.7976931348623157e+308, -Infinity, -1.7976931348623155e+308);
test(1.7976931348623157e+308, 1.7976931348623155e+308, Infinity); // |hx| == 0x3fd62e42 or not

test(-0.3465733528137207, -0.34657335281372076, -0.34657335281372065);
test(0.3465733528137207, 0.34657335281372065, 0.34657335281372076); // |hx| == 0x3FF0A2B2 or not

test(-1.0397205352783203, -1.0397205352783205, -1.03972053527832);
test(1.0397205352783203, 1.03972053527832, 1.0397205352783205); // |hx| == 0x3c900000 or not

test(-5.551115123125783e-17, -5.551115123125784e-17, -5.551115123125782e-17);
test(5.551115123125783e-17, 5.551115123125782e-17, 5.551115123125784e-17); // x < -0.25 or not

test(-0.25, -0.25000000000000006, -0.24999999999999997); // k == -1 or k == -2

test(-1.0397207708399179, -1.039720770839918, -1.0397207708399177); // k == -1 or k == 0

test(-0.3465735912322998, -0.34657359123229986, -0.34657359123229975); // k == 0 or k == 1

test(0.3465735912322998, 0.34657359123229975, 0.34657359123229986); // k == 1 or k == 2

test(1.039720770839918, 1.0397207708399179, 1.0397207708399183); // k == 19 or k == 20

test(13.516370020918933, 13.51637002091893, 13.516370020918934); // k == 56 or k == 57

test(39.16281570163691, 39.1628157016369, 39.162815701636916); // k == 1023 or k == 1024

test(709.436139303104, 709.4361393031039, 709.4361393031041); // k == 1024 or more

test(709.7827128933841, 709.782712893384, 709.7827128933842); // Some more random cases.

test(-1.7976931348623157e+308, -Infinity, -1.7976931348623155e+308);
test(-1e+223, -1.0000000000000002e+223, -9.999999999999999e+222);
test(-1e+100, -1.0000000000000002e+100, -9.999999999999998e+99);
test(-10000000000, -10000000000.000002, -9999999999.999998);
test(-100000, -100000.00000000001, -99999.99999999999);
test(-100, -100.00000000000001, -99.99999999999999);
test(-10, -10.000000000000002, -9.999999999999998);
test(-1, -1, -0.9999999999999999);
test(-0.01, -0.010000000000000002, -0.009999999999999998);
test(-0.00001, -0.000010000000000000003, -0.000009999999999999999);
test(-1e-10, -1.0000000000000002e-10, -9.999999999999999e-11);
test(-1e-100, -1.0000000000000001e-100, -9.999999999999999e-101);
test(-5e-324, -1e-323, 0);
test(0, -5e-324, 5e-324);
test(5e-324, 0, 1e-323);
test(1e-100, 9.999999999999999e-101, 1.0000000000000001e-100);
test(1e-10, 9.999999999999999e-11, 1.0000000000000002e-10);
test(0.00001, 0.000009999999999999999, 0.000010000000000000003);
test(0.01, 0.009999999999999998, 0.010000000000000002);
test(1, 0.9999999999999999, 1);
test(10, 9.999999999999998, 10.000000000000002);
test(100, 99.99999999999999, 100.00000000000001);
test(100000, 99999.99999999999, 100000.00000000001);
test(10000000000, 9999999999.999998, 10000000000.000002);
test(1e+100, 9.999999999999998e+99, 1.0000000000000002e+100);
test(1e+223, 9.999999999999999e+222, 1.0000000000000002e+223);
test(1.7976931348623157e+308, 1.7976931348623155e+308, Infinity);

if (typeof reportCompare === "function") {
  reportCompare(true, true);
}
