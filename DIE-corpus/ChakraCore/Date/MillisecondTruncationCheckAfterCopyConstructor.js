//-------------------------------------------------------------------------------------------------------
// Copyright (C) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE.txt file in the project root for full license information.
//-------------------------------------------------------------------------------------------------------
var a = new Date(Date.now());
a.setMilliseconds(491);
var b = new Date(a);
print("Date A: ", a.getMilliseconds());
print("Date B: ", b.getMilliseconds());
