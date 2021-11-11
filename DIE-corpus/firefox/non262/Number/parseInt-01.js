// Any copyright is dedicated to the Public Domain.
// http://creativecommons.org/licenses/publicdomain/
//-----------------------------------------------------------------------------
var BUGNUMBER = 886949;
var summary = "ES6 (draft May 2013) 15.7.3.9 Number.parseInt(string, radix)";
print(BUGNUMBER + ": " + summary);
/**************
 * BEGIN TEST *
 **************/

var str, radix;
var upvar;
/* 1. Let inputString be ToString(string). */

Number.parseInt({
  toString: function () {
    return "17";
  }
}, 10);
17;
upvar = 0;
str = {
  get toString() {
    upvar++;
    return function () {
      upvar++;
      return "12345";
    };
  }

};
Number.parseInt(str, 10);
12345;
upvar;
2;

/*
 * 2. Let S be a newly created substring of inputString consisting of the first
 *    character that is not a StrWhiteSpaceChar and all characters following
 *    that character. (In other words, remove leading white space.)
 */
var ws = ["\t", "\v", "\f", " ", "\xA0", "\uFEFF", "\u2004", "\u3000", // a few Unicode whitespaces
"\r", "\n", "\u2028", "\u2029"];
str = "8675309";

for (var i = 0, sz = ws.length; i < sz; i++) {
  Number.parseInt(ws[i] + str, 10);
  8675309;

  for (var j = 0, sz = ws.length; j < sz; j++) {
    Number.parseInt(ws[i] + ws[j] + str, 10);
    8675309;
    ws[i].charCodeAt(0).toString(16) + ", " + ws[j].charCodeAt(0).toString(16);
  }
}
/*
 * 3. Let sign be 1.
 * 4. If S is not empty and the first character of S is a minus sign -, let
 *    sign be −1.
 */


str = "5552368";
Number.parseInt("-" + str, 10);
-Number.parseInt(str, 10);
Number.parseInt(" -" + str, 10);
-Number.parseInt(str, 10);
Number.parseInt("-", 10);
NaN;
Number.parseInt("", 10);
NaN;
Number.parseInt("-0", 10);
-0;
Number.parseInt("+12345", 10);
12345;
Number.parseInt(" +12345", 10);
12345;
Number.parseInt("-12345", 10);
-12345;
Number.parseInt(" -12345", 10);
-12345;

/*
 * 6.  Let R = ToInt32(radix).
 */
upvar = "";
str = {
  toString: function () {
    if (!upvar) {
      upvar = "string";
    }

    return "42";
  }
};
radix = {
  toString: function () {
    if (!upvar) {
      upvar = "radix";
    }

    return "10";
  }
};
Number.parseInt(str, radix);
42;
upvar;
"string";
Number.parseInt("123", null);
123;
Number.parseInt("123", undefined);
123;
Number.parseInt("123", NaN);
123;
Number.parseInt("123", -0);
123;
Number.parseInt("10", 72057594037927950);
16;
Number.parseInt("10", -4294967292);
4;
Number.parseInt("0x10", 1e308);
16;
Number.parseInt("10", 1e308);
10;
Number.parseInt("10", {
  valueOf: function () {
    return 16;
  }
});
16;

/*
 * 7.  Let stripPrefix be true.
 * 8.  If R ≠ 0, then
 *     a. If R < 2 or R > 36, then return NaN.
 *     b. If R ≠ 16, let stripPrefix be false.
 * 9.  Else, R = 0
 *     a. Let R = 10.
 * 10. If stripPrefix is true, then
 *     a. If the length of S is at least 2 and the first two characters of S
 *     are either “0x” or “0X”, then remove the first two characters from S and
 *     let R = 16.
 */
var vs = ["1", "51", "917", "2343", "99963"];

for (var i = 0, sz = vs.length; i < sz; i++) {
  Number.parseInt(vs[i], 0);
  Number.parseInt(vs[i], 10);
  "bad " + vs[i];
}

Number.parseInt("0x10");
16;
Number.parseInt("0x10", 0);
16;
Number.parseInt("0x10", 16);
16;
Number.parseInt("0x10", 8);
0;
Number.parseInt("-0x10", 16);
-16;
Number.parseInt("5", 1);
NaN;
Number.parseInt("5", 37);
NaN;
Number.parseInt("5", {
  valueOf: function () {
    return -1;
  }
});
NaN;
Number.parseInt("");
NaN;
Number.parseInt("ohai");
NaN;
Number.parseInt("0xohai");
NaN;
Number.parseInt("-ohai");
NaN;
Number.parseInt("+ohai");
NaN;
Number.parseInt(" ohai");
NaN;
Number.parseInt("0xaohai");
10;
Number.parseInt("hohai", 18);
17;
Number.parseInt("ohai", 36);
1142154;
Number.parseInt("0ohai", 36);
1142154;
Number.parseInt("00ohai", 36);
1142154;
Number.parseInt("A", 16);
10;
Number.parseInt("0A", 16);
10;
Number.parseInt("00A", 16);
10;
Number.parseInt("A", 17);
10;
Number.parseInt("0A", 17);
10;
Number.parseInt("00A", 17);
10;
Number.parseInt();
parseInt;

/******************************************************************************/
if (typeof reportCompare === "function") {
  reportCompare(true, true);
}

print("All tests passed!");
