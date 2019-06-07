'''Use nearest neighbors to estimate the gradient of df.

Notes
-----
Assuming that off-resonance varies smoothly pixel-to-pixel, rf phase
varies smoothly pixel-to-pixel, and that we can segment out similar
tissue, then each nieghboring ellipse should arise from about the same
underlying ellipse, i.e., the tissue properties that define the shape
of the ellipses will be similar.  If we don't expect off-resonance
to vary smoothly, then some other scheme will be required to group
phase-cycle points along the ellipse from adjacent ellipses.

Since we only have 4 points, we cannot specify the ellipse.  But, if
df and rf phase change only a little bit pixel to pixel, then we can
align the ellipses of neighboring pixels and ``fill in'' more points
on the ellipse since df will change where the underlying ellipse was
sampled.  We are effectively using the neighboring ellipses' points to
fully specify our own ellipse.  Now that we have a fully specified
ellipse, we can use a method such as PLANET to get back the
parameters we desire (T1, T2, M0, df, RF phase).

We can actually do something even more interesting, I think...
The rotation required to rotate an ellipse to its neighbor is the
change in off-resonance from the home pixel to the neighboring pixel.
So if we do this for all pixels and their nearest neighbors, we get
4 off-resonance gradient estimates: along each axis and the flipped
version.

If we assume that isocenter has df=0, then we can use a cummulative
sum outward from the isocenter to get off-resonance estimates for
each of our off-resonance gradient estimates (plus some constant --
what it actually was at the isocenter).  We can use this in
conjunction with PLANET to increase the SNR of our resultant
off-resonance maps.
'''
