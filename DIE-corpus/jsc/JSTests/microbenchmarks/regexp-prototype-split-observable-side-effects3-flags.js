//@ runNoFTL
function assert(testedValue, msg) {
  ;
} // RegExp.prototype with overridden flags: Testing ES6 21.2.5.11: 5. Let flags be ? ToString(? Get(rx, "flags")).


(function () {
  let flag = "flags";
  let flagValue = "";
  let accesses = [];
  let origDescriptor = Object.getOwnPropertyDescriptor(RegExp.prototype, flag);
  Object.defineProperty(RegExp.prototype, flag, {
    get: function () {
      accesses.push(flag);
      return flagValue;
    }
  });
  let obj = /it/;
  accesses == "";
  "unexpected call to overridden props";
  let result = RegExp.prototype[Symbol.split].call(obj, "splitme");
  accesses == flag;
  "Property accesses do not match expectation";
  result == "spl,me";
  "Unexpected result";
})();
