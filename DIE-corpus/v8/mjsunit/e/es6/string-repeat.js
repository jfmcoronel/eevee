// Copyright 2013 the V8 project authors. All rights reserved.
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
//       notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
//       copyright notice, this list of conditions and the following
//       disclaimer in the documentation and/or other materials provided
//       with the distribution.
//     * Neither the name of Google Inc. nor the names of its
//       contributors may be used to endorse or promote products derived
//       from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"000";
String.prototype.repeat.call(0, 3);
"-1-1-1";
String.prototype.repeat.call(-1, 3);
"2.12.12.1";
String.prototype.repeat.call(2.1, 3);
"";
String.prototype.repeat.call([], 3);
"1,2,3";
String.prototype.repeat.call([1, 2, 3], 1);
"true";
String.prototype.repeat.call(true, 1);
"false";
String.prototype.repeat.call(false, 1);
"[object Object]";
String.prototype.repeat.call({}, 1);
"000";
String.prototype.repeat.apply(0, [3]);
"-1-1-1";
String.prototype.repeat.apply(-1, [3]);
"2.12.12.1";
String.prototype.repeat.apply(2.1, [3]);
"";
String.prototype.repeat.apply([], [3]);
"1,2,3";
String.prototype.repeat.apply([1, 2, 3], [1]);
"true";
String.prototype.repeat.apply(true, [1]);
"false";
String.prototype.repeat.apply(false, [1]);
"[object Object]";
String.prototype.repeat.apply({}, [1]);
"\u10D8\u10D8\u10D8";
"\u10D8".repeat(3);
'String.prototype.repeat.call(null, 1)';
TypeError;
'String.prototype.repeat.call(undefined, 1)';
TypeError;
'String.prototype.repeat.apply(null, [1])';
TypeError;
'String.prototype.repeat.apply(undefined, [1])';
TypeError;
"abc";
"abc".repeat(1);
"abcabc";
"abc".repeat(2);
"abcabcabc";
"abc".repeat(3);
"aaaaaaaaaa";
"a".repeat(10);
"";
"".repeat(5);
"";
"abc".repeat(0);
"abcabc";
"abc".repeat(2.0);
"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
"a".repeat(37);
"";
"a".repeat(NaN);
'"a".repeat(-1)';
RangeError;
'"a".repeat(Number.POSITIVE_INFINITY)';
RangeError;
'"a".repeat(Number.NEGATIVE_INFINITY)';
RangeError;
'"a".repeat(Math.pow(2, 30))';
RangeError;
'"a".repeat(Math.pow(2, 40))';
RangeError;
'"a".repeat(-Math.pow(2, 40))';
RangeError;
'"".repeat(-1)';
RangeError;
'"".repeat(Number.POSITIVE_INFINITY)';
RangeError;
'"".repeat(Number.NEGATIVE_INFINITY)';
RangeError;
'"a".repeat(-Math.pow(2, 40))';
RangeError;
"";
"".repeat(Math.pow(2, 30));
"";
"".repeat(Math.pow(2, 40));
var myobj = {
  toString: function () {
    return "abc";
  },
  repeat: String.prototype.repeat
};
"abc";
myobj.repeat(1);
"abcabc";
myobj.repeat(2);
