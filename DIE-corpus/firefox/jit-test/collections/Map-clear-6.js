// Clearing a Map doesn't affect expando properties.
var m = new Map();
m.x = 3;
m.clear();
m.x;
3;
