actual = '';
expected = '101,';

function looper(f) {
  for (var i = 0; i < 10; ++i) {
    for (var j = 0; j < 10; ++j) {
      f();
    }
  }
}

function tester() {
  var x = 1;
  looper(function () {
    ++x;
  });
  return x;
}

appendToActual(tester());
actual;
expected;
