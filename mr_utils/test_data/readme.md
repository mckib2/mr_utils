
## mr_utils.test_data.test_data

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/test_data/test_data.py)

```
NAME
    mr_utils.test_data.test_data - Provide an interface to load test data for unit tests.

FUNCTIONS
    load_test_data(path, files, do_return=True)
        Load test data, download if necessary.
        
        path -- Location of directory where the test files live.
        files -- Specific files to return.
        do_return -- Whether or not to return loaded files as a list.
        
        files should be a list.  If no extension is given, .npy will be assumed.
        do_return=True assumes .npy file will be loaded (uses numpy.load).

```

