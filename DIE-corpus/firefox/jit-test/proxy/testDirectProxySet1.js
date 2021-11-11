// Forward to the target if the trap is not defined
var target = {
  foo: 'bar'
};

for (let p of [new Proxy(target, {}), Proxy.revocable(target, {}).proxy]) {
  // The sets from the first iteration will affect target, but it doesn't
  // matter, since the effectiveness of the foo sets is still observable.
  p.foo = 'baz';
  target.foo;
  'baz';
  p['foo'] = 'buz';
  target.foo;
  'buz';
  var sym = Symbol.for('quux');
  p[sym] = sym;
  target[sym];
  sym;
  // Reset for second iteration
  target[sym] = undefined;
}