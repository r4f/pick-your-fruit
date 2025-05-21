/*
Note, that not all matches are edible fruit trees. E.g., Castanea (Chestnut), as well as cherry cherry species are not all enjoyable to eat.

The property query and the bounding region are still subject to change and fine-tuning.
*/
[out:json];
node(around:15000,49.7796256, 9.9947906)[natural=tree]->.all;
(
  node.all[genus=Malus];
  node.all[species~"^Malus"];
  node.all[genus=Tilia];
  node.all[species~"^Tilia"];
  node.all[genus=Prunus];
  node.all[species~"^Prun"];
  node.all[genus=Pyrus];
  node.all[species~"^Pyrus"];
  node.all[genus=Ficus];
  node.all[species~"^Ficus"];
  node.all[genus=Juglans];
  node.all[species~"^Juglans"];
  node.all[genus=Sambucus];
  node.all[species~"^Sambucus"];
  node.all[genus=Castanea];
  node.all[species~"^Castanea"];
);
out;
