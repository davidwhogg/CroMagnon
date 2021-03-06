# CroMagnon
*Oh no, yet another attempt at Cryo-EM and CET data analysis.*

## authors
- David W. Hogg (NYU)

## license
Copyright 2015 the authors.
**CroMagnon** is open-source software licensed under the *MIT License*.
See the file `LICENSE` for details.

## dependencies
- In the `data` subdirectory there is another `README.md` file that contains
notes about what data sets we will start with.
- We will probably need to use
[EMAN2](http://blake.bcm.edu/emanwiki/EMAN2) to read the image data files.
(Yes, they invented a new image format.)

## never-asked questions
- *Why are we doing this?*
In large part because Leslie Greengard (NYU) and the authors noted that there
is a possible relationship between Cryo-EM and certain kinds of astronomical
deprojection problems.
- *Can we apply this to astronomical data?*
Yes, we certainly hope so.  Cryo-EM for galaxies!
- *Should we take [this Coursera course](https://www.coursera.org/learn/cryo-em)?*
The MOOC is a fraud!  But we might benefit from the overview.
- *In what sense is this "tomography"?*
In our view, *tomography* is the construction of a function from a good set
of projections.
That is not the view of all people who think about these things.
