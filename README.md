# VirtualMicroscopy
Tool to visualize particle simulations like a microscope


Input file is a .lammpstrj in the following form:


ITEM: TIMESTEP

0

ITEM: NUMBER OF ATOMS

38033

ITEM: BOX BOUNDS

-5000 5000

-5000 5000

-5000 5000

ITEM: ATOMS id type xs ys zs

1 1 0.771711 0.809357 0.325273

2 1 0.599459 0.277628 0.90704

3 1 0.938981 0.746498 0.873663

.

.

.

ITEM: TIMESTEP

1

ITEM: NUMBER OF ATOMS

38033

ITEM: BOX BOUNDS

-5000 5000

-5000 5000

-5000 5000

ITEM: ATOMS id type xs ys zs

1 1 0.771711 0.809357 0.325273

2 1 0.599459 0.277628 0.90704

3 1 0.938981 0.746498 0.873663

.

.

.

Path has to be specified in the file.
