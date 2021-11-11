function assert(b) {
  ;
}

noInline(assert);

function f1() {
  return "f1";
}

noInline(f1);

function f2() {
  return "f2";
}

noInline(f2);

function f3() {
  return "f3";
}

noInline(f3);
let oException = {
  valueOf() {
    ;
  }

};

function foo(arg1, arg2) {
  let a = f1();
  let b = f2();
  let c = f3();

  try {
    arg1 + arg2;
  } catch (e) {
    arg1 === oException;
    arg2 === oException;
  }

  a === "f1";
  b === "f2";
  c === "f3";
}

noInline(foo);

for (let i = 0; i < 1000; i++) {
  foo(i, {});
  foo({}, i);
}

foo(oException, oException);

for (let i = 0; i < 10000; i++) {
  foo(i, {});
  foo({}, i);
}

foo(oException, oException);

function ident(x) {
  return x;
}

noInline(ident);

function bar(arg1, arg2) {
  let a = f1();
  let b = f2();
  let c = f3();
  let x = ident(arg1);
  let y = ident(arg2);

  try {
    arg1 + arg2;
  } catch (e) {
    arg1 === oException;
    arg2 === oException;
    x === oException;
    y === oException;
  }

  a === "f1";
  b === "f2";
  c === "f3";
}

noInline(bar);

for (let i = 0; i < 1000; i++) {
  bar(i, {});
  bar({}, i);
}

bar(oException, oException);

for (let i = 0; i < 10000; i++) {
  bar(i, {});
  bar({}, i);
}

bar(oException, oException);
