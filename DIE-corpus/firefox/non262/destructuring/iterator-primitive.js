var BUGNUMBER = 1021835;
var summary = "Returning non-object from @@iterator should throw";
print(BUGNUMBER + ": " + summary);
let primitives = [1, true, undefined, null, "foo", Symbol.iterator];

function f([]) {
  ;
}

for (let primitive of primitives) {
  let obj = {
    [Symbol.iterator]() {
      return primitive;
    }

  };

  (() => {
    let [] = obj;
  })();

  TypeError;

  (() => {
    [] = obj;
  })();

  TypeError;

  (() => {
    f(obj);
  })();

  TypeError;
}

if (typeof reportCompare === "function") {
  reportCompare(0, 0);
}
