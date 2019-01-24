# Baking-Namepair-Creator
This addon set's a namepair (for example: "body_low" and "body_high"), to use with baking software, like Substance Painter/Designer, with one click.

To use:
Select the low poly and high poly objects, and press the Create Baking Namepair button in the Relations tab. The suffixes _high and _low are added automatically based on the vertex count. The name of the low poly object is used as the new name's base.

The addon will display an error message if it finds any problems.

in 2.8 extra options can be found in the "N"-panel:
https://i.imgur.com/rzKjPj1.jpg
In 2.79 they are in the tools panel.

When Generate Random Name option is on, the objects will get a new random name, for instance: SVDDSFD_low and SVDDSFD_high. This is great if your object's names are long or weird and cause trouble in your baking software. For instance, I found a name like "Mesh.1862_low.018_low" was causing trouble in SP.

Hide After Renaming is great to create namepairs for lots of objects - just set them up until everything is hidden, and then unhide all. This way you won't miss any object pairs.

Also Rename Datablock will also rename the mesh data.

In 2.8 there are extra options:
There are also buttons that allow to batch-show/batch-hide all of the renamed objects by groups: only-high/only-low/all renamed.
