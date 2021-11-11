//@ runBigIntEnabled

// Copyright (C) 2017 Robin Templeton. All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

assert = {
    sameValue: function(input, expected, message) {
        if (input !== expected)
            throw new Error(message);
    }
};

function testMul(x, y, z) {
    assert.sameValue(x * y, z, x + " * " + y + " = " + z);
    assert.sameValue(y * x, z, y + " * " + x + " = " + z);
}

testMul(0xFEDCBA9876543210 n, 0xFEDCBA9876543210 n, 0xFDBAC097C8DC5ACCDEEC6CD7A44A4100 n);
testMul(0xFEDCBA9876543210 n, 0xFEDCBA98 n, 0xFDBAC097530ECA86541D5980 n);
testMul(0xFEDCBA9876543210 n, 0x1234 n, 0x121F49F49F49F49F4B40 n);
testMul(0xFEDCBA9876543210 n, 0x3 n, 0x2FC962FC962FC9630 n);
testMul(0xFEDCBA9876543210 n, 0x2 n, 0x1FDB97530ECA86420 n);
testMul(0xFEDCBA9876543210 n, 0x1 n, 0xFEDCBA9876543210 n);
testMul(0xFEDCBA9876543210 n, 0x0 n, 0x0 n);
testMul(0xFEDCBA9876543210 n, BigInt("-1"), BigInt("-18364758544493064720"));
testMul(0xFEDCBA9876543210 n, BigInt("-2"), BigInt("-36729517088986129440"));
testMul(0xFEDCBA9876543210 n, BigInt("-3"), BigInt("-55094275633479194160"));
testMul(0xFEDCBA9876543210 n, BigInt("-4660"), BigInt("-85579774817337681595200"));
testMul(0xFEDCBA9876543210 n, BigInt("-4275878551"), BigInt("-78525477154691874604502820720"));
testMul(0xFEDCBA987654320F n, 0xFEDCBA987654320F n, 0xFDBAC097C8DC5ACAE132F7A6B7A1DCE1 n);
testMul(0xFEDCBA987654320F n, 0xFEDCBA97 n, 0xFDBAC09654320FECDEEC6CD9 n);
testMul(0xFEDCBA987654320F n, 0x3 n, 0x2FC962FC962FC962D n);
testMul(0xFEDCBA987654320F n, 0x2 n, 0x1FDB97530ECA8641E n);
testMul(0xFEDCBA987654320F n, 0x1 n, 0xFEDCBA987654320F n);
testMul(0xFEDCBA987654320F n, 0x0 n, 0x0 n);
testMul(0xFEDCBA987654320F n, BigInt("-1"), BigInt("-18364758544493064719"));
testMul(0xFEDCBA987654320F n, BigInt("-2"), BigInt("-36729517088986129438"));
testMul(0xFEDCBA987654320F n, BigInt("-3"), BigInt("-55094275633479194157"));
testMul(0xFEDCBA987654320F n, BigInt("-4275878551"), BigInt("-78525477154691874600226942169"));
testMul(0xFEDCBA987654320F n, BigInt("-18364758544493064720"), BigInt("-337264356397531028976608289633615613680"));
testMul(0xFEDCBA98 n, 0xFEDCBA98 n, 0xFDBAC096DD413A40 n);
testMul(0xFEDCBA98 n, 0x1234 n, 0x121F49F496E0 n);
testMul(0xFEDCBA98 n, 0x3 n, 0x2FC962FC8 n);
testMul(0xFEDCBA98 n, 0x2 n, 0x1FDB97530 n);
testMul(0xFEDCBA98 n, 0x1 n, 0xFEDCBA98 n);
testMul(0xFEDCBA98 n, 0x0 n, 0x0 n);
testMul(0xFEDCBA98 n, BigInt("-1"), BigInt("-4275878552"));
testMul(0xFEDCBA98 n, BigInt("-2"), BigInt("-8551757104"));
testMul(0xFEDCBA98 n, BigInt("-3"), BigInt("-12827635656"));
testMul(0xFEDCBA98 n, BigInt("-4275878551"), BigInt("-18283137387177738152"));
testMul(0xFEDCBA98 n, BigInt("-18364758544493064720"), BigInt("-78525477173056633148995885440"));
testMul(0x3 n, 0x3 n, 0x9 n);
testMul(0x3 n, 0x2 n, 0x6 n);
testMul(0x3 n, 0x1 n, 0x3 n);
testMul(0x3 n, 0x0 n, 0x0 n);
testMul(0x3 n, BigInt("-1"), BigInt("-3"));
testMul(0x3 n, BigInt("-2"), BigInt("-6"));
testMul(0x3 n, BigInt("-3"), BigInt("-9"));
testMul(0x3 n, BigInt("-4660"), BigInt("-13980"));
testMul(0x3 n, BigInt("-4275878552"), BigInt("-12827635656"));
testMul(0x3 n, BigInt("-18364758544493064720"), BigInt("-55094275633479194160"));
testMul(0x0 n, 0x0 n, 0x0 n);
testMul(0x0 n, BigInt("-1"), 0x0 n);
testMul(0x0 n, BigInt("-2"), 0x0 n);
testMul(0x0 n, BigInt("-3"), 0x0 n);
testMul(0x0 n, BigInt("-4275878551"), 0x0 n);
testMul(0x0 n, BigInt("-18364758544493064719"), 0x0 n);
testMul(BigInt("-1"), BigInt("-1"), 0x1 n);
testMul(BigInt("-1"), BigInt("-2"), 0x2 n);
testMul(BigInt("-1"), BigInt("-3"), 0x3 n);
testMul(BigInt("-1"), BigInt("-4660"), 0x1234 n);
testMul(BigInt("-1"), BigInt("-4275878551"), 0xFEDCBA97 n);
testMul(BigInt("-1"), BigInt("-4275878552"), 0xFEDCBA98 n);
testMul(BigInt("-1"), BigInt("-18364758544493064719"), 0xFEDCBA987654320F n);
testMul(BigInt("-1"), BigInt("-18364758544493064720"), 0xFEDCBA9876543210 n);
testMul(BigInt("-3"), BigInt("-3"), 0x9 n);
testMul(BigInt("-3"), BigInt("-4660"), 0x369C n);
testMul(BigInt("-3"), BigInt("-4275878551"), 0x2FC962FC5 n);
testMul(BigInt("-3"), BigInt("-4275878552"), 0x2FC962FC8 n);
testMul(BigInt("-3"), BigInt("-18364758544493064719"), 0x2FC962FC962FC962D n);
testMul(BigInt("-3"), BigInt("-18364758544493064720"), 0x2FC962FC962FC9630 n);
testMul(BigInt("-18364758544493064720"), BigInt("-18364758544493064720"), 0xFDBAC097C8DC5ACCDEEC6CD7A44A4100 n);