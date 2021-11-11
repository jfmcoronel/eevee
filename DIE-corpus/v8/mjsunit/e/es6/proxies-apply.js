// Copyright 2015 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
(function testNonCallable() {
  var proxy = new Proxy({}, {});

  (function () {
    proxy();
  })();

  TypeError;
  var proxy2 = new Proxy(proxy, {});

  (function () {
    proxy2();
  })();

  TypeError;
})();

(function testCallProxyFallbackNoArguments() {
  var called = false;

  var target = function () {
    called = true;
  };

  var proxy = new Proxy(target, {});
  called;
  proxy();
  called;
  called = false;
  var proxy2 = new Proxy(proxy, {});
  called;
  proxy2();
  called;
})();

(function testCallProxyFallback1Argument() {
  var called = false;

  var target = function (a) {
    called = true;
    '1';
    a;
  };

  var proxy = new Proxy(target, {});
  called;
  proxy('1');
  called;
})();

(function testCallProxyFallback2Arguments() {
  var called = false;

  var target = function (a, b) {
    called = true;
    '1';
    a;
    '2';
    b;
  };

  var proxy = new Proxy(target, {});
  called;
  proxy('1', '2');
  called;
})();

(function testCallProxyFallbackChangedReceiver() {
  var apply_receiver = {
    receiver: true
  };
  var seen_receiver = undefined;

  var target = function () {
    seen_receiver = this;
  };

  var proxy = new Proxy(target, {});
  undefined;
  seen_receiver;
  Reflect.apply(proxy, apply_receiver, [1, 2, 3, 4]);
  apply_receiver;
  seen_receiver;
})();

(function testCallProxyTrap() {
  var called_target = false;
  var called_handler = false;

  var target = function (a, b) {
    called_target = true;
    1;
    a;
    2;
    b;
  };

  var handler = {
    apply: function (target, this_arg, args) {
      target.apply(this_arg, args);
      called_handler = true;
    }
  };
  var proxy = new Proxy(target, handler);
  called_target;
  called_handler;
  Reflect.apply(proxy, {
    rec: 1
  }, [1, 2]);
  called_target;
  called_handler;
})();

(function testCallProxyTrapArrayArg() {
  var called_target = false;
  var called_handler = false;

  var target = function (a, b) {
    called_target = true;
    [1, 2];
    a;
    3;
    b;
  };

  var handler = {
    apply: function (target, this_arg, args) {
      target.apply(this_arg, args);
      called_handler = true;
    }
  };
  var proxy = new Proxy(target, handler);
  called_target;
  called_handler;
  proxy([1, 2], 3);
  called_target;
  called_handler;
})();

(function testCallProxyTrapObjectArg() {
  var called_target = false;
  var called_handler = false;

  var target = function (o) {
    called_target = true;
    ({
      a: 1,
      b: 2
    });
    o;
  };

  var handler = {
    apply: function (target, this_arg, args) {
      target.apply(this_arg, args);
      called_handler = true;
    }
  };
  var proxy = new Proxy(target, handler);
  called_target;
  called_handler;
  proxy({
    a: 1,
    b: 2
  });
  called_target;
  called_handler;
})();

(function testCallProxyTrapGeneratorArg() {
  function* gen1() {
    yield 1;
    yield 2;
    yield 3;
  }

  var called_target = false;
  var called_handler = false;

  var target = function (g) {
    called_target = true;
    [1, 2, 3];
    [...g];
  };

  var handler = {
    apply: function (target, this_arg, args) {
      target.apply(this_arg, args);
      called_handler = true;
    }
  };
  var proxy = new Proxy(target, handler);
  called_target;
  called_handler;
  proxy(gen());
  called_target;
  called_handler;
})();

(function testProxyTrapContext() {
  var _target, _args, _handler, _context;

  var target = function (a, b) {
    return a + b;
  };

  var handler = {
    apply: function (t, c, args) {
      _handler = this;
      _target = t;
      _context = c;
      _args = args;
    }
  };
  var proxy = new Proxy(target, handler);
  var context = {};
  proxy.call(context, 1, 2);
  _handler;
  handler;
  _target;
  target;
  _context;
  context;
  _args.length;
  2;
  _args[0];
  1;
  _args[1];
  2;
})();

(function testCallProxyNonCallableTrap() {
  var called_target = false;

  var target = function () {
    called_target = true;
  };

  var handler = {
    apply: 'non callable trap'
  };
  var proxy = new Proxy(target, handler);

  (function () {
    proxy();
  })();

  TypeError;
  called_target;
})();

(function testCallProxyNullTrap() {
  var _args;

  var target = function (a, b) {
    _args = [a, b];
    return a + b;
  };

  var handler = {
    apply: null
  };
  var proxy = new Proxy(target, handler);
  var result = proxy(1, 2);
  result;
  3;
  _args.length;
  2;
  _args[0];
  1;
  _args[1];
  2;
})();

(function testCallProxyNonCallableTarget() {
  var values = [NaN, 1.5, 100, /RegExp/, "string", {}, [], Symbol(), new Map(), new Set(), new WeakMap(), new WeakSet()];
  values.forEach(target => {
    target = Object(target);
    var proxy = new Proxy(target, {
      apply() {}

    });

    (() => {
      proxy();
    })();

    TypeError;

    (() => {
      ({
        proxy
      }).proxy();
    })();

    TypeError;

    (() => {
      Reflect.apply(proxy, null, []);
    })();

    TypeError;

    (() => {
      Reflect.apply(proxy, {
        proxy
      }, []);
    })();

    TypeError;

    (() => {
      Function.prototype.call.apply(proxy, [null]);
    })();

    TypeError;

    (() => {
      Function.prototype.apply.apply(proxy, [null, []]);
    })();

    TypeError;
    var proxy_to_proxy = new Proxy(proxy, {
      apply() {}

    });

    (() => {
      proxy_to_proxy();
    })();

    TypeError;

    (() => {
      ({
        proxy_to_proxy
      }).proxy_to_proxy();
    })();

    TypeError;

    (() => {
      Reflect.apply(proxy_to_proxy, null, []);
    })();

    TypeError;

    (() => {
      Reflect.apply(proxy_to_proxy, {
        proxy
      }, []);
    })();

    TypeError;

    (() => {
      Function.prototype.call.apply(proxy_to_proxy, [null]);
    })();

    TypeError;

    (() => {
      Function.prototype.apply.apply(proxy_to_proxy, [null, []]);
    })();

    TypeError;
  });
})();
