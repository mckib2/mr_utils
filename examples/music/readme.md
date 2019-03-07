
# MUSIC
## examples.music.compression

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/music/compression.py)

```
NAME
    examples.music.compression - Fun little experiment for audio compression.

DESCRIPTION
    The idea is to use our reordering trick for sparse signals and apply it to
    audio waveforms.  The new thing we're doing here is using permutation ranks
    to be a sort of "key" that we can look the permutation up with.  The reason
    we might want to use permutation rank instead of the permutation is because
    it takes less storage -- instead of storing an integer for every sample of the
    waveform, store an (potentially quite large but not as large as storing an
    integer for every waveform) integer representing the permutation.  This means
    we get some compression out of the deal, since we could transmit less and
    still get the same audio quality.
    
    The sad part is that permutation ranking and unranking goes by the factorial
    of the length of the permutation -- even for the most efficient algorithms. So
    we're restricted to very short block lengths over which to reorder, and it
    might not be worth it for all the trouble we had to go through to ge the
    ranks in the first place and the space we need to now take up storing many
    incredibly large integers.
    
    Maybe an idea to piggyback on other forms of compression?
    
    Notes:
        Finite differences (when you start dropping a lot of smaller coefficients)
        gets square-wave-like with very noticable artifacts.  Perhaps low-pass
        filtering might help?
    
        DCT seems to be very robust and does a great job, even when block lengths
        are small (chunk_size=16).
    
        I've only tried db1 wavelets, don't work as well as DCT.


```

