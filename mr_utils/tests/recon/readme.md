
## mr_utils.tests.recon.test_grappa

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/recon/test_grappa.py)

```
NAME
    mr_utils.tests.recon.test_grappa - Test module for simple GRAPPA implementation.

CLASSES
    unittest.case.TestCase(builtins.object)
        GRAPPAUnitTest
    
    class GRAPPAUnitTest(unittest.case.TestCase)
     |  A class whose instances are single test cases.
     |  
     |  By default, the test code itself should be placed in a method named
     |  'runTest'.
     |  
     |  If the fixture may be used for many test cases, create as
     |  many test methods as are needed. When instantiating such a TestCase
     |  subclass, specify in the constructor arguments the name of the test method
     |  that the instance is to execute.
     |  
     |  Test authors should subclass TestCase for their own tests. Construction
     |  and deconstruction of the test's environment ('fixture') can be
     |  implemented by overriding the 'setUp' and 'tearDown' methods respectively.
     |  
     |  If it is necessary to override the __init__ method, the base class
     |  __init__ method must always be called. It is important that subclasses
     |  should not change the signature of their __init__ method, since instances
     |  of the classes are instantiated automatically by parts of the framework
     |  in order to be run.
     |  
     |  When subclassing TestCase, you can set these attributes:
     |  * failureException: determines which exception will be raised when
     |      the instance's assertion methods fail; test methods raising this
     |      exception will be deemed to have 'failed' rather than 'errored'.
     |  * longMessage: determines whether long messages (including repr of
     |      objects used in assert methods) will be printed on failure in *addition*
     |      to any explicit message passed.
     |  * maxDiff: sets the maximum length of a diff in failure messages
     |      by assert methods using difflib. It is looked up as an instance
     |      attribute so can be configured by individual tests if required.
     |  
     |  Method resolution order:
     |      GRAPPAUnitTest
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_grappa2d(self)
     |      Do simple 2d recon.
     |  
     |  test_recon(self)
     |      Replicate MATLAB results.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from unittest.case.TestCase:
     |  
     |  __call__(self, *args, **kwds)
     |      Call self as a function.
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, methodName='runTest')
     |      Create an instance of the class that will use the named test
     |      method when executed. Raises a ValueError if the instance does
     |      not have a method with the specified name.
     |  
     |  __repr__(self)
     |      Return repr(self).
     |  
     |  __str__(self)
     |      Return str(self).
     |  
     |  addCleanup(self, function, *args, **kwargs)
     |      Add a function, with arguments, to be called when the test is
     |      completed. Functions added are called on a LIFO basis and are
     |      called after tearDown on test failure or success.
     |      
     |      Cleanup items are called even if setUp fails (unlike tearDown).
     |  
     |  addTypeEqualityFunc(self, typeobj, function)
     |      Add a type specific assertEqual style function to compare a type.
     |      
     |      This method is for use by TestCase subclasses that need to register
     |      their own type equality functions to provide nicer error messages.
     |      
     |      Args:
     |          typeobj: The data type to call this function on when both values
     |                  are of the same type in assertEqual().
     |          function: The callable taking two arguments and an optional
     |                  msg= argument that raises self.failureException with a
     |                  useful error message when the two arguments are not equal.
     |  
     |  assertAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are unequal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is more than the given
     |      delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      If the two objects compare equal then they will automatically
     |      compare almost equal.
     |  
     |  assertAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertCountEqual(self, first, second, msg=None)
     |      An unordered sequence comparison asserting that the same elements,
     |      regardless of order.  If the same element occurs more than once,
     |      it verifies that the elements occur the same number of times.
     |      
     |          self.assertEqual(Counter(list(first)),
     |                           Counter(list(second)))
     |      
     |       Example:
     |          - [0, 1, 1] and [1, 0, 1] compare equal.
     |          - [0, 0, 1] and [0, 1] compare unequal.
     |  
     |  assertDictContainsSubset(self, subset, dictionary, msg=None)
     |      Checks whether dictionary is a superset of subset.
     |  
     |  assertDictEqual(self, d1, d2, msg=None)
     |  
     |  assertEqual(self, first, second, msg=None)
     |      Fail if the two objects are unequal as determined by the '=='
     |      operator.
     |  
     |  assertEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertFalse(self, expr, msg=None)
     |      Check that the expression is false.
     |  
     |  assertGreater(self, a, b, msg=None)
     |      Just like self.assertTrue(a > b), but with a nicer default message.
     |  
     |  assertGreaterEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a >= b), but with a nicer default message.
     |  
     |  assertIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a in b), but with a nicer default message.
     |  
     |  assertIs(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is b), but with a nicer default message.
     |  
     |  assertIsInstance(self, obj, cls, msg=None)
     |      Same as self.assertTrue(isinstance(obj, cls)), with a nicer
     |      default message.
     |  
     |  assertIsNone(self, obj, msg=None)
     |      Same as self.assertTrue(obj is None), with a nicer default message.
     |  
     |  assertIsNot(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is not b), but with a nicer default message.
     |  
     |  assertIsNotNone(self, obj, msg=None)
     |      Included for symmetry with assertIsNone.
     |  
     |  assertLess(self, a, b, msg=None)
     |      Just like self.assertTrue(a < b), but with a nicer default message.
     |  
     |  assertLessEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a <= b), but with a nicer default message.
     |  
     |  assertListEqual(self, list1, list2, msg=None)
     |      A list-specific equality assertion.
     |      
     |      Args:
     |          list1: The first list to compare.
     |          list2: The second list to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertLogs(self, logger=None, level=None)
     |      Fail unless a log message of level *level* or higher is emitted
     |      on *logger_name* or its children.  If omitted, *level* defaults to
     |      INFO and *logger* defaults to the root logger.
     |      
     |      This method must be used as a context manager, and will yield
     |      a recording object with two attributes: `output` and `records`.
     |      At the end of the context manager, the `output` attribute will
     |      be a list of the matching formatted log messages and the
     |      `records` attribute will be a list of the corresponding LogRecord
     |      objects.
     |      
     |      Example::
     |      
     |          with self.assertLogs('foo', level='INFO') as cm:
     |              logging.getLogger('foo').info('first message')
     |              logging.getLogger('foo.bar').error('second message')
     |          self.assertEqual(cm.output, ['INFO:foo:first message',
     |                                       'ERROR:foo.bar:second message'])
     |  
     |  assertMultiLineEqual(self, first, second, msg=None)
     |      Assert that two multi-line strings are equal.
     |  
     |  assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are equal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is less than the given delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      Objects that are equal automatically fail.
     |  
     |  assertNotAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotEqual(self, first, second, msg=None)
     |      Fail if the two objects are equal as determined by the '!='
     |      operator.
     |  
     |  assertNotEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a not in b), but with a nicer default message.
     |  
     |  assertNotIsInstance(self, obj, cls, msg=None)
     |      Included for symmetry with assertIsInstance.
     |  
     |  assertNotRegex(self, text, unexpected_regex, msg=None)
     |      Fail the test if the text matches the regular expression.
     |  
     |  assertNotRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertRaises(self, expected_exception, *args, **kwargs)
     |      Fail unless an exception of class expected_exception is raised
     |      by the callable when invoked with specified positional and
     |      keyword arguments. If a different type of exception is
     |      raised, it will not be caught, and the test case will be
     |      deemed to have suffered an error, exactly as for an
     |      unexpected exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertRaises(SomeException):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertRaises
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the exception as
     |      the 'exception' attribute. This allows you to inspect the
     |      exception after the assertion::
     |      
     |          with self.assertRaises(SomeException) as cm:
     |              do_something()
     |          the_exception = cm.exception
     |          self.assertEqual(the_exception.error_code, 3)
     |  
     |  assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs)
     |      Asserts that the message in a raised exception matches a regex.
     |      
     |      Args:
     |          expected_exception: Exception class expected to be raised.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertRaisesRegex is used as a context manager.
     |  
     |  assertRaisesRegexp = deprecated_func(*args, **kwargs)
     |  
     |  assertRegex(self, text, expected_regex, msg=None)
     |      Fail the test unless the text matches the regular expression.
     |  
     |  assertRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None)
     |      An equality assertion for ordered sequences (like lists and tuples).
     |      
     |      For the purposes of this function, a valid ordered sequence type is one
     |      which can be indexed, has a length, and has an equality operator.
     |      
     |      Args:
     |          seq1: The first sequence to compare.
     |          seq2: The second sequence to compare.
     |          seq_type: The expected datatype of the sequences, or None if no
     |                  datatype should be enforced.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertSetEqual(self, set1, set2, msg=None)
     |      A set-specific equality assertion.
     |      
     |      Args:
     |          set1: The first set to compare.
     |          set2: The second set to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |      
     |      assertSetEqual uses ducktyping to support different types of sets, and
     |      is optimized for sets specifically (parameters must support a
     |      difference method).
     |  
     |  assertTrue(self, expr, msg=None)
     |      Check that the expression is true.
     |  
     |  assertTupleEqual(self, tuple1, tuple2, msg=None)
     |      A tuple-specific equality assertion.
     |      
     |      Args:
     |          tuple1: The first tuple to compare.
     |          tuple2: The second tuple to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertWarns(self, expected_warning, *args, **kwargs)
     |      Fail unless a warning of class warnClass is triggered
     |      by the callable when invoked with specified positional and
     |      keyword arguments.  If a different type of warning is
     |      triggered, it will not be handled: depending on the other
     |      warning filtering rules in effect, it might be silenced, printed
     |      out, or raised as an exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertWarns(SomeWarning):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertWarns
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the first matching
     |      warning as the 'warning' attribute; similarly, the 'filename'
     |      and 'lineno' attributes give you information about the line
     |      of Python code from which the warning was triggered.
     |      This allows you to inspect the warning after the assertion::
     |      
     |          with self.assertWarns(SomeWarning) as cm:
     |              do_something()
     |          the_warning = cm.warning
     |          self.assertEqual(the_warning.some_attribute, 147)
     |  
     |  assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs)
     |      Asserts that the message in a triggered warning matches a regexp.
     |      Basic functioning is similar to assertWarns() with the addition
     |      that only warnings whose messages also match the regular expression
     |      are considered successful matches.
     |      
     |      Args:
     |          expected_warning: Warning class expected to be triggered.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertWarnsRegex is used as a context manager.
     |  
     |  assert_ = deprecated_func(*args, **kwargs)
     |  
     |  countTestCases(self)
     |  
     |  debug(self)
     |      Run the test without collecting errors in a TestResult
     |  
     |  defaultTestResult(self)
     |  
     |  doCleanups(self)
     |      Execute all cleanup functions. Normally called for you after
     |      tearDown.
     |  
     |  fail(self, msg=None)
     |      Fail immediately, with the given message.
     |  
     |  failIf = deprecated_func(*args, **kwargs)
     |  
     |  failIfAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failIfEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnless = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessRaises = deprecated_func(*args, **kwargs)
     |  
     |  id(self)
     |  
     |  run(self, result=None)
     |  
     |  shortDescription(self)
     |      Returns a one-line description of the test, or None if no
     |      description has been provided.
     |      
     |      The default implementation of this method returns the first line of
     |      the specified test method's docstring.
     |  
     |  skipTest(self, reason)
     |      Skip this test.
     |  
     |  subTest(self, msg=<object object at 0x7f267fce1280>, **params)
     |      Return a context manager that will return the enclosed block
     |      of code in a subtest identified by the optional message and
     |      keyword parameters.  A failure in the subtest marks the test
     |      case as failed but resumes execution at the end of the enclosed
     |      block, allowing further test code to be executed.
     |  
     |  tearDown(self)
     |      Hook method for deconstructing the test fixture after testing it.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from unittest.case.TestCase:
     |  
     |  setUpClass() from builtins.type
     |      Hook method for setting up class fixture before running tests in the class.
     |  
     |  tearDownClass() from builtins.type
     |      Hook method for deconstructing the class fixture after running all tests in the class.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from unittest.case.TestCase:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from unittest.case.TestCase:
     |  
     |  failureException = <class 'AssertionError'>
     |      Assertion failed.
     |  
     |  longMessage = True
     |  
     |  maxDiff = 640


```


## mr_utils.tests.recon.test_gs_recon

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/recon/test_gs_recon.py)

```
NAME
    mr_utils.tests.recon.test_gs_recon - Verification, validation of geometric solution to elliptical signal model.

DESCRIPTION
    Test solution against naive loop implementation, Hoff's MATLAB implementation,
    and Taylor's MATLAB implementation.

CLASSES
    unittest.case.TestCase(builtins.object)
        GSReconKneeData
        GSReconTestCase
    
    class GSReconKneeData(unittest.case.TestCase)
     |  Make sure our implementation matches output of Taylor knee recon.
     |  
     |  Method resolution order:
     |      GSReconKneeData
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_complex_sum(self)
     |      Verify complex sum is the same as Taylor's implementation.
     |  
     |  test_direct_solution(self)
     |      Make sure first pass solution is the same as Taylor's.
     |  
     |  test_gs_recon_knee(self)
     |      Verify the final solution matches Taylor's solution.
     |  
     |  test_max_magnitudes(self)
     |      Make sure max magnitues are the same as Taylor's implementation.
     |  
     |  test_weighted_combination(self)
     |      Make sure second pass solution is the same as Taylor's.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from unittest.case.TestCase:
     |  
     |  __call__(self, *args, **kwds)
     |      Call self as a function.
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, methodName='runTest')
     |      Create an instance of the class that will use the named test
     |      method when executed. Raises a ValueError if the instance does
     |      not have a method with the specified name.
     |  
     |  __repr__(self)
     |      Return repr(self).
     |  
     |  __str__(self)
     |      Return str(self).
     |  
     |  addCleanup(self, function, *args, **kwargs)
     |      Add a function, with arguments, to be called when the test is
     |      completed. Functions added are called on a LIFO basis and are
     |      called after tearDown on test failure or success.
     |      
     |      Cleanup items are called even if setUp fails (unlike tearDown).
     |  
     |  addTypeEqualityFunc(self, typeobj, function)
     |      Add a type specific assertEqual style function to compare a type.
     |      
     |      This method is for use by TestCase subclasses that need to register
     |      their own type equality functions to provide nicer error messages.
     |      
     |      Args:
     |          typeobj: The data type to call this function on when both values
     |                  are of the same type in assertEqual().
     |          function: The callable taking two arguments and an optional
     |                  msg= argument that raises self.failureException with a
     |                  useful error message when the two arguments are not equal.
     |  
     |  assertAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are unequal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is more than the given
     |      delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      If the two objects compare equal then they will automatically
     |      compare almost equal.
     |  
     |  assertAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertCountEqual(self, first, second, msg=None)
     |      An unordered sequence comparison asserting that the same elements,
     |      regardless of order.  If the same element occurs more than once,
     |      it verifies that the elements occur the same number of times.
     |      
     |          self.assertEqual(Counter(list(first)),
     |                           Counter(list(second)))
     |      
     |       Example:
     |          - [0, 1, 1] and [1, 0, 1] compare equal.
     |          - [0, 0, 1] and [0, 1] compare unequal.
     |  
     |  assertDictContainsSubset(self, subset, dictionary, msg=None)
     |      Checks whether dictionary is a superset of subset.
     |  
     |  assertDictEqual(self, d1, d2, msg=None)
     |  
     |  assertEqual(self, first, second, msg=None)
     |      Fail if the two objects are unequal as determined by the '=='
     |      operator.
     |  
     |  assertEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertFalse(self, expr, msg=None)
     |      Check that the expression is false.
     |  
     |  assertGreater(self, a, b, msg=None)
     |      Just like self.assertTrue(a > b), but with a nicer default message.
     |  
     |  assertGreaterEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a >= b), but with a nicer default message.
     |  
     |  assertIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a in b), but with a nicer default message.
     |  
     |  assertIs(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is b), but with a nicer default message.
     |  
     |  assertIsInstance(self, obj, cls, msg=None)
     |      Same as self.assertTrue(isinstance(obj, cls)), with a nicer
     |      default message.
     |  
     |  assertIsNone(self, obj, msg=None)
     |      Same as self.assertTrue(obj is None), with a nicer default message.
     |  
     |  assertIsNot(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is not b), but with a nicer default message.
     |  
     |  assertIsNotNone(self, obj, msg=None)
     |      Included for symmetry with assertIsNone.
     |  
     |  assertLess(self, a, b, msg=None)
     |      Just like self.assertTrue(a < b), but with a nicer default message.
     |  
     |  assertLessEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a <= b), but with a nicer default message.
     |  
     |  assertListEqual(self, list1, list2, msg=None)
     |      A list-specific equality assertion.
     |      
     |      Args:
     |          list1: The first list to compare.
     |          list2: The second list to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertLogs(self, logger=None, level=None)
     |      Fail unless a log message of level *level* or higher is emitted
     |      on *logger_name* or its children.  If omitted, *level* defaults to
     |      INFO and *logger* defaults to the root logger.
     |      
     |      This method must be used as a context manager, and will yield
     |      a recording object with two attributes: `output` and `records`.
     |      At the end of the context manager, the `output` attribute will
     |      be a list of the matching formatted log messages and the
     |      `records` attribute will be a list of the corresponding LogRecord
     |      objects.
     |      
     |      Example::
     |      
     |          with self.assertLogs('foo', level='INFO') as cm:
     |              logging.getLogger('foo').info('first message')
     |              logging.getLogger('foo.bar').error('second message')
     |          self.assertEqual(cm.output, ['INFO:foo:first message',
     |                                       'ERROR:foo.bar:second message'])
     |  
     |  assertMultiLineEqual(self, first, second, msg=None)
     |      Assert that two multi-line strings are equal.
     |  
     |  assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are equal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is less than the given delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      Objects that are equal automatically fail.
     |  
     |  assertNotAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotEqual(self, first, second, msg=None)
     |      Fail if the two objects are equal as determined by the '!='
     |      operator.
     |  
     |  assertNotEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a not in b), but with a nicer default message.
     |  
     |  assertNotIsInstance(self, obj, cls, msg=None)
     |      Included for symmetry with assertIsInstance.
     |  
     |  assertNotRegex(self, text, unexpected_regex, msg=None)
     |      Fail the test if the text matches the regular expression.
     |  
     |  assertNotRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertRaises(self, expected_exception, *args, **kwargs)
     |      Fail unless an exception of class expected_exception is raised
     |      by the callable when invoked with specified positional and
     |      keyword arguments. If a different type of exception is
     |      raised, it will not be caught, and the test case will be
     |      deemed to have suffered an error, exactly as for an
     |      unexpected exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertRaises(SomeException):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertRaises
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the exception as
     |      the 'exception' attribute. This allows you to inspect the
     |      exception after the assertion::
     |      
     |          with self.assertRaises(SomeException) as cm:
     |              do_something()
     |          the_exception = cm.exception
     |          self.assertEqual(the_exception.error_code, 3)
     |  
     |  assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs)
     |      Asserts that the message in a raised exception matches a regex.
     |      
     |      Args:
     |          expected_exception: Exception class expected to be raised.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertRaisesRegex is used as a context manager.
     |  
     |  assertRaisesRegexp = deprecated_func(*args, **kwargs)
     |  
     |  assertRegex(self, text, expected_regex, msg=None)
     |      Fail the test unless the text matches the regular expression.
     |  
     |  assertRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None)
     |      An equality assertion for ordered sequences (like lists and tuples).
     |      
     |      For the purposes of this function, a valid ordered sequence type is one
     |      which can be indexed, has a length, and has an equality operator.
     |      
     |      Args:
     |          seq1: The first sequence to compare.
     |          seq2: The second sequence to compare.
     |          seq_type: The expected datatype of the sequences, or None if no
     |                  datatype should be enforced.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertSetEqual(self, set1, set2, msg=None)
     |      A set-specific equality assertion.
     |      
     |      Args:
     |          set1: The first set to compare.
     |          set2: The second set to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |      
     |      assertSetEqual uses ducktyping to support different types of sets, and
     |      is optimized for sets specifically (parameters must support a
     |      difference method).
     |  
     |  assertTrue(self, expr, msg=None)
     |      Check that the expression is true.
     |  
     |  assertTupleEqual(self, tuple1, tuple2, msg=None)
     |      A tuple-specific equality assertion.
     |      
     |      Args:
     |          tuple1: The first tuple to compare.
     |          tuple2: The second tuple to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertWarns(self, expected_warning, *args, **kwargs)
     |      Fail unless a warning of class warnClass is triggered
     |      by the callable when invoked with specified positional and
     |      keyword arguments.  If a different type of warning is
     |      triggered, it will not be handled: depending on the other
     |      warning filtering rules in effect, it might be silenced, printed
     |      out, or raised as an exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertWarns(SomeWarning):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertWarns
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the first matching
     |      warning as the 'warning' attribute; similarly, the 'filename'
     |      and 'lineno' attributes give you information about the line
     |      of Python code from which the warning was triggered.
     |      This allows you to inspect the warning after the assertion::
     |      
     |          with self.assertWarns(SomeWarning) as cm:
     |              do_something()
     |          the_warning = cm.warning
     |          self.assertEqual(the_warning.some_attribute, 147)
     |  
     |  assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs)
     |      Asserts that the message in a triggered warning matches a regexp.
     |      Basic functioning is similar to assertWarns() with the addition
     |      that only warnings whose messages also match the regular expression
     |      are considered successful matches.
     |      
     |      Args:
     |          expected_warning: Warning class expected to be triggered.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertWarnsRegex is used as a context manager.
     |  
     |  assert_ = deprecated_func(*args, **kwargs)
     |  
     |  countTestCases(self)
     |  
     |  debug(self)
     |      Run the test without collecting errors in a TestResult
     |  
     |  defaultTestResult(self)
     |  
     |  doCleanups(self)
     |      Execute all cleanup functions. Normally called for you after
     |      tearDown.
     |  
     |  fail(self, msg=None)
     |      Fail immediately, with the given message.
     |  
     |  failIf = deprecated_func(*args, **kwargs)
     |  
     |  failIfAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failIfEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnless = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessRaises = deprecated_func(*args, **kwargs)
     |  
     |  id(self)
     |  
     |  run(self, result=None)
     |  
     |  shortDescription(self)
     |      Returns a one-line description of the test, or None if no
     |      description has been provided.
     |      
     |      The default implementation of this method returns the first line of
     |      the specified test method's docstring.
     |  
     |  skipTest(self, reason)
     |      Skip this test.
     |  
     |  subTest(self, msg=<object object at 0x7f267fce1280>, **params)
     |      Return a context manager that will return the enclosed block
     |      of code in a subtest identified by the optional message and
     |      keyword parameters.  A failure in the subtest marks the test
     |      case as failed but resumes execution at the end of the enclosed
     |      block, allowing further test code to be executed.
     |  
     |  tearDown(self)
     |      Hook method for deconstructing the test fixture after testing it.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from unittest.case.TestCase:
     |  
     |  setUpClass() from builtins.type
     |      Hook method for setting up class fixture before running tests in the class.
     |  
     |  tearDownClass() from builtins.type
     |      Hook method for deconstructing the class fixture after running all tests in the class.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from unittest.case.TestCase:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from unittest.case.TestCase:
     |  
     |  failureException = <class 'AssertionError'>
     |      Assertion failed.
     |  
     |  longMessage = True
     |  
     |  maxDiff = 640
    
    class GSReconTestCase(unittest.case.TestCase)
     |  Verify technical implementation of algorithm.
     |  
     |  Method resolution order:
     |      GSReconTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_gs_recon(self)
     |      Test matrix implementation against naive loop implementation.
     |  
     |  test_gs_recon3d(self)
     |      Make sure 3d recon gives same answer as running 2d on all slices.
     |  
     |  test_max_magnitudes(self)
     |      Make sure we're indeed finding the maximum pixels.
     |  
     |  test_noisy_gs_recon(self)
     |      Add noise and make sure implementations are still identical.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from unittest.case.TestCase:
     |  
     |  __call__(self, *args, **kwds)
     |      Call self as a function.
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, methodName='runTest')
     |      Create an instance of the class that will use the named test
     |      method when executed. Raises a ValueError if the instance does
     |      not have a method with the specified name.
     |  
     |  __repr__(self)
     |      Return repr(self).
     |  
     |  __str__(self)
     |      Return str(self).
     |  
     |  addCleanup(self, function, *args, **kwargs)
     |      Add a function, with arguments, to be called when the test is
     |      completed. Functions added are called on a LIFO basis and are
     |      called after tearDown on test failure or success.
     |      
     |      Cleanup items are called even if setUp fails (unlike tearDown).
     |  
     |  addTypeEqualityFunc(self, typeobj, function)
     |      Add a type specific assertEqual style function to compare a type.
     |      
     |      This method is for use by TestCase subclasses that need to register
     |      their own type equality functions to provide nicer error messages.
     |      
     |      Args:
     |          typeobj: The data type to call this function on when both values
     |                  are of the same type in assertEqual().
     |          function: The callable taking two arguments and an optional
     |                  msg= argument that raises self.failureException with a
     |                  useful error message when the two arguments are not equal.
     |  
     |  assertAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are unequal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is more than the given
     |      delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      If the two objects compare equal then they will automatically
     |      compare almost equal.
     |  
     |  assertAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertCountEqual(self, first, second, msg=None)
     |      An unordered sequence comparison asserting that the same elements,
     |      regardless of order.  If the same element occurs more than once,
     |      it verifies that the elements occur the same number of times.
     |      
     |          self.assertEqual(Counter(list(first)),
     |                           Counter(list(second)))
     |      
     |       Example:
     |          - [0, 1, 1] and [1, 0, 1] compare equal.
     |          - [0, 0, 1] and [0, 1] compare unequal.
     |  
     |  assertDictContainsSubset(self, subset, dictionary, msg=None)
     |      Checks whether dictionary is a superset of subset.
     |  
     |  assertDictEqual(self, d1, d2, msg=None)
     |  
     |  assertEqual(self, first, second, msg=None)
     |      Fail if the two objects are unequal as determined by the '=='
     |      operator.
     |  
     |  assertEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertFalse(self, expr, msg=None)
     |      Check that the expression is false.
     |  
     |  assertGreater(self, a, b, msg=None)
     |      Just like self.assertTrue(a > b), but with a nicer default message.
     |  
     |  assertGreaterEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a >= b), but with a nicer default message.
     |  
     |  assertIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a in b), but with a nicer default message.
     |  
     |  assertIs(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is b), but with a nicer default message.
     |  
     |  assertIsInstance(self, obj, cls, msg=None)
     |      Same as self.assertTrue(isinstance(obj, cls)), with a nicer
     |      default message.
     |  
     |  assertIsNone(self, obj, msg=None)
     |      Same as self.assertTrue(obj is None), with a nicer default message.
     |  
     |  assertIsNot(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is not b), but with a nicer default message.
     |  
     |  assertIsNotNone(self, obj, msg=None)
     |      Included for symmetry with assertIsNone.
     |  
     |  assertLess(self, a, b, msg=None)
     |      Just like self.assertTrue(a < b), but with a nicer default message.
     |  
     |  assertLessEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a <= b), but with a nicer default message.
     |  
     |  assertListEqual(self, list1, list2, msg=None)
     |      A list-specific equality assertion.
     |      
     |      Args:
     |          list1: The first list to compare.
     |          list2: The second list to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertLogs(self, logger=None, level=None)
     |      Fail unless a log message of level *level* or higher is emitted
     |      on *logger_name* or its children.  If omitted, *level* defaults to
     |      INFO and *logger* defaults to the root logger.
     |      
     |      This method must be used as a context manager, and will yield
     |      a recording object with two attributes: `output` and `records`.
     |      At the end of the context manager, the `output` attribute will
     |      be a list of the matching formatted log messages and the
     |      `records` attribute will be a list of the corresponding LogRecord
     |      objects.
     |      
     |      Example::
     |      
     |          with self.assertLogs('foo', level='INFO') as cm:
     |              logging.getLogger('foo').info('first message')
     |              logging.getLogger('foo.bar').error('second message')
     |          self.assertEqual(cm.output, ['INFO:foo:first message',
     |                                       'ERROR:foo.bar:second message'])
     |  
     |  assertMultiLineEqual(self, first, second, msg=None)
     |      Assert that two multi-line strings are equal.
     |  
     |  assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are equal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is less than the given delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      Objects that are equal automatically fail.
     |  
     |  assertNotAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotEqual(self, first, second, msg=None)
     |      Fail if the two objects are equal as determined by the '!='
     |      operator.
     |  
     |  assertNotEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a not in b), but with a nicer default message.
     |  
     |  assertNotIsInstance(self, obj, cls, msg=None)
     |      Included for symmetry with assertIsInstance.
     |  
     |  assertNotRegex(self, text, unexpected_regex, msg=None)
     |      Fail the test if the text matches the regular expression.
     |  
     |  assertNotRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertRaises(self, expected_exception, *args, **kwargs)
     |      Fail unless an exception of class expected_exception is raised
     |      by the callable when invoked with specified positional and
     |      keyword arguments. If a different type of exception is
     |      raised, it will not be caught, and the test case will be
     |      deemed to have suffered an error, exactly as for an
     |      unexpected exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertRaises(SomeException):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertRaises
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the exception as
     |      the 'exception' attribute. This allows you to inspect the
     |      exception after the assertion::
     |      
     |          with self.assertRaises(SomeException) as cm:
     |              do_something()
     |          the_exception = cm.exception
     |          self.assertEqual(the_exception.error_code, 3)
     |  
     |  assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs)
     |      Asserts that the message in a raised exception matches a regex.
     |      
     |      Args:
     |          expected_exception: Exception class expected to be raised.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertRaisesRegex is used as a context manager.
     |  
     |  assertRaisesRegexp = deprecated_func(*args, **kwargs)
     |  
     |  assertRegex(self, text, expected_regex, msg=None)
     |      Fail the test unless the text matches the regular expression.
     |  
     |  assertRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None)
     |      An equality assertion for ordered sequences (like lists and tuples).
     |      
     |      For the purposes of this function, a valid ordered sequence type is one
     |      which can be indexed, has a length, and has an equality operator.
     |      
     |      Args:
     |          seq1: The first sequence to compare.
     |          seq2: The second sequence to compare.
     |          seq_type: The expected datatype of the sequences, or None if no
     |                  datatype should be enforced.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertSetEqual(self, set1, set2, msg=None)
     |      A set-specific equality assertion.
     |      
     |      Args:
     |          set1: The first set to compare.
     |          set2: The second set to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |      
     |      assertSetEqual uses ducktyping to support different types of sets, and
     |      is optimized for sets specifically (parameters must support a
     |      difference method).
     |  
     |  assertTrue(self, expr, msg=None)
     |      Check that the expression is true.
     |  
     |  assertTupleEqual(self, tuple1, tuple2, msg=None)
     |      A tuple-specific equality assertion.
     |      
     |      Args:
     |          tuple1: The first tuple to compare.
     |          tuple2: The second tuple to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertWarns(self, expected_warning, *args, **kwargs)
     |      Fail unless a warning of class warnClass is triggered
     |      by the callable when invoked with specified positional and
     |      keyword arguments.  If a different type of warning is
     |      triggered, it will not be handled: depending on the other
     |      warning filtering rules in effect, it might be silenced, printed
     |      out, or raised as an exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertWarns(SomeWarning):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertWarns
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the first matching
     |      warning as the 'warning' attribute; similarly, the 'filename'
     |      and 'lineno' attributes give you information about the line
     |      of Python code from which the warning was triggered.
     |      This allows you to inspect the warning after the assertion::
     |      
     |          with self.assertWarns(SomeWarning) as cm:
     |              do_something()
     |          the_warning = cm.warning
     |          self.assertEqual(the_warning.some_attribute, 147)
     |  
     |  assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs)
     |      Asserts that the message in a triggered warning matches a regexp.
     |      Basic functioning is similar to assertWarns() with the addition
     |      that only warnings whose messages also match the regular expression
     |      are considered successful matches.
     |      
     |      Args:
     |          expected_warning: Warning class expected to be triggered.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertWarnsRegex is used as a context manager.
     |  
     |  assert_ = deprecated_func(*args, **kwargs)
     |  
     |  countTestCases(self)
     |  
     |  debug(self)
     |      Run the test without collecting errors in a TestResult
     |  
     |  defaultTestResult(self)
     |  
     |  doCleanups(self)
     |      Execute all cleanup functions. Normally called for you after
     |      tearDown.
     |  
     |  fail(self, msg=None)
     |      Fail immediately, with the given message.
     |  
     |  failIf = deprecated_func(*args, **kwargs)
     |  
     |  failIfAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failIfEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnless = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessRaises = deprecated_func(*args, **kwargs)
     |  
     |  id(self)
     |  
     |  run(self, result=None)
     |  
     |  shortDescription(self)
     |      Returns a one-line description of the test, or None if no
     |      description has been provided.
     |      
     |      The default implementation of this method returns the first line of
     |      the specified test method's docstring.
     |  
     |  skipTest(self, reason)
     |      Skip this test.
     |  
     |  subTest(self, msg=<object object at 0x7f267fce1280>, **params)
     |      Return a context manager that will return the enclosed block
     |      of code in a subtest identified by the optional message and
     |      keyword parameters.  A failure in the subtest marks the test
     |      case as failed but resumes execution at the end of the enclosed
     |      block, allowing further test code to be executed.
     |  
     |  tearDown(self)
     |      Hook method for deconstructing the test fixture after testing it.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from unittest.case.TestCase:
     |  
     |  setUpClass() from builtins.type
     |      Hook method for setting up class fixture before running tests in the class.
     |  
     |  tearDownClass() from builtins.type
     |      Hook method for deconstructing the class fixture after running all tests in the class.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from unittest.case.TestCase:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from unittest.case.TestCase:
     |  
     |  failureException = <class 'AssertionError'>
     |      Assertion failed.
     |  
     |  longMessage = True
     |  
     |  maxDiff = 640


```


## mr_utils.tests.recon.test_multiphase

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/recon/test_multiphase.py)

```
NAME
    mr_utils.tests.recon.test_multiphase

CLASSES
    unittest.case.TestCase(builtins.object)
        MultiphaseTestCase
    
    class MultiphaseTestCase(unittest.case.TestCase)
     |  A class whose instances are single test cases.
     |  
     |  By default, the test code itself should be placed in a method named
     |  'runTest'.
     |  
     |  If the fixture may be used for many test cases, create as
     |  many test methods as are needed. When instantiating such a TestCase
     |  subclass, specify in the constructor arguments the name of the test method
     |  that the instance is to execute.
     |  
     |  Test authors should subclass TestCase for their own tests. Construction
     |  and deconstruction of the test's environment ('fixture') can be
     |  implemented by overriding the 'setUp' and 'tearDown' methods respectively.
     |  
     |  If it is necessary to override the __init__ method, the base class
     |  __init__ method must always be called. It is important that subclasses
     |  should not change the signature of their __init__ method, since instances
     |  of the classes are instantiated automatically by parts of the framework
     |  in order to be run.
     |  
     |  When subclassing TestCase, you can set these attributes:
     |  * failureException: determines which exception will be raised when
     |      the instance's assertion methods fail; test methods raising this
     |      exception will be deemed to have 'failed' rather than 'errored'.
     |  * longMessage: determines whether long messages (including repr of
     |      objects used in assert methods) will be printed on failure in *addition*
     |      to any explicit message passed.
     |  * maxDiff: sets the maximum length of a diff in failure messages
     |      by assert methods using difflib. It is looked up as an instance
     |      attribute so can be configured by individual tests if required.
     |  
     |  Method resolution order:
     |      MultiphaseTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_multiphase(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from unittest.case.TestCase:
     |  
     |  __call__(self, *args, **kwds)
     |      Call self as a function.
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, methodName='runTest')
     |      Create an instance of the class that will use the named test
     |      method when executed. Raises a ValueError if the instance does
     |      not have a method with the specified name.
     |  
     |  __repr__(self)
     |      Return repr(self).
     |  
     |  __str__(self)
     |      Return str(self).
     |  
     |  addCleanup(self, function, *args, **kwargs)
     |      Add a function, with arguments, to be called when the test is
     |      completed. Functions added are called on a LIFO basis and are
     |      called after tearDown on test failure or success.
     |      
     |      Cleanup items are called even if setUp fails (unlike tearDown).
     |  
     |  addTypeEqualityFunc(self, typeobj, function)
     |      Add a type specific assertEqual style function to compare a type.
     |      
     |      This method is for use by TestCase subclasses that need to register
     |      their own type equality functions to provide nicer error messages.
     |      
     |      Args:
     |          typeobj: The data type to call this function on when both values
     |                  are of the same type in assertEqual().
     |          function: The callable taking two arguments and an optional
     |                  msg= argument that raises self.failureException with a
     |                  useful error message when the two arguments are not equal.
     |  
     |  assertAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are unequal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is more than the given
     |      delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      If the two objects compare equal then they will automatically
     |      compare almost equal.
     |  
     |  assertAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertCountEqual(self, first, second, msg=None)
     |      An unordered sequence comparison asserting that the same elements,
     |      regardless of order.  If the same element occurs more than once,
     |      it verifies that the elements occur the same number of times.
     |      
     |          self.assertEqual(Counter(list(first)),
     |                           Counter(list(second)))
     |      
     |       Example:
     |          - [0, 1, 1] and [1, 0, 1] compare equal.
     |          - [0, 0, 1] and [0, 1] compare unequal.
     |  
     |  assertDictContainsSubset(self, subset, dictionary, msg=None)
     |      Checks whether dictionary is a superset of subset.
     |  
     |  assertDictEqual(self, d1, d2, msg=None)
     |  
     |  assertEqual(self, first, second, msg=None)
     |      Fail if the two objects are unequal as determined by the '=='
     |      operator.
     |  
     |  assertEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertFalse(self, expr, msg=None)
     |      Check that the expression is false.
     |  
     |  assertGreater(self, a, b, msg=None)
     |      Just like self.assertTrue(a > b), but with a nicer default message.
     |  
     |  assertGreaterEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a >= b), but with a nicer default message.
     |  
     |  assertIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a in b), but with a nicer default message.
     |  
     |  assertIs(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is b), but with a nicer default message.
     |  
     |  assertIsInstance(self, obj, cls, msg=None)
     |      Same as self.assertTrue(isinstance(obj, cls)), with a nicer
     |      default message.
     |  
     |  assertIsNone(self, obj, msg=None)
     |      Same as self.assertTrue(obj is None), with a nicer default message.
     |  
     |  assertIsNot(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is not b), but with a nicer default message.
     |  
     |  assertIsNotNone(self, obj, msg=None)
     |      Included for symmetry with assertIsNone.
     |  
     |  assertLess(self, a, b, msg=None)
     |      Just like self.assertTrue(a < b), but with a nicer default message.
     |  
     |  assertLessEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a <= b), but with a nicer default message.
     |  
     |  assertListEqual(self, list1, list2, msg=None)
     |      A list-specific equality assertion.
     |      
     |      Args:
     |          list1: The first list to compare.
     |          list2: The second list to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertLogs(self, logger=None, level=None)
     |      Fail unless a log message of level *level* or higher is emitted
     |      on *logger_name* or its children.  If omitted, *level* defaults to
     |      INFO and *logger* defaults to the root logger.
     |      
     |      This method must be used as a context manager, and will yield
     |      a recording object with two attributes: `output` and `records`.
     |      At the end of the context manager, the `output` attribute will
     |      be a list of the matching formatted log messages and the
     |      `records` attribute will be a list of the corresponding LogRecord
     |      objects.
     |      
     |      Example::
     |      
     |          with self.assertLogs('foo', level='INFO') as cm:
     |              logging.getLogger('foo').info('first message')
     |              logging.getLogger('foo.bar').error('second message')
     |          self.assertEqual(cm.output, ['INFO:foo:first message',
     |                                       'ERROR:foo.bar:second message'])
     |  
     |  assertMultiLineEqual(self, first, second, msg=None)
     |      Assert that two multi-line strings are equal.
     |  
     |  assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are equal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is less than the given delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      Objects that are equal automatically fail.
     |  
     |  assertNotAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotEqual(self, first, second, msg=None)
     |      Fail if the two objects are equal as determined by the '!='
     |      operator.
     |  
     |  assertNotEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a not in b), but with a nicer default message.
     |  
     |  assertNotIsInstance(self, obj, cls, msg=None)
     |      Included for symmetry with assertIsInstance.
     |  
     |  assertNotRegex(self, text, unexpected_regex, msg=None)
     |      Fail the test if the text matches the regular expression.
     |  
     |  assertNotRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertRaises(self, expected_exception, *args, **kwargs)
     |      Fail unless an exception of class expected_exception is raised
     |      by the callable when invoked with specified positional and
     |      keyword arguments. If a different type of exception is
     |      raised, it will not be caught, and the test case will be
     |      deemed to have suffered an error, exactly as for an
     |      unexpected exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertRaises(SomeException):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertRaises
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the exception as
     |      the 'exception' attribute. This allows you to inspect the
     |      exception after the assertion::
     |      
     |          with self.assertRaises(SomeException) as cm:
     |              do_something()
     |          the_exception = cm.exception
     |          self.assertEqual(the_exception.error_code, 3)
     |  
     |  assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs)
     |      Asserts that the message in a raised exception matches a regex.
     |      
     |      Args:
     |          expected_exception: Exception class expected to be raised.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertRaisesRegex is used as a context manager.
     |  
     |  assertRaisesRegexp = deprecated_func(*args, **kwargs)
     |  
     |  assertRegex(self, text, expected_regex, msg=None)
     |      Fail the test unless the text matches the regular expression.
     |  
     |  assertRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None)
     |      An equality assertion for ordered sequences (like lists and tuples).
     |      
     |      For the purposes of this function, a valid ordered sequence type is one
     |      which can be indexed, has a length, and has an equality operator.
     |      
     |      Args:
     |          seq1: The first sequence to compare.
     |          seq2: The second sequence to compare.
     |          seq_type: The expected datatype of the sequences, or None if no
     |                  datatype should be enforced.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertSetEqual(self, set1, set2, msg=None)
     |      A set-specific equality assertion.
     |      
     |      Args:
     |          set1: The first set to compare.
     |          set2: The second set to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |      
     |      assertSetEqual uses ducktyping to support different types of sets, and
     |      is optimized for sets specifically (parameters must support a
     |      difference method).
     |  
     |  assertTrue(self, expr, msg=None)
     |      Check that the expression is true.
     |  
     |  assertTupleEqual(self, tuple1, tuple2, msg=None)
     |      A tuple-specific equality assertion.
     |      
     |      Args:
     |          tuple1: The first tuple to compare.
     |          tuple2: The second tuple to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertWarns(self, expected_warning, *args, **kwargs)
     |      Fail unless a warning of class warnClass is triggered
     |      by the callable when invoked with specified positional and
     |      keyword arguments.  If a different type of warning is
     |      triggered, it will not be handled: depending on the other
     |      warning filtering rules in effect, it might be silenced, printed
     |      out, or raised as an exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertWarns(SomeWarning):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertWarns
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the first matching
     |      warning as the 'warning' attribute; similarly, the 'filename'
     |      and 'lineno' attributes give you information about the line
     |      of Python code from which the warning was triggered.
     |      This allows you to inspect the warning after the assertion::
     |      
     |          with self.assertWarns(SomeWarning) as cm:
     |              do_something()
     |          the_warning = cm.warning
     |          self.assertEqual(the_warning.some_attribute, 147)
     |  
     |  assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs)
     |      Asserts that the message in a triggered warning matches a regexp.
     |      Basic functioning is similar to assertWarns() with the addition
     |      that only warnings whose messages also match the regular expression
     |      are considered successful matches.
     |      
     |      Args:
     |          expected_warning: Warning class expected to be triggered.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertWarnsRegex is used as a context manager.
     |  
     |  assert_ = deprecated_func(*args, **kwargs)
     |  
     |  countTestCases(self)
     |  
     |  debug(self)
     |      Run the test without collecting errors in a TestResult
     |  
     |  defaultTestResult(self)
     |  
     |  doCleanups(self)
     |      Execute all cleanup functions. Normally called for you after
     |      tearDown.
     |  
     |  fail(self, msg=None)
     |      Fail immediately, with the given message.
     |  
     |  failIf = deprecated_func(*args, **kwargs)
     |  
     |  failIfAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failIfEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnless = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessRaises = deprecated_func(*args, **kwargs)
     |  
     |  id(self)
     |  
     |  run(self, result=None)
     |  
     |  shortDescription(self)
     |      Returns a one-line description of the test, or None if no
     |      description has been provided.
     |      
     |      The default implementation of this method returns the first line of
     |      the specified test method's docstring.
     |  
     |  skipTest(self, reason)
     |      Skip this test.
     |  
     |  subTest(self, msg=<object object at 0x7f267fce1280>, **params)
     |      Return a context manager that will return the enclosed block
     |      of code in a subtest identified by the optional message and
     |      keyword parameters.  A failure in the subtest marks the test
     |      case as failed but resumes execution at the end of the enclosed
     |      block, allowing further test code to be executed.
     |  
     |  tearDown(self)
     |      Hook method for deconstructing the test fixture after testing it.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from unittest.case.TestCase:
     |  
     |  setUpClass() from builtins.type
     |      Hook method for setting up class fixture before running tests in the class.
     |  
     |  tearDownClass() from builtins.type
     |      Hook method for deconstructing the class fixture after running all tests in the class.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from unittest.case.TestCase:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from unittest.case.TestCase:
     |  
     |  failureException = <class 'AssertionError'>
     |      Assertion failed.
     |  
     |  longMessage = True
     |  
     |  maxDiff = 640


```


## mr_utils.tests.recon.test_partial_fourier_pocs

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/recon/test_partial_fourier_pocs.py)

```
NAME
    mr_utils.tests.recon.test_partial_fourier_pocs

CLASSES
    unittest.case.TestCase(builtins.object)
        PartialFourerPOCSTestCase
    
    class PartialFourerPOCSTestCase(unittest.case.TestCase)
     |  A class whose instances are single test cases.
     |  
     |  By default, the test code itself should be placed in a method named
     |  'runTest'.
     |  
     |  If the fixture may be used for many test cases, create as
     |  many test methods as are needed. When instantiating such a TestCase
     |  subclass, specify in the constructor arguments the name of the test method
     |  that the instance is to execute.
     |  
     |  Test authors should subclass TestCase for their own tests. Construction
     |  and deconstruction of the test's environment ('fixture') can be
     |  implemented by overriding the 'setUp' and 'tearDown' methods respectively.
     |  
     |  If it is necessary to override the __init__ method, the base class
     |  __init__ method must always be called. It is important that subclasses
     |  should not change the signature of their __init__ method, since instances
     |  of the classes are instantiated automatically by parts of the framework
     |  in order to be run.
     |  
     |  When subclassing TestCase, you can set these attributes:
     |  * failureException: determines which exception will be raised when
     |      the instance's assertion methods fail; test methods raising this
     |      exception will be deemed to have 'failed' rather than 'errored'.
     |  * longMessage: determines whether long messages (including repr of
     |      objects used in assert methods) will be printed on failure in *addition*
     |      to any explicit message passed.
     |  * maxDiff: sets the maximum length of a diff in failure messages
     |      by assert methods using difflib. It is looked up as an instance
     |      attribute so can be configured by individual tests if required.
     |  
     |  Method resolution order:
     |      PartialFourerPOCSTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  test_partial_fourier_pocs(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from unittest.case.TestCase:
     |  
     |  __call__(self, *args, **kwds)
     |      Call self as a function.
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, methodName='runTest')
     |      Create an instance of the class that will use the named test
     |      method when executed. Raises a ValueError if the instance does
     |      not have a method with the specified name.
     |  
     |  __repr__(self)
     |      Return repr(self).
     |  
     |  __str__(self)
     |      Return str(self).
     |  
     |  addCleanup(self, function, *args, **kwargs)
     |      Add a function, with arguments, to be called when the test is
     |      completed. Functions added are called on a LIFO basis and are
     |      called after tearDown on test failure or success.
     |      
     |      Cleanup items are called even if setUp fails (unlike tearDown).
     |  
     |  addTypeEqualityFunc(self, typeobj, function)
     |      Add a type specific assertEqual style function to compare a type.
     |      
     |      This method is for use by TestCase subclasses that need to register
     |      their own type equality functions to provide nicer error messages.
     |      
     |      Args:
     |          typeobj: The data type to call this function on when both values
     |                  are of the same type in assertEqual().
     |          function: The callable taking two arguments and an optional
     |                  msg= argument that raises self.failureException with a
     |                  useful error message when the two arguments are not equal.
     |  
     |  assertAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are unequal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is more than the given
     |      delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      If the two objects compare equal then they will automatically
     |      compare almost equal.
     |  
     |  assertAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertCountEqual(self, first, second, msg=None)
     |      An unordered sequence comparison asserting that the same elements,
     |      regardless of order.  If the same element occurs more than once,
     |      it verifies that the elements occur the same number of times.
     |      
     |          self.assertEqual(Counter(list(first)),
     |                           Counter(list(second)))
     |      
     |       Example:
     |          - [0, 1, 1] and [1, 0, 1] compare equal.
     |          - [0, 0, 1] and [0, 1] compare unequal.
     |  
     |  assertDictContainsSubset(self, subset, dictionary, msg=None)
     |      Checks whether dictionary is a superset of subset.
     |  
     |  assertDictEqual(self, d1, d2, msg=None)
     |  
     |  assertEqual(self, first, second, msg=None)
     |      Fail if the two objects are unequal as determined by the '=='
     |      operator.
     |  
     |  assertEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertFalse(self, expr, msg=None)
     |      Check that the expression is false.
     |  
     |  assertGreater(self, a, b, msg=None)
     |      Just like self.assertTrue(a > b), but with a nicer default message.
     |  
     |  assertGreaterEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a >= b), but with a nicer default message.
     |  
     |  assertIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a in b), but with a nicer default message.
     |  
     |  assertIs(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is b), but with a nicer default message.
     |  
     |  assertIsInstance(self, obj, cls, msg=None)
     |      Same as self.assertTrue(isinstance(obj, cls)), with a nicer
     |      default message.
     |  
     |  assertIsNone(self, obj, msg=None)
     |      Same as self.assertTrue(obj is None), with a nicer default message.
     |  
     |  assertIsNot(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is not b), but with a nicer default message.
     |  
     |  assertIsNotNone(self, obj, msg=None)
     |      Included for symmetry with assertIsNone.
     |  
     |  assertLess(self, a, b, msg=None)
     |      Just like self.assertTrue(a < b), but with a nicer default message.
     |  
     |  assertLessEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a <= b), but with a nicer default message.
     |  
     |  assertListEqual(self, list1, list2, msg=None)
     |      A list-specific equality assertion.
     |      
     |      Args:
     |          list1: The first list to compare.
     |          list2: The second list to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertLogs(self, logger=None, level=None)
     |      Fail unless a log message of level *level* or higher is emitted
     |      on *logger_name* or its children.  If omitted, *level* defaults to
     |      INFO and *logger* defaults to the root logger.
     |      
     |      This method must be used as a context manager, and will yield
     |      a recording object with two attributes: `output` and `records`.
     |      At the end of the context manager, the `output` attribute will
     |      be a list of the matching formatted log messages and the
     |      `records` attribute will be a list of the corresponding LogRecord
     |      objects.
     |      
     |      Example::
     |      
     |          with self.assertLogs('foo', level='INFO') as cm:
     |              logging.getLogger('foo').info('first message')
     |              logging.getLogger('foo.bar').error('second message')
     |          self.assertEqual(cm.output, ['INFO:foo:first message',
     |                                       'ERROR:foo.bar:second message'])
     |  
     |  assertMultiLineEqual(self, first, second, msg=None)
     |      Assert that two multi-line strings are equal.
     |  
     |  assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are equal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is less than the given delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      Objects that are equal automatically fail.
     |  
     |  assertNotAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotEqual(self, first, second, msg=None)
     |      Fail if the two objects are equal as determined by the '!='
     |      operator.
     |  
     |  assertNotEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a not in b), but with a nicer default message.
     |  
     |  assertNotIsInstance(self, obj, cls, msg=None)
     |      Included for symmetry with assertIsInstance.
     |  
     |  assertNotRegex(self, text, unexpected_regex, msg=None)
     |      Fail the test if the text matches the regular expression.
     |  
     |  assertNotRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertRaises(self, expected_exception, *args, **kwargs)
     |      Fail unless an exception of class expected_exception is raised
     |      by the callable when invoked with specified positional and
     |      keyword arguments. If a different type of exception is
     |      raised, it will not be caught, and the test case will be
     |      deemed to have suffered an error, exactly as for an
     |      unexpected exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertRaises(SomeException):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertRaises
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the exception as
     |      the 'exception' attribute. This allows you to inspect the
     |      exception after the assertion::
     |      
     |          with self.assertRaises(SomeException) as cm:
     |              do_something()
     |          the_exception = cm.exception
     |          self.assertEqual(the_exception.error_code, 3)
     |  
     |  assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs)
     |      Asserts that the message in a raised exception matches a regex.
     |      
     |      Args:
     |          expected_exception: Exception class expected to be raised.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertRaisesRegex is used as a context manager.
     |  
     |  assertRaisesRegexp = deprecated_func(*args, **kwargs)
     |  
     |  assertRegex(self, text, expected_regex, msg=None)
     |      Fail the test unless the text matches the regular expression.
     |  
     |  assertRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None)
     |      An equality assertion for ordered sequences (like lists and tuples).
     |      
     |      For the purposes of this function, a valid ordered sequence type is one
     |      which can be indexed, has a length, and has an equality operator.
     |      
     |      Args:
     |          seq1: The first sequence to compare.
     |          seq2: The second sequence to compare.
     |          seq_type: The expected datatype of the sequences, or None if no
     |                  datatype should be enforced.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertSetEqual(self, set1, set2, msg=None)
     |      A set-specific equality assertion.
     |      
     |      Args:
     |          set1: The first set to compare.
     |          set2: The second set to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |      
     |      assertSetEqual uses ducktyping to support different types of sets, and
     |      is optimized for sets specifically (parameters must support a
     |      difference method).
     |  
     |  assertTrue(self, expr, msg=None)
     |      Check that the expression is true.
     |  
     |  assertTupleEqual(self, tuple1, tuple2, msg=None)
     |      A tuple-specific equality assertion.
     |      
     |      Args:
     |          tuple1: The first tuple to compare.
     |          tuple2: The second tuple to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertWarns(self, expected_warning, *args, **kwargs)
     |      Fail unless a warning of class warnClass is triggered
     |      by the callable when invoked with specified positional and
     |      keyword arguments.  If a different type of warning is
     |      triggered, it will not be handled: depending on the other
     |      warning filtering rules in effect, it might be silenced, printed
     |      out, or raised as an exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertWarns(SomeWarning):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertWarns
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the first matching
     |      warning as the 'warning' attribute; similarly, the 'filename'
     |      and 'lineno' attributes give you information about the line
     |      of Python code from which the warning was triggered.
     |      This allows you to inspect the warning after the assertion::
     |      
     |          with self.assertWarns(SomeWarning) as cm:
     |              do_something()
     |          the_warning = cm.warning
     |          self.assertEqual(the_warning.some_attribute, 147)
     |  
     |  assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs)
     |      Asserts that the message in a triggered warning matches a regexp.
     |      Basic functioning is similar to assertWarns() with the addition
     |      that only warnings whose messages also match the regular expression
     |      are considered successful matches.
     |      
     |      Args:
     |          expected_warning: Warning class expected to be triggered.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertWarnsRegex is used as a context manager.
     |  
     |  assert_ = deprecated_func(*args, **kwargs)
     |  
     |  countTestCases(self)
     |  
     |  debug(self)
     |      Run the test without collecting errors in a TestResult
     |  
     |  defaultTestResult(self)
     |  
     |  doCleanups(self)
     |      Execute all cleanup functions. Normally called for you after
     |      tearDown.
     |  
     |  fail(self, msg=None)
     |      Fail immediately, with the given message.
     |  
     |  failIf = deprecated_func(*args, **kwargs)
     |  
     |  failIfAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failIfEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnless = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessRaises = deprecated_func(*args, **kwargs)
     |  
     |  id(self)
     |  
     |  run(self, result=None)
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  shortDescription(self)
     |      Returns a one-line description of the test, or None if no
     |      description has been provided.
     |      
     |      The default implementation of this method returns the first line of
     |      the specified test method's docstring.
     |  
     |  skipTest(self, reason)
     |      Skip this test.
     |  
     |  subTest(self, msg=<object object at 0x7f267fce1280>, **params)
     |      Return a context manager that will return the enclosed block
     |      of code in a subtest identified by the optional message and
     |      keyword parameters.  A failure in the subtest marks the test
     |      case as failed but resumes execution at the end of the enclosed
     |      block, allowing further test code to be executed.
     |  
     |  tearDown(self)
     |      Hook method for deconstructing the test fixture after testing it.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from unittest.case.TestCase:
     |  
     |  setUpClass() from builtins.type
     |      Hook method for setting up class fixture before running tests in the class.
     |  
     |  tearDownClass() from builtins.type
     |      Hook method for deconstructing the class fixture after running all tests in the class.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from unittest.case.TestCase:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from unittest.case.TestCase:
     |  
     |  failureException = <class 'AssertionError'>
     |      Assertion failed.
     |  
     |  longMessage = True
     |  
     |  maxDiff = 640


```


## mr_utils.tests.recon.test_patch_reordering

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/recon/test_patch_reordering.py)

```
NAME
    mr_utils.tests.recon.test_patch_reordering

CLASSES
    unittest.case.TestCase(builtins.object)
        PatchReorderTestCase
    
    class PatchReorderTestCase(unittest.case.TestCase)
     |  A class whose instances are single test cases.
     |  
     |  By default, the test code itself should be placed in a method named
     |  'runTest'.
     |  
     |  If the fixture may be used for many test cases, create as
     |  many test methods as are needed. When instantiating such a TestCase
     |  subclass, specify in the constructor arguments the name of the test method
     |  that the instance is to execute.
     |  
     |  Test authors should subclass TestCase for their own tests. Construction
     |  and deconstruction of the test's environment ('fixture') can be
     |  implemented by overriding the 'setUp' and 'tearDown' methods respectively.
     |  
     |  If it is necessary to override the __init__ method, the base class
     |  __init__ method must always be called. It is important that subclasses
     |  should not change the signature of their __init__ method, since instances
     |  of the classes are instantiated automatically by parts of the framework
     |  in order to be run.
     |  
     |  When subclassing TestCase, you can set these attributes:
     |  * failureException: determines which exception will be raised when
     |      the instance's assertion methods fail; test methods raising this
     |      exception will be deemed to have 'failed' rather than 'errored'.
     |  * longMessage: determines whether long messages (including repr of
     |      objects used in assert methods) will be printed on failure in *addition*
     |      to any explicit message passed.
     |  * maxDiff: sets the maximum length of a diff in failure messages
     |      by assert methods using difflib. It is looked up as an instance
     |      attribute so can be configured by individual tests if required.
     |  
     |  Method resolution order:
     |      PatchReorderTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_reorder(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from unittest.case.TestCase:
     |  
     |  __call__(self, *args, **kwds)
     |      Call self as a function.
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, methodName='runTest')
     |      Create an instance of the class that will use the named test
     |      method when executed. Raises a ValueError if the instance does
     |      not have a method with the specified name.
     |  
     |  __repr__(self)
     |      Return repr(self).
     |  
     |  __str__(self)
     |      Return str(self).
     |  
     |  addCleanup(self, function, *args, **kwargs)
     |      Add a function, with arguments, to be called when the test is
     |      completed. Functions added are called on a LIFO basis and are
     |      called after tearDown on test failure or success.
     |      
     |      Cleanup items are called even if setUp fails (unlike tearDown).
     |  
     |  addTypeEqualityFunc(self, typeobj, function)
     |      Add a type specific assertEqual style function to compare a type.
     |      
     |      This method is for use by TestCase subclasses that need to register
     |      their own type equality functions to provide nicer error messages.
     |      
     |      Args:
     |          typeobj: The data type to call this function on when both values
     |                  are of the same type in assertEqual().
     |          function: The callable taking two arguments and an optional
     |                  msg= argument that raises self.failureException with a
     |                  useful error message when the two arguments are not equal.
     |  
     |  assertAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are unequal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is more than the given
     |      delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      If the two objects compare equal then they will automatically
     |      compare almost equal.
     |  
     |  assertAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertCountEqual(self, first, second, msg=None)
     |      An unordered sequence comparison asserting that the same elements,
     |      regardless of order.  If the same element occurs more than once,
     |      it verifies that the elements occur the same number of times.
     |      
     |          self.assertEqual(Counter(list(first)),
     |                           Counter(list(second)))
     |      
     |       Example:
     |          - [0, 1, 1] and [1, 0, 1] compare equal.
     |          - [0, 0, 1] and [0, 1] compare unequal.
     |  
     |  assertDictContainsSubset(self, subset, dictionary, msg=None)
     |      Checks whether dictionary is a superset of subset.
     |  
     |  assertDictEqual(self, d1, d2, msg=None)
     |  
     |  assertEqual(self, first, second, msg=None)
     |      Fail if the two objects are unequal as determined by the '=='
     |      operator.
     |  
     |  assertEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertFalse(self, expr, msg=None)
     |      Check that the expression is false.
     |  
     |  assertGreater(self, a, b, msg=None)
     |      Just like self.assertTrue(a > b), but with a nicer default message.
     |  
     |  assertGreaterEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a >= b), but with a nicer default message.
     |  
     |  assertIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a in b), but with a nicer default message.
     |  
     |  assertIs(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is b), but with a nicer default message.
     |  
     |  assertIsInstance(self, obj, cls, msg=None)
     |      Same as self.assertTrue(isinstance(obj, cls)), with a nicer
     |      default message.
     |  
     |  assertIsNone(self, obj, msg=None)
     |      Same as self.assertTrue(obj is None), with a nicer default message.
     |  
     |  assertIsNot(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is not b), but with a nicer default message.
     |  
     |  assertIsNotNone(self, obj, msg=None)
     |      Included for symmetry with assertIsNone.
     |  
     |  assertLess(self, a, b, msg=None)
     |      Just like self.assertTrue(a < b), but with a nicer default message.
     |  
     |  assertLessEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a <= b), but with a nicer default message.
     |  
     |  assertListEqual(self, list1, list2, msg=None)
     |      A list-specific equality assertion.
     |      
     |      Args:
     |          list1: The first list to compare.
     |          list2: The second list to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertLogs(self, logger=None, level=None)
     |      Fail unless a log message of level *level* or higher is emitted
     |      on *logger_name* or its children.  If omitted, *level* defaults to
     |      INFO and *logger* defaults to the root logger.
     |      
     |      This method must be used as a context manager, and will yield
     |      a recording object with two attributes: `output` and `records`.
     |      At the end of the context manager, the `output` attribute will
     |      be a list of the matching formatted log messages and the
     |      `records` attribute will be a list of the corresponding LogRecord
     |      objects.
     |      
     |      Example::
     |      
     |          with self.assertLogs('foo', level='INFO') as cm:
     |              logging.getLogger('foo').info('first message')
     |              logging.getLogger('foo.bar').error('second message')
     |          self.assertEqual(cm.output, ['INFO:foo:first message',
     |                                       'ERROR:foo.bar:second message'])
     |  
     |  assertMultiLineEqual(self, first, second, msg=None)
     |      Assert that two multi-line strings are equal.
     |  
     |  assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are equal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is less than the given delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      Objects that are equal automatically fail.
     |  
     |  assertNotAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotEqual(self, first, second, msg=None)
     |      Fail if the two objects are equal as determined by the '!='
     |      operator.
     |  
     |  assertNotEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a not in b), but with a nicer default message.
     |  
     |  assertNotIsInstance(self, obj, cls, msg=None)
     |      Included for symmetry with assertIsInstance.
     |  
     |  assertNotRegex(self, text, unexpected_regex, msg=None)
     |      Fail the test if the text matches the regular expression.
     |  
     |  assertNotRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertRaises(self, expected_exception, *args, **kwargs)
     |      Fail unless an exception of class expected_exception is raised
     |      by the callable when invoked with specified positional and
     |      keyword arguments. If a different type of exception is
     |      raised, it will not be caught, and the test case will be
     |      deemed to have suffered an error, exactly as for an
     |      unexpected exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertRaises(SomeException):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertRaises
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the exception as
     |      the 'exception' attribute. This allows you to inspect the
     |      exception after the assertion::
     |      
     |          with self.assertRaises(SomeException) as cm:
     |              do_something()
     |          the_exception = cm.exception
     |          self.assertEqual(the_exception.error_code, 3)
     |  
     |  assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs)
     |      Asserts that the message in a raised exception matches a regex.
     |      
     |      Args:
     |          expected_exception: Exception class expected to be raised.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertRaisesRegex is used as a context manager.
     |  
     |  assertRaisesRegexp = deprecated_func(*args, **kwargs)
     |  
     |  assertRegex(self, text, expected_regex, msg=None)
     |      Fail the test unless the text matches the regular expression.
     |  
     |  assertRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None)
     |      An equality assertion for ordered sequences (like lists and tuples).
     |      
     |      For the purposes of this function, a valid ordered sequence type is one
     |      which can be indexed, has a length, and has an equality operator.
     |      
     |      Args:
     |          seq1: The first sequence to compare.
     |          seq2: The second sequence to compare.
     |          seq_type: The expected datatype of the sequences, or None if no
     |                  datatype should be enforced.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertSetEqual(self, set1, set2, msg=None)
     |      A set-specific equality assertion.
     |      
     |      Args:
     |          set1: The first set to compare.
     |          set2: The second set to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |      
     |      assertSetEqual uses ducktyping to support different types of sets, and
     |      is optimized for sets specifically (parameters must support a
     |      difference method).
     |  
     |  assertTrue(self, expr, msg=None)
     |      Check that the expression is true.
     |  
     |  assertTupleEqual(self, tuple1, tuple2, msg=None)
     |      A tuple-specific equality assertion.
     |      
     |      Args:
     |          tuple1: The first tuple to compare.
     |          tuple2: The second tuple to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertWarns(self, expected_warning, *args, **kwargs)
     |      Fail unless a warning of class warnClass is triggered
     |      by the callable when invoked with specified positional and
     |      keyword arguments.  If a different type of warning is
     |      triggered, it will not be handled: depending on the other
     |      warning filtering rules in effect, it might be silenced, printed
     |      out, or raised as an exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertWarns(SomeWarning):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertWarns
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the first matching
     |      warning as the 'warning' attribute; similarly, the 'filename'
     |      and 'lineno' attributes give you information about the line
     |      of Python code from which the warning was triggered.
     |      This allows you to inspect the warning after the assertion::
     |      
     |          with self.assertWarns(SomeWarning) as cm:
     |              do_something()
     |          the_warning = cm.warning
     |          self.assertEqual(the_warning.some_attribute, 147)
     |  
     |  assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs)
     |      Asserts that the message in a triggered warning matches a regexp.
     |      Basic functioning is similar to assertWarns() with the addition
     |      that only warnings whose messages also match the regular expression
     |      are considered successful matches.
     |      
     |      Args:
     |          expected_warning: Warning class expected to be triggered.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertWarnsRegex is used as a context manager.
     |  
     |  assert_ = deprecated_func(*args, **kwargs)
     |  
     |  countTestCases(self)
     |  
     |  debug(self)
     |      Run the test without collecting errors in a TestResult
     |  
     |  defaultTestResult(self)
     |  
     |  doCleanups(self)
     |      Execute all cleanup functions. Normally called for you after
     |      tearDown.
     |  
     |  fail(self, msg=None)
     |      Fail immediately, with the given message.
     |  
     |  failIf = deprecated_func(*args, **kwargs)
     |  
     |  failIfAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failIfEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnless = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessRaises = deprecated_func(*args, **kwargs)
     |  
     |  id(self)
     |  
     |  run(self, result=None)
     |  
     |  shortDescription(self)
     |      Returns a one-line description of the test, or None if no
     |      description has been provided.
     |      
     |      The default implementation of this method returns the first line of
     |      the specified test method's docstring.
     |  
     |  skipTest(self, reason)
     |      Skip this test.
     |  
     |  subTest(self, msg=<object object at 0x7f267fce1280>, **params)
     |      Return a context manager that will return the enclosed block
     |      of code in a subtest identified by the optional message and
     |      keyword parameters.  A failure in the subtest marks the test
     |      case as failed but resumes execution at the end of the enclosed
     |      block, allowing further test code to be executed.
     |  
     |  tearDown(self)
     |      Hook method for deconstructing the test fixture after testing it.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from unittest.case.TestCase:
     |  
     |  setUpClass() from builtins.type
     |      Hook method for setting up class fixture before running tests in the class.
     |  
     |  tearDownClass() from builtins.type
     |      Hook method for deconstructing the class fixture after running all tests in the class.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from unittest.case.TestCase:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from unittest.case.TestCase:
     |  
     |  failureException = <class 'AssertionError'>
     |      Assertion failed.
     |  
     |  longMessage = True
     |  
     |  maxDiff = 640


```


## mr_utils.tests.recon.test_planet

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/recon/test_planet.py)

```
NAME
    mr_utils.tests.recon.test_planet - Tests for python PLANET implementation.

CLASSES
    unittest.case.TestCase(builtins.object)
        TestPLANET
    
    class TestPLANET(unittest.case.TestCase)
     |  PLANET sanity checks.
     |  
     |  Method resolution order:
     |      TestPLANET
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_ellipse_fit(self)
     |      Make sure we can fit an ellipse using complex ssfp data.
     |  
     |  test_no_noise_case(self)
     |      Make sure we perform in ideal conditions.
     |  
     |  test_requires_6_phase_cycles(self)
     |      Make sure we can't continue without 6 phase-cycles.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from unittest.case.TestCase:
     |  
     |  __call__(self, *args, **kwds)
     |      Call self as a function.
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, methodName='runTest')
     |      Create an instance of the class that will use the named test
     |      method when executed. Raises a ValueError if the instance does
     |      not have a method with the specified name.
     |  
     |  __repr__(self)
     |      Return repr(self).
     |  
     |  __str__(self)
     |      Return str(self).
     |  
     |  addCleanup(self, function, *args, **kwargs)
     |      Add a function, with arguments, to be called when the test is
     |      completed. Functions added are called on a LIFO basis and are
     |      called after tearDown on test failure or success.
     |      
     |      Cleanup items are called even if setUp fails (unlike tearDown).
     |  
     |  addTypeEqualityFunc(self, typeobj, function)
     |      Add a type specific assertEqual style function to compare a type.
     |      
     |      This method is for use by TestCase subclasses that need to register
     |      their own type equality functions to provide nicer error messages.
     |      
     |      Args:
     |          typeobj: The data type to call this function on when both values
     |                  are of the same type in assertEqual().
     |          function: The callable taking two arguments and an optional
     |                  msg= argument that raises self.failureException with a
     |                  useful error message when the two arguments are not equal.
     |  
     |  assertAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are unequal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is more than the given
     |      delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      If the two objects compare equal then they will automatically
     |      compare almost equal.
     |  
     |  assertAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertCountEqual(self, first, second, msg=None)
     |      An unordered sequence comparison asserting that the same elements,
     |      regardless of order.  If the same element occurs more than once,
     |      it verifies that the elements occur the same number of times.
     |      
     |          self.assertEqual(Counter(list(first)),
     |                           Counter(list(second)))
     |      
     |       Example:
     |          - [0, 1, 1] and [1, 0, 1] compare equal.
     |          - [0, 0, 1] and [0, 1] compare unequal.
     |  
     |  assertDictContainsSubset(self, subset, dictionary, msg=None)
     |      Checks whether dictionary is a superset of subset.
     |  
     |  assertDictEqual(self, d1, d2, msg=None)
     |  
     |  assertEqual(self, first, second, msg=None)
     |      Fail if the two objects are unequal as determined by the '=='
     |      operator.
     |  
     |  assertEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertFalse(self, expr, msg=None)
     |      Check that the expression is false.
     |  
     |  assertGreater(self, a, b, msg=None)
     |      Just like self.assertTrue(a > b), but with a nicer default message.
     |  
     |  assertGreaterEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a >= b), but with a nicer default message.
     |  
     |  assertIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a in b), but with a nicer default message.
     |  
     |  assertIs(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is b), but with a nicer default message.
     |  
     |  assertIsInstance(self, obj, cls, msg=None)
     |      Same as self.assertTrue(isinstance(obj, cls)), with a nicer
     |      default message.
     |  
     |  assertIsNone(self, obj, msg=None)
     |      Same as self.assertTrue(obj is None), with a nicer default message.
     |  
     |  assertIsNot(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is not b), but with a nicer default message.
     |  
     |  assertIsNotNone(self, obj, msg=None)
     |      Included for symmetry with assertIsNone.
     |  
     |  assertLess(self, a, b, msg=None)
     |      Just like self.assertTrue(a < b), but with a nicer default message.
     |  
     |  assertLessEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a <= b), but with a nicer default message.
     |  
     |  assertListEqual(self, list1, list2, msg=None)
     |      A list-specific equality assertion.
     |      
     |      Args:
     |          list1: The first list to compare.
     |          list2: The second list to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertLogs(self, logger=None, level=None)
     |      Fail unless a log message of level *level* or higher is emitted
     |      on *logger_name* or its children.  If omitted, *level* defaults to
     |      INFO and *logger* defaults to the root logger.
     |      
     |      This method must be used as a context manager, and will yield
     |      a recording object with two attributes: `output` and `records`.
     |      At the end of the context manager, the `output` attribute will
     |      be a list of the matching formatted log messages and the
     |      `records` attribute will be a list of the corresponding LogRecord
     |      objects.
     |      
     |      Example::
     |      
     |          with self.assertLogs('foo', level='INFO') as cm:
     |              logging.getLogger('foo').info('first message')
     |              logging.getLogger('foo.bar').error('second message')
     |          self.assertEqual(cm.output, ['INFO:foo:first message',
     |                                       'ERROR:foo.bar:second message'])
     |  
     |  assertMultiLineEqual(self, first, second, msg=None)
     |      Assert that two multi-line strings are equal.
     |  
     |  assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are equal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is less than the given delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      Objects that are equal automatically fail.
     |  
     |  assertNotAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotEqual(self, first, second, msg=None)
     |      Fail if the two objects are equal as determined by the '!='
     |      operator.
     |  
     |  assertNotEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a not in b), but with a nicer default message.
     |  
     |  assertNotIsInstance(self, obj, cls, msg=None)
     |      Included for symmetry with assertIsInstance.
     |  
     |  assertNotRegex(self, text, unexpected_regex, msg=None)
     |      Fail the test if the text matches the regular expression.
     |  
     |  assertNotRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertRaises(self, expected_exception, *args, **kwargs)
     |      Fail unless an exception of class expected_exception is raised
     |      by the callable when invoked with specified positional and
     |      keyword arguments. If a different type of exception is
     |      raised, it will not be caught, and the test case will be
     |      deemed to have suffered an error, exactly as for an
     |      unexpected exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertRaises(SomeException):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertRaises
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the exception as
     |      the 'exception' attribute. This allows you to inspect the
     |      exception after the assertion::
     |      
     |          with self.assertRaises(SomeException) as cm:
     |              do_something()
     |          the_exception = cm.exception
     |          self.assertEqual(the_exception.error_code, 3)
     |  
     |  assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs)
     |      Asserts that the message in a raised exception matches a regex.
     |      
     |      Args:
     |          expected_exception: Exception class expected to be raised.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertRaisesRegex is used as a context manager.
     |  
     |  assertRaisesRegexp = deprecated_func(*args, **kwargs)
     |  
     |  assertRegex(self, text, expected_regex, msg=None)
     |      Fail the test unless the text matches the regular expression.
     |  
     |  assertRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None)
     |      An equality assertion for ordered sequences (like lists and tuples).
     |      
     |      For the purposes of this function, a valid ordered sequence type is one
     |      which can be indexed, has a length, and has an equality operator.
     |      
     |      Args:
     |          seq1: The first sequence to compare.
     |          seq2: The second sequence to compare.
     |          seq_type: The expected datatype of the sequences, or None if no
     |                  datatype should be enforced.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertSetEqual(self, set1, set2, msg=None)
     |      A set-specific equality assertion.
     |      
     |      Args:
     |          set1: The first set to compare.
     |          set2: The second set to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |      
     |      assertSetEqual uses ducktyping to support different types of sets, and
     |      is optimized for sets specifically (parameters must support a
     |      difference method).
     |  
     |  assertTrue(self, expr, msg=None)
     |      Check that the expression is true.
     |  
     |  assertTupleEqual(self, tuple1, tuple2, msg=None)
     |      A tuple-specific equality assertion.
     |      
     |      Args:
     |          tuple1: The first tuple to compare.
     |          tuple2: The second tuple to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertWarns(self, expected_warning, *args, **kwargs)
     |      Fail unless a warning of class warnClass is triggered
     |      by the callable when invoked with specified positional and
     |      keyword arguments.  If a different type of warning is
     |      triggered, it will not be handled: depending on the other
     |      warning filtering rules in effect, it might be silenced, printed
     |      out, or raised as an exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertWarns(SomeWarning):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertWarns
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the first matching
     |      warning as the 'warning' attribute; similarly, the 'filename'
     |      and 'lineno' attributes give you information about the line
     |      of Python code from which the warning was triggered.
     |      This allows you to inspect the warning after the assertion::
     |      
     |          with self.assertWarns(SomeWarning) as cm:
     |              do_something()
     |          the_warning = cm.warning
     |          self.assertEqual(the_warning.some_attribute, 147)
     |  
     |  assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs)
     |      Asserts that the message in a triggered warning matches a regexp.
     |      Basic functioning is similar to assertWarns() with the addition
     |      that only warnings whose messages also match the regular expression
     |      are considered successful matches.
     |      
     |      Args:
     |          expected_warning: Warning class expected to be triggered.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertWarnsRegex is used as a context manager.
     |  
     |  assert_ = deprecated_func(*args, **kwargs)
     |  
     |  countTestCases(self)
     |  
     |  debug(self)
     |      Run the test without collecting errors in a TestResult
     |  
     |  defaultTestResult(self)
     |  
     |  doCleanups(self)
     |      Execute all cleanup functions. Normally called for you after
     |      tearDown.
     |  
     |  fail(self, msg=None)
     |      Fail immediately, with the given message.
     |  
     |  failIf = deprecated_func(*args, **kwargs)
     |  
     |  failIfAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failIfEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnless = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessRaises = deprecated_func(*args, **kwargs)
     |  
     |  id(self)
     |  
     |  run(self, result=None)
     |  
     |  shortDescription(self)
     |      Returns a one-line description of the test, or None if no
     |      description has been provided.
     |      
     |      The default implementation of this method returns the first line of
     |      the specified test method's docstring.
     |  
     |  skipTest(self, reason)
     |      Skip this test.
     |  
     |  subTest(self, msg=<object object at 0x7f267fce1280>, **params)
     |      Return a context manager that will return the enclosed block
     |      of code in a subtest identified by the optional message and
     |      keyword parameters.  A failure in the subtest marks the test
     |      case as failed but resumes execution at the end of the enclosed
     |      block, allowing further test code to be executed.
     |  
     |  tearDown(self)
     |      Hook method for deconstructing the test fixture after testing it.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from unittest.case.TestCase:
     |  
     |  setUpClass() from builtins.type
     |      Hook method for setting up class fixture before running tests in the class.
     |  
     |  tearDownClass() from builtins.type
     |      Hook method for deconstructing the class fixture after running all tests in the class.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from unittest.case.TestCase:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from unittest.case.TestCase:
     |  
     |  failureException = <class 'AssertionError'>
     |      Assertion failed.
     |  
     |  longMessage = True
     |  
     |  maxDiff = 640


```


## mr_utils.tests.recon.test_rudin_osher_fatemi

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/recon/test_rudin_osher_fatemi.py)

```
NAME
    mr_utils.tests.recon.test_rudin_osher_fatemi

CLASSES
    unittest.case.TestCase(builtins.object)
        RudinEtAlTestCase
    
    class RudinEtAlTestCase(unittest.case.TestCase)
     |  A class whose instances are single test cases.
     |  
     |  By default, the test code itself should be placed in a method named
     |  'runTest'.
     |  
     |  If the fixture may be used for many test cases, create as
     |  many test methods as are needed. When instantiating such a TestCase
     |  subclass, specify in the constructor arguments the name of the test method
     |  that the instance is to execute.
     |  
     |  Test authors should subclass TestCase for their own tests. Construction
     |  and deconstruction of the test's environment ('fixture') can be
     |  implemented by overriding the 'setUp' and 'tearDown' methods respectively.
     |  
     |  If it is necessary to override the __init__ method, the base class
     |  __init__ method must always be called. It is important that subclasses
     |  should not change the signature of their __init__ method, since instances
     |  of the classes are instantiated automatically by parts of the framework
     |  in order to be run.
     |  
     |  When subclassing TestCase, you can set these attributes:
     |  * failureException: determines which exception will be raised when
     |      the instance's assertion methods fail; test methods raising this
     |      exception will be deemed to have 'failed' rather than 'errored'.
     |  * longMessage: determines whether long messages (including repr of
     |      objects used in assert methods) will be printed on failure in *addition*
     |      to any explicit message passed.
     |  * maxDiff: sets the maximum length of a diff in failure messages
     |      by assert methods using difflib. It is looked up as an instance
     |      attribute so can be configured by individual tests if required.
     |  
     |  Method resolution order:
     |      RudinEtAlTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_algo_for_loop(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from unittest.case.TestCase:
     |  
     |  __call__(self, *args, **kwds)
     |      Call self as a function.
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, methodName='runTest')
     |      Create an instance of the class that will use the named test
     |      method when executed. Raises a ValueError if the instance does
     |      not have a method with the specified name.
     |  
     |  __repr__(self)
     |      Return repr(self).
     |  
     |  __str__(self)
     |      Return str(self).
     |  
     |  addCleanup(self, function, *args, **kwargs)
     |      Add a function, with arguments, to be called when the test is
     |      completed. Functions added are called on a LIFO basis and are
     |      called after tearDown on test failure or success.
     |      
     |      Cleanup items are called even if setUp fails (unlike tearDown).
     |  
     |  addTypeEqualityFunc(self, typeobj, function)
     |      Add a type specific assertEqual style function to compare a type.
     |      
     |      This method is for use by TestCase subclasses that need to register
     |      their own type equality functions to provide nicer error messages.
     |      
     |      Args:
     |          typeobj: The data type to call this function on when both values
     |                  are of the same type in assertEqual().
     |          function: The callable taking two arguments and an optional
     |                  msg= argument that raises self.failureException with a
     |                  useful error message when the two arguments are not equal.
     |  
     |  assertAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are unequal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is more than the given
     |      delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      If the two objects compare equal then they will automatically
     |      compare almost equal.
     |  
     |  assertAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertCountEqual(self, first, second, msg=None)
     |      An unordered sequence comparison asserting that the same elements,
     |      regardless of order.  If the same element occurs more than once,
     |      it verifies that the elements occur the same number of times.
     |      
     |          self.assertEqual(Counter(list(first)),
     |                           Counter(list(second)))
     |      
     |       Example:
     |          - [0, 1, 1] and [1, 0, 1] compare equal.
     |          - [0, 0, 1] and [0, 1] compare unequal.
     |  
     |  assertDictContainsSubset(self, subset, dictionary, msg=None)
     |      Checks whether dictionary is a superset of subset.
     |  
     |  assertDictEqual(self, d1, d2, msg=None)
     |  
     |  assertEqual(self, first, second, msg=None)
     |      Fail if the two objects are unequal as determined by the '=='
     |      operator.
     |  
     |  assertEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertFalse(self, expr, msg=None)
     |      Check that the expression is false.
     |  
     |  assertGreater(self, a, b, msg=None)
     |      Just like self.assertTrue(a > b), but with a nicer default message.
     |  
     |  assertGreaterEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a >= b), but with a nicer default message.
     |  
     |  assertIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a in b), but with a nicer default message.
     |  
     |  assertIs(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is b), but with a nicer default message.
     |  
     |  assertIsInstance(self, obj, cls, msg=None)
     |      Same as self.assertTrue(isinstance(obj, cls)), with a nicer
     |      default message.
     |  
     |  assertIsNone(self, obj, msg=None)
     |      Same as self.assertTrue(obj is None), with a nicer default message.
     |  
     |  assertIsNot(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is not b), but with a nicer default message.
     |  
     |  assertIsNotNone(self, obj, msg=None)
     |      Included for symmetry with assertIsNone.
     |  
     |  assertLess(self, a, b, msg=None)
     |      Just like self.assertTrue(a < b), but with a nicer default message.
     |  
     |  assertLessEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a <= b), but with a nicer default message.
     |  
     |  assertListEqual(self, list1, list2, msg=None)
     |      A list-specific equality assertion.
     |      
     |      Args:
     |          list1: The first list to compare.
     |          list2: The second list to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertLogs(self, logger=None, level=None)
     |      Fail unless a log message of level *level* or higher is emitted
     |      on *logger_name* or its children.  If omitted, *level* defaults to
     |      INFO and *logger* defaults to the root logger.
     |      
     |      This method must be used as a context manager, and will yield
     |      a recording object with two attributes: `output` and `records`.
     |      At the end of the context manager, the `output` attribute will
     |      be a list of the matching formatted log messages and the
     |      `records` attribute will be a list of the corresponding LogRecord
     |      objects.
     |      
     |      Example::
     |      
     |          with self.assertLogs('foo', level='INFO') as cm:
     |              logging.getLogger('foo').info('first message')
     |              logging.getLogger('foo.bar').error('second message')
     |          self.assertEqual(cm.output, ['INFO:foo:first message',
     |                                       'ERROR:foo.bar:second message'])
     |  
     |  assertMultiLineEqual(self, first, second, msg=None)
     |      Assert that two multi-line strings are equal.
     |  
     |  assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are equal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is less than the given delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      Objects that are equal automatically fail.
     |  
     |  assertNotAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotEqual(self, first, second, msg=None)
     |      Fail if the two objects are equal as determined by the '!='
     |      operator.
     |  
     |  assertNotEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a not in b), but with a nicer default message.
     |  
     |  assertNotIsInstance(self, obj, cls, msg=None)
     |      Included for symmetry with assertIsInstance.
     |  
     |  assertNotRegex(self, text, unexpected_regex, msg=None)
     |      Fail the test if the text matches the regular expression.
     |  
     |  assertNotRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertRaises(self, expected_exception, *args, **kwargs)
     |      Fail unless an exception of class expected_exception is raised
     |      by the callable when invoked with specified positional and
     |      keyword arguments. If a different type of exception is
     |      raised, it will not be caught, and the test case will be
     |      deemed to have suffered an error, exactly as for an
     |      unexpected exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertRaises(SomeException):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertRaises
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the exception as
     |      the 'exception' attribute. This allows you to inspect the
     |      exception after the assertion::
     |      
     |          with self.assertRaises(SomeException) as cm:
     |              do_something()
     |          the_exception = cm.exception
     |          self.assertEqual(the_exception.error_code, 3)
     |  
     |  assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs)
     |      Asserts that the message in a raised exception matches a regex.
     |      
     |      Args:
     |          expected_exception: Exception class expected to be raised.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertRaisesRegex is used as a context manager.
     |  
     |  assertRaisesRegexp = deprecated_func(*args, **kwargs)
     |  
     |  assertRegex(self, text, expected_regex, msg=None)
     |      Fail the test unless the text matches the regular expression.
     |  
     |  assertRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None)
     |      An equality assertion for ordered sequences (like lists and tuples).
     |      
     |      For the purposes of this function, a valid ordered sequence type is one
     |      which can be indexed, has a length, and has an equality operator.
     |      
     |      Args:
     |          seq1: The first sequence to compare.
     |          seq2: The second sequence to compare.
     |          seq_type: The expected datatype of the sequences, or None if no
     |                  datatype should be enforced.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertSetEqual(self, set1, set2, msg=None)
     |      A set-specific equality assertion.
     |      
     |      Args:
     |          set1: The first set to compare.
     |          set2: The second set to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |      
     |      assertSetEqual uses ducktyping to support different types of sets, and
     |      is optimized for sets specifically (parameters must support a
     |      difference method).
     |  
     |  assertTrue(self, expr, msg=None)
     |      Check that the expression is true.
     |  
     |  assertTupleEqual(self, tuple1, tuple2, msg=None)
     |      A tuple-specific equality assertion.
     |      
     |      Args:
     |          tuple1: The first tuple to compare.
     |          tuple2: The second tuple to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertWarns(self, expected_warning, *args, **kwargs)
     |      Fail unless a warning of class warnClass is triggered
     |      by the callable when invoked with specified positional and
     |      keyword arguments.  If a different type of warning is
     |      triggered, it will not be handled: depending on the other
     |      warning filtering rules in effect, it might be silenced, printed
     |      out, or raised as an exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertWarns(SomeWarning):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertWarns
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the first matching
     |      warning as the 'warning' attribute; similarly, the 'filename'
     |      and 'lineno' attributes give you information about the line
     |      of Python code from which the warning was triggered.
     |      This allows you to inspect the warning after the assertion::
     |      
     |          with self.assertWarns(SomeWarning) as cm:
     |              do_something()
     |          the_warning = cm.warning
     |          self.assertEqual(the_warning.some_attribute, 147)
     |  
     |  assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs)
     |      Asserts that the message in a triggered warning matches a regexp.
     |      Basic functioning is similar to assertWarns() with the addition
     |      that only warnings whose messages also match the regular expression
     |      are considered successful matches.
     |      
     |      Args:
     |          expected_warning: Warning class expected to be triggered.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertWarnsRegex is used as a context manager.
     |  
     |  assert_ = deprecated_func(*args, **kwargs)
     |  
     |  countTestCases(self)
     |  
     |  debug(self)
     |      Run the test without collecting errors in a TestResult
     |  
     |  defaultTestResult(self)
     |  
     |  doCleanups(self)
     |      Execute all cleanup functions. Normally called for you after
     |      tearDown.
     |  
     |  fail(self, msg=None)
     |      Fail immediately, with the given message.
     |  
     |  failIf = deprecated_func(*args, **kwargs)
     |  
     |  failIfAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failIfEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnless = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessRaises = deprecated_func(*args, **kwargs)
     |  
     |  id(self)
     |  
     |  run(self, result=None)
     |  
     |  shortDescription(self)
     |      Returns a one-line description of the test, or None if no
     |      description has been provided.
     |      
     |      The default implementation of this method returns the first line of
     |      the specified test method's docstring.
     |  
     |  skipTest(self, reason)
     |      Skip this test.
     |  
     |  subTest(self, msg=<object object at 0x7f267fce1280>, **params)
     |      Return a context manager that will return the enclosed block
     |      of code in a subtest identified by the optional message and
     |      keyword parameters.  A failure in the subtest marks the test
     |      case as failed but resumes execution at the end of the enclosed
     |      block, allowing further test code to be executed.
     |  
     |  tearDown(self)
     |      Hook method for deconstructing the test fixture after testing it.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from unittest.case.TestCase:
     |  
     |  setUpClass() from builtins.type
     |      Hook method for setting up class fixture before running tests in the class.
     |  
     |  tearDownClass() from builtins.type
     |      Hook method for deconstructing the class fixture after running all tests in the class.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from unittest.case.TestCase:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from unittest.case.TestCase:
     |  
     |  failureException = <class 'AssertionError'>
     |      Assertion failed.
     |  
     |  longMessage = True
     |  
     |  maxDiff = 640


```


## mr_utils.tests.recon.test_scr_reordering

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/recon/test_scr_reordering.py)

```
NAME
    mr_utils.tests.recon.test_scr_reordering

CLASSES
    unittest.case.TestCase(builtins.object)
        SCRReorderingTestCase
    
    class SCRReorderingTestCase(unittest.case.TestCase)
     |  A class whose instances are single test cases.
     |  
     |  By default, the test code itself should be placed in a method named
     |  'runTest'.
     |  
     |  If the fixture may be used for many test cases, create as
     |  many test methods as are needed. When instantiating such a TestCase
     |  subclass, specify in the constructor arguments the name of the test method
     |  that the instance is to execute.
     |  
     |  Test authors should subclass TestCase for their own tests. Construction
     |  and deconstruction of the test's environment ('fixture') can be
     |  implemented by overriding the 'setUp' and 'tearDown' methods respectively.
     |  
     |  If it is necessary to override the __init__ method, the base class
     |  __init__ method must always be called. It is important that subclasses
     |  should not change the signature of their __init__ method, since instances
     |  of the classes are instantiated automatically by parts of the framework
     |  in order to be run.
     |  
     |  When subclassing TestCase, you can set these attributes:
     |  * failureException: determines which exception will be raised when
     |      the instance's assertion methods fail; test methods raising this
     |      exception will be deemed to have 'failed' rather than 'errored'.
     |  * longMessage: determines whether long messages (including repr of
     |      objects used in assert methods) will be printed on failure in *addition*
     |      to any explicit message passed.
     |  * maxDiff: sets the maximum length of a diff in failure messages
     |      by assert methods using difflib. It is looked up as an instance
     |      attribute so can be configured by individual tests if required.
     |  
     |  Method resolution order:
     |      SCRReorderingTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_TVG_re_order(self)
     |  
     |  test_TV_term_update(self)
     |  
     |  test_scr_reordering_adluru_fidelity_update(self)
     |  
     |  test_scr_reordering_adluru_true_prior_100_iter(self)
     |  
     |  test_scr_reordering_adluru_true_prior_10_iter(self)
     |  
     |  test_scr_reordering_adluru_true_prior_1_iter(self)
     |  
     |  test_scr_reordering_adluru_true_prior_2_iter(self)
     |  
     |  test_scr_reordering_adluru_true_prior_50_iter(self)
     |  
     |  test_sort_real_imag_parts_space(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from unittest.case.TestCase:
     |  
     |  __call__(self, *args, **kwds)
     |      Call self as a function.
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, methodName='runTest')
     |      Create an instance of the class that will use the named test
     |      method when executed. Raises a ValueError if the instance does
     |      not have a method with the specified name.
     |  
     |  __repr__(self)
     |      Return repr(self).
     |  
     |  __str__(self)
     |      Return str(self).
     |  
     |  addCleanup(self, function, *args, **kwargs)
     |      Add a function, with arguments, to be called when the test is
     |      completed. Functions added are called on a LIFO basis and are
     |      called after tearDown on test failure or success.
     |      
     |      Cleanup items are called even if setUp fails (unlike tearDown).
     |  
     |  addTypeEqualityFunc(self, typeobj, function)
     |      Add a type specific assertEqual style function to compare a type.
     |      
     |      This method is for use by TestCase subclasses that need to register
     |      their own type equality functions to provide nicer error messages.
     |      
     |      Args:
     |          typeobj: The data type to call this function on when both values
     |                  are of the same type in assertEqual().
     |          function: The callable taking two arguments and an optional
     |                  msg= argument that raises self.failureException with a
     |                  useful error message when the two arguments are not equal.
     |  
     |  assertAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are unequal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is more than the given
     |      delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      If the two objects compare equal then they will automatically
     |      compare almost equal.
     |  
     |  assertAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertCountEqual(self, first, second, msg=None)
     |      An unordered sequence comparison asserting that the same elements,
     |      regardless of order.  If the same element occurs more than once,
     |      it verifies that the elements occur the same number of times.
     |      
     |          self.assertEqual(Counter(list(first)),
     |                           Counter(list(second)))
     |      
     |       Example:
     |          - [0, 1, 1] and [1, 0, 1] compare equal.
     |          - [0, 0, 1] and [0, 1] compare unequal.
     |  
     |  assertDictContainsSubset(self, subset, dictionary, msg=None)
     |      Checks whether dictionary is a superset of subset.
     |  
     |  assertDictEqual(self, d1, d2, msg=None)
     |  
     |  assertEqual(self, first, second, msg=None)
     |      Fail if the two objects are unequal as determined by the '=='
     |      operator.
     |  
     |  assertEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertFalse(self, expr, msg=None)
     |      Check that the expression is false.
     |  
     |  assertGreater(self, a, b, msg=None)
     |      Just like self.assertTrue(a > b), but with a nicer default message.
     |  
     |  assertGreaterEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a >= b), but with a nicer default message.
     |  
     |  assertIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a in b), but with a nicer default message.
     |  
     |  assertIs(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is b), but with a nicer default message.
     |  
     |  assertIsInstance(self, obj, cls, msg=None)
     |      Same as self.assertTrue(isinstance(obj, cls)), with a nicer
     |      default message.
     |  
     |  assertIsNone(self, obj, msg=None)
     |      Same as self.assertTrue(obj is None), with a nicer default message.
     |  
     |  assertIsNot(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is not b), but with a nicer default message.
     |  
     |  assertIsNotNone(self, obj, msg=None)
     |      Included for symmetry with assertIsNone.
     |  
     |  assertLess(self, a, b, msg=None)
     |      Just like self.assertTrue(a < b), but with a nicer default message.
     |  
     |  assertLessEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a <= b), but with a nicer default message.
     |  
     |  assertListEqual(self, list1, list2, msg=None)
     |      A list-specific equality assertion.
     |      
     |      Args:
     |          list1: The first list to compare.
     |          list2: The second list to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertLogs(self, logger=None, level=None)
     |      Fail unless a log message of level *level* or higher is emitted
     |      on *logger_name* or its children.  If omitted, *level* defaults to
     |      INFO and *logger* defaults to the root logger.
     |      
     |      This method must be used as a context manager, and will yield
     |      a recording object with two attributes: `output` and `records`.
     |      At the end of the context manager, the `output` attribute will
     |      be a list of the matching formatted log messages and the
     |      `records` attribute will be a list of the corresponding LogRecord
     |      objects.
     |      
     |      Example::
     |      
     |          with self.assertLogs('foo', level='INFO') as cm:
     |              logging.getLogger('foo').info('first message')
     |              logging.getLogger('foo.bar').error('second message')
     |          self.assertEqual(cm.output, ['INFO:foo:first message',
     |                                       'ERROR:foo.bar:second message'])
     |  
     |  assertMultiLineEqual(self, first, second, msg=None)
     |      Assert that two multi-line strings are equal.
     |  
     |  assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are equal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is less than the given delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      Objects that are equal automatically fail.
     |  
     |  assertNotAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotEqual(self, first, second, msg=None)
     |      Fail if the two objects are equal as determined by the '!='
     |      operator.
     |  
     |  assertNotEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a not in b), but with a nicer default message.
     |  
     |  assertNotIsInstance(self, obj, cls, msg=None)
     |      Included for symmetry with assertIsInstance.
     |  
     |  assertNotRegex(self, text, unexpected_regex, msg=None)
     |      Fail the test if the text matches the regular expression.
     |  
     |  assertNotRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertRaises(self, expected_exception, *args, **kwargs)
     |      Fail unless an exception of class expected_exception is raised
     |      by the callable when invoked with specified positional and
     |      keyword arguments. If a different type of exception is
     |      raised, it will not be caught, and the test case will be
     |      deemed to have suffered an error, exactly as for an
     |      unexpected exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertRaises(SomeException):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertRaises
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the exception as
     |      the 'exception' attribute. This allows you to inspect the
     |      exception after the assertion::
     |      
     |          with self.assertRaises(SomeException) as cm:
     |              do_something()
     |          the_exception = cm.exception
     |          self.assertEqual(the_exception.error_code, 3)
     |  
     |  assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs)
     |      Asserts that the message in a raised exception matches a regex.
     |      
     |      Args:
     |          expected_exception: Exception class expected to be raised.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertRaisesRegex is used as a context manager.
     |  
     |  assertRaisesRegexp = deprecated_func(*args, **kwargs)
     |  
     |  assertRegex(self, text, expected_regex, msg=None)
     |      Fail the test unless the text matches the regular expression.
     |  
     |  assertRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None)
     |      An equality assertion for ordered sequences (like lists and tuples).
     |      
     |      For the purposes of this function, a valid ordered sequence type is one
     |      which can be indexed, has a length, and has an equality operator.
     |      
     |      Args:
     |          seq1: The first sequence to compare.
     |          seq2: The second sequence to compare.
     |          seq_type: The expected datatype of the sequences, or None if no
     |                  datatype should be enforced.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertSetEqual(self, set1, set2, msg=None)
     |      A set-specific equality assertion.
     |      
     |      Args:
     |          set1: The first set to compare.
     |          set2: The second set to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |      
     |      assertSetEqual uses ducktyping to support different types of sets, and
     |      is optimized for sets specifically (parameters must support a
     |      difference method).
     |  
     |  assertTrue(self, expr, msg=None)
     |      Check that the expression is true.
     |  
     |  assertTupleEqual(self, tuple1, tuple2, msg=None)
     |      A tuple-specific equality assertion.
     |      
     |      Args:
     |          tuple1: The first tuple to compare.
     |          tuple2: The second tuple to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertWarns(self, expected_warning, *args, **kwargs)
     |      Fail unless a warning of class warnClass is triggered
     |      by the callable when invoked with specified positional and
     |      keyword arguments.  If a different type of warning is
     |      triggered, it will not be handled: depending on the other
     |      warning filtering rules in effect, it might be silenced, printed
     |      out, or raised as an exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertWarns(SomeWarning):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertWarns
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the first matching
     |      warning as the 'warning' attribute; similarly, the 'filename'
     |      and 'lineno' attributes give you information about the line
     |      of Python code from which the warning was triggered.
     |      This allows you to inspect the warning after the assertion::
     |      
     |          with self.assertWarns(SomeWarning) as cm:
     |              do_something()
     |          the_warning = cm.warning
     |          self.assertEqual(the_warning.some_attribute, 147)
     |  
     |  assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs)
     |      Asserts that the message in a triggered warning matches a regexp.
     |      Basic functioning is similar to assertWarns() with the addition
     |      that only warnings whose messages also match the regular expression
     |      are considered successful matches.
     |      
     |      Args:
     |          expected_warning: Warning class expected to be triggered.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertWarnsRegex is used as a context manager.
     |  
     |  assert_ = deprecated_func(*args, **kwargs)
     |  
     |  countTestCases(self)
     |  
     |  debug(self)
     |      Run the test without collecting errors in a TestResult
     |  
     |  defaultTestResult(self)
     |  
     |  doCleanups(self)
     |      Execute all cleanup functions. Normally called for you after
     |      tearDown.
     |  
     |  fail(self, msg=None)
     |      Fail immediately, with the given message.
     |  
     |  failIf = deprecated_func(*args, **kwargs)
     |  
     |  failIfAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failIfEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnless = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessRaises = deprecated_func(*args, **kwargs)
     |  
     |  id(self)
     |  
     |  run(self, result=None)
     |  
     |  shortDescription(self)
     |      Returns a one-line description of the test, or None if no
     |      description has been provided.
     |      
     |      The default implementation of this method returns the first line of
     |      the specified test method's docstring.
     |  
     |  skipTest(self, reason)
     |      Skip this test.
     |  
     |  subTest(self, msg=<object object at 0x7f267fce1280>, **params)
     |      Return a context manager that will return the enclosed block
     |      of code in a subtest identified by the optional message and
     |      keyword parameters.  A failure in the subtest marks the test
     |      case as failed but resumes execution at the end of the enclosed
     |      block, allowing further test code to be executed.
     |  
     |  tearDown(self)
     |      Hook method for deconstructing the test fixture after testing it.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from unittest.case.TestCase:
     |  
     |  setUpClass() from builtins.type
     |      Hook method for setting up class fixture before running tests in the class.
     |  
     |  tearDownClass() from builtins.type
     |      Hook method for deconstructing the class fixture after running all tests in the class.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from unittest.case.TestCase:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from unittest.case.TestCase:
     |  
     |  failureException = <class 'AssertionError'>
     |      Assertion failed.
     |  
     |  longMessage = True
     |  
     |  maxDiff = 640


```


## mr_utils.tests.recon.test_scr_reordering_one_d

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/recon/test_scr_reordering_one_d.py)

```
NAME
    mr_utils.tests.recon.test_scr_reordering_one_d

CLASSES
    unittest.case.TestCase(builtins.object)
        SCRReordering1D
    
    class SCRReordering1D(unittest.case.TestCase)
     |  A class whose instances are single test cases.
     |  
     |  By default, the test code itself should be placed in a method named
     |  'runTest'.
     |  
     |  If the fixture may be used for many test cases, create as
     |  many test methods as are needed. When instantiating such a TestCase
     |  subclass, specify in the constructor arguments the name of the test method
     |  that the instance is to execute.
     |  
     |  Test authors should subclass TestCase for their own tests. Construction
     |  and deconstruction of the test's environment ('fixture') can be
     |  implemented by overriding the 'setUp' and 'tearDown' methods respectively.
     |  
     |  If it is necessary to override the __init__ method, the base class
     |  __init__ method must always be called. It is important that subclasses
     |  should not change the signature of their __init__ method, since instances
     |  of the classes are instantiated automatically by parts of the framework
     |  in order to be run.
     |  
     |  When subclassing TestCase, you can set these attributes:
     |  * failureException: determines which exception will be raised when
     |      the instance's assertion methods fail; test methods raising this
     |      exception will be deemed to have 'failed' rather than 'errored'.
     |  * longMessage: determines whether long messages (including repr of
     |      objects used in assert methods) will be printed on failure in *addition*
     |      to any explicit message passed.
     |  * maxDiff: sets the maximum length of a diff in failure messages
     |      by assert methods using difflib. It is looked up as an instance
     |      attribute so can be configured by individual tests if required.
     |  
     |  Method resolution order:
     |      SCRReordering1D
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_compare_lasso(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from unittest.case.TestCase:
     |  
     |  __call__(self, *args, **kwds)
     |      Call self as a function.
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, methodName='runTest')
     |      Create an instance of the class that will use the named test
     |      method when executed. Raises a ValueError if the instance does
     |      not have a method with the specified name.
     |  
     |  __repr__(self)
     |      Return repr(self).
     |  
     |  __str__(self)
     |      Return str(self).
     |  
     |  addCleanup(self, function, *args, **kwargs)
     |      Add a function, with arguments, to be called when the test is
     |      completed. Functions added are called on a LIFO basis and are
     |      called after tearDown on test failure or success.
     |      
     |      Cleanup items are called even if setUp fails (unlike tearDown).
     |  
     |  addTypeEqualityFunc(self, typeobj, function)
     |      Add a type specific assertEqual style function to compare a type.
     |      
     |      This method is for use by TestCase subclasses that need to register
     |      their own type equality functions to provide nicer error messages.
     |      
     |      Args:
     |          typeobj: The data type to call this function on when both values
     |                  are of the same type in assertEqual().
     |          function: The callable taking two arguments and an optional
     |                  msg= argument that raises self.failureException with a
     |                  useful error message when the two arguments are not equal.
     |  
     |  assertAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are unequal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is more than the given
     |      delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      If the two objects compare equal then they will automatically
     |      compare almost equal.
     |  
     |  assertAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertCountEqual(self, first, second, msg=None)
     |      An unordered sequence comparison asserting that the same elements,
     |      regardless of order.  If the same element occurs more than once,
     |      it verifies that the elements occur the same number of times.
     |      
     |          self.assertEqual(Counter(list(first)),
     |                           Counter(list(second)))
     |      
     |       Example:
     |          - [0, 1, 1] and [1, 0, 1] compare equal.
     |          - [0, 0, 1] and [0, 1] compare unequal.
     |  
     |  assertDictContainsSubset(self, subset, dictionary, msg=None)
     |      Checks whether dictionary is a superset of subset.
     |  
     |  assertDictEqual(self, d1, d2, msg=None)
     |  
     |  assertEqual(self, first, second, msg=None)
     |      Fail if the two objects are unequal as determined by the '=='
     |      operator.
     |  
     |  assertEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertFalse(self, expr, msg=None)
     |      Check that the expression is false.
     |  
     |  assertGreater(self, a, b, msg=None)
     |      Just like self.assertTrue(a > b), but with a nicer default message.
     |  
     |  assertGreaterEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a >= b), but with a nicer default message.
     |  
     |  assertIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a in b), but with a nicer default message.
     |  
     |  assertIs(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is b), but with a nicer default message.
     |  
     |  assertIsInstance(self, obj, cls, msg=None)
     |      Same as self.assertTrue(isinstance(obj, cls)), with a nicer
     |      default message.
     |  
     |  assertIsNone(self, obj, msg=None)
     |      Same as self.assertTrue(obj is None), with a nicer default message.
     |  
     |  assertIsNot(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is not b), but with a nicer default message.
     |  
     |  assertIsNotNone(self, obj, msg=None)
     |      Included for symmetry with assertIsNone.
     |  
     |  assertLess(self, a, b, msg=None)
     |      Just like self.assertTrue(a < b), but with a nicer default message.
     |  
     |  assertLessEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a <= b), but with a nicer default message.
     |  
     |  assertListEqual(self, list1, list2, msg=None)
     |      A list-specific equality assertion.
     |      
     |      Args:
     |          list1: The first list to compare.
     |          list2: The second list to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertLogs(self, logger=None, level=None)
     |      Fail unless a log message of level *level* or higher is emitted
     |      on *logger_name* or its children.  If omitted, *level* defaults to
     |      INFO and *logger* defaults to the root logger.
     |      
     |      This method must be used as a context manager, and will yield
     |      a recording object with two attributes: `output` and `records`.
     |      At the end of the context manager, the `output` attribute will
     |      be a list of the matching formatted log messages and the
     |      `records` attribute will be a list of the corresponding LogRecord
     |      objects.
     |      
     |      Example::
     |      
     |          with self.assertLogs('foo', level='INFO') as cm:
     |              logging.getLogger('foo').info('first message')
     |              logging.getLogger('foo.bar').error('second message')
     |          self.assertEqual(cm.output, ['INFO:foo:first message',
     |                                       'ERROR:foo.bar:second message'])
     |  
     |  assertMultiLineEqual(self, first, second, msg=None)
     |      Assert that two multi-line strings are equal.
     |  
     |  assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are equal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is less than the given delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      Objects that are equal automatically fail.
     |  
     |  assertNotAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotEqual(self, first, second, msg=None)
     |      Fail if the two objects are equal as determined by the '!='
     |      operator.
     |  
     |  assertNotEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a not in b), but with a nicer default message.
     |  
     |  assertNotIsInstance(self, obj, cls, msg=None)
     |      Included for symmetry with assertIsInstance.
     |  
     |  assertNotRegex(self, text, unexpected_regex, msg=None)
     |      Fail the test if the text matches the regular expression.
     |  
     |  assertNotRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertRaises(self, expected_exception, *args, **kwargs)
     |      Fail unless an exception of class expected_exception is raised
     |      by the callable when invoked with specified positional and
     |      keyword arguments. If a different type of exception is
     |      raised, it will not be caught, and the test case will be
     |      deemed to have suffered an error, exactly as for an
     |      unexpected exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertRaises(SomeException):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertRaises
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the exception as
     |      the 'exception' attribute. This allows you to inspect the
     |      exception after the assertion::
     |      
     |          with self.assertRaises(SomeException) as cm:
     |              do_something()
     |          the_exception = cm.exception
     |          self.assertEqual(the_exception.error_code, 3)
     |  
     |  assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs)
     |      Asserts that the message in a raised exception matches a regex.
     |      
     |      Args:
     |          expected_exception: Exception class expected to be raised.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertRaisesRegex is used as a context manager.
     |  
     |  assertRaisesRegexp = deprecated_func(*args, **kwargs)
     |  
     |  assertRegex(self, text, expected_regex, msg=None)
     |      Fail the test unless the text matches the regular expression.
     |  
     |  assertRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None)
     |      An equality assertion for ordered sequences (like lists and tuples).
     |      
     |      For the purposes of this function, a valid ordered sequence type is one
     |      which can be indexed, has a length, and has an equality operator.
     |      
     |      Args:
     |          seq1: The first sequence to compare.
     |          seq2: The second sequence to compare.
     |          seq_type: The expected datatype of the sequences, or None if no
     |                  datatype should be enforced.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertSetEqual(self, set1, set2, msg=None)
     |      A set-specific equality assertion.
     |      
     |      Args:
     |          set1: The first set to compare.
     |          set2: The second set to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |      
     |      assertSetEqual uses ducktyping to support different types of sets, and
     |      is optimized for sets specifically (parameters must support a
     |      difference method).
     |  
     |  assertTrue(self, expr, msg=None)
     |      Check that the expression is true.
     |  
     |  assertTupleEqual(self, tuple1, tuple2, msg=None)
     |      A tuple-specific equality assertion.
     |      
     |      Args:
     |          tuple1: The first tuple to compare.
     |          tuple2: The second tuple to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertWarns(self, expected_warning, *args, **kwargs)
     |      Fail unless a warning of class warnClass is triggered
     |      by the callable when invoked with specified positional and
     |      keyword arguments.  If a different type of warning is
     |      triggered, it will not be handled: depending on the other
     |      warning filtering rules in effect, it might be silenced, printed
     |      out, or raised as an exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertWarns(SomeWarning):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertWarns
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the first matching
     |      warning as the 'warning' attribute; similarly, the 'filename'
     |      and 'lineno' attributes give you information about the line
     |      of Python code from which the warning was triggered.
     |      This allows you to inspect the warning after the assertion::
     |      
     |          with self.assertWarns(SomeWarning) as cm:
     |              do_something()
     |          the_warning = cm.warning
     |          self.assertEqual(the_warning.some_attribute, 147)
     |  
     |  assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs)
     |      Asserts that the message in a triggered warning matches a regexp.
     |      Basic functioning is similar to assertWarns() with the addition
     |      that only warnings whose messages also match the regular expression
     |      are considered successful matches.
     |      
     |      Args:
     |          expected_warning: Warning class expected to be triggered.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertWarnsRegex is used as a context manager.
     |  
     |  assert_ = deprecated_func(*args, **kwargs)
     |  
     |  countTestCases(self)
     |  
     |  debug(self)
     |      Run the test without collecting errors in a TestResult
     |  
     |  defaultTestResult(self)
     |  
     |  doCleanups(self)
     |      Execute all cleanup functions. Normally called for you after
     |      tearDown.
     |  
     |  fail(self, msg=None)
     |      Fail immediately, with the given message.
     |  
     |  failIf = deprecated_func(*args, **kwargs)
     |  
     |  failIfAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failIfEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnless = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessRaises = deprecated_func(*args, **kwargs)
     |  
     |  id(self)
     |  
     |  run(self, result=None)
     |  
     |  shortDescription(self)
     |      Returns a one-line description of the test, or None if no
     |      description has been provided.
     |      
     |      The default implementation of this method returns the first line of
     |      the specified test method's docstring.
     |  
     |  skipTest(self, reason)
     |      Skip this test.
     |  
     |  subTest(self, msg=<object object at 0x7f267fce1280>, **params)
     |      Return a context manager that will return the enclosed block
     |      of code in a subtest identified by the optional message and
     |      keyword parameters.  A failure in the subtest marks the test
     |      case as failed but resumes execution at the end of the enclosed
     |      block, allowing further test code to be executed.
     |  
     |  tearDown(self)
     |      Hook method for deconstructing the test fixture after testing it.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from unittest.case.TestCase:
     |  
     |  setUpClass() from builtins.type
     |      Hook method for setting up class fixture before running tests in the class.
     |  
     |  tearDownClass() from builtins.type
     |      Hook method for deconstructing the class fixture after running all tests in the class.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from unittest.case.TestCase:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from unittest.case.TestCase:
     |  
     |  failureException = <class 'AssertionError'>
     |      Assertion failed.
     |  
     |  longMessage = True
     |  
     |  maxDiff = 640


```


## mr_utils.tests.recon.test_tv_denoising

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/recon/test_tv_denoising.py)

```
NAME
    mr_utils.tests.recon.test_tv_denoising

CLASSES
    unittest.case.TestCase(builtins.object)
        TestTVDenoisingTestCase
    
    class TestTVDenoisingTestCase(unittest.case.TestCase)
     |  A class whose instances are single test cases.
     |  
     |  By default, the test code itself should be placed in a method named
     |  'runTest'.
     |  
     |  If the fixture may be used for many test cases, create as
     |  many test methods as are needed. When instantiating such a TestCase
     |  subclass, specify in the constructor arguments the name of the test method
     |  that the instance is to execute.
     |  
     |  Test authors should subclass TestCase for their own tests. Construction
     |  and deconstruction of the test's environment ('fixture') can be
     |  implemented by overriding the 'setUp' and 'tearDown' methods respectively.
     |  
     |  If it is necessary to override the __init__ method, the base class
     |  __init__ method must always be called. It is important that subclasses
     |  should not change the signature of their __init__ method, since instances
     |  of the classes are instantiated automatically by parts of the framework
     |  in order to be run.
     |  
     |  When subclassing TestCase, you can set these attributes:
     |  * failureException: determines which exception will be raised when
     |      the instance's assertion methods fail; test methods raising this
     |      exception will be deemed to have 'failed' rather than 'errored'.
     |  * longMessage: determines whether long messages (including repr of
     |      objects used in assert methods) will be printed on failure in *addition*
     |      to any explicit message passed.
     |  * maxDiff: sets the maximum length of a diff in failure messages
     |      by assert methods using difflib. It is looked up as an instance
     |      attribute so can be configured by individual tests if required.
     |  
     |  Method resolution order:
     |      TestTVDenoisingTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_tv_denoising(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from unittest.case.TestCase:
     |  
     |  __call__(self, *args, **kwds)
     |      Call self as a function.
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, methodName='runTest')
     |      Create an instance of the class that will use the named test
     |      method when executed. Raises a ValueError if the instance does
     |      not have a method with the specified name.
     |  
     |  __repr__(self)
     |      Return repr(self).
     |  
     |  __str__(self)
     |      Return str(self).
     |  
     |  addCleanup(self, function, *args, **kwargs)
     |      Add a function, with arguments, to be called when the test is
     |      completed. Functions added are called on a LIFO basis and are
     |      called after tearDown on test failure or success.
     |      
     |      Cleanup items are called even if setUp fails (unlike tearDown).
     |  
     |  addTypeEqualityFunc(self, typeobj, function)
     |      Add a type specific assertEqual style function to compare a type.
     |      
     |      This method is for use by TestCase subclasses that need to register
     |      their own type equality functions to provide nicer error messages.
     |      
     |      Args:
     |          typeobj: The data type to call this function on when both values
     |                  are of the same type in assertEqual().
     |          function: The callable taking two arguments and an optional
     |                  msg= argument that raises self.failureException with a
     |                  useful error message when the two arguments are not equal.
     |  
     |  assertAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are unequal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is more than the given
     |      delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      If the two objects compare equal then they will automatically
     |      compare almost equal.
     |  
     |  assertAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertCountEqual(self, first, second, msg=None)
     |      An unordered sequence comparison asserting that the same elements,
     |      regardless of order.  If the same element occurs more than once,
     |      it verifies that the elements occur the same number of times.
     |      
     |          self.assertEqual(Counter(list(first)),
     |                           Counter(list(second)))
     |      
     |       Example:
     |          - [0, 1, 1] and [1, 0, 1] compare equal.
     |          - [0, 0, 1] and [0, 1] compare unequal.
     |  
     |  assertDictContainsSubset(self, subset, dictionary, msg=None)
     |      Checks whether dictionary is a superset of subset.
     |  
     |  assertDictEqual(self, d1, d2, msg=None)
     |  
     |  assertEqual(self, first, second, msg=None)
     |      Fail if the two objects are unequal as determined by the '=='
     |      operator.
     |  
     |  assertEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertFalse(self, expr, msg=None)
     |      Check that the expression is false.
     |  
     |  assertGreater(self, a, b, msg=None)
     |      Just like self.assertTrue(a > b), but with a nicer default message.
     |  
     |  assertGreaterEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a >= b), but with a nicer default message.
     |  
     |  assertIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a in b), but with a nicer default message.
     |  
     |  assertIs(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is b), but with a nicer default message.
     |  
     |  assertIsInstance(self, obj, cls, msg=None)
     |      Same as self.assertTrue(isinstance(obj, cls)), with a nicer
     |      default message.
     |  
     |  assertIsNone(self, obj, msg=None)
     |      Same as self.assertTrue(obj is None), with a nicer default message.
     |  
     |  assertIsNot(self, expr1, expr2, msg=None)
     |      Just like self.assertTrue(a is not b), but with a nicer default message.
     |  
     |  assertIsNotNone(self, obj, msg=None)
     |      Included for symmetry with assertIsNone.
     |  
     |  assertLess(self, a, b, msg=None)
     |      Just like self.assertTrue(a < b), but with a nicer default message.
     |  
     |  assertLessEqual(self, a, b, msg=None)
     |      Just like self.assertTrue(a <= b), but with a nicer default message.
     |  
     |  assertListEqual(self, list1, list2, msg=None)
     |      A list-specific equality assertion.
     |      
     |      Args:
     |          list1: The first list to compare.
     |          list2: The second list to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertLogs(self, logger=None, level=None)
     |      Fail unless a log message of level *level* or higher is emitted
     |      on *logger_name* or its children.  If omitted, *level* defaults to
     |      INFO and *logger* defaults to the root logger.
     |      
     |      This method must be used as a context manager, and will yield
     |      a recording object with two attributes: `output` and `records`.
     |      At the end of the context manager, the `output` attribute will
     |      be a list of the matching formatted log messages and the
     |      `records` attribute will be a list of the corresponding LogRecord
     |      objects.
     |      
     |      Example::
     |      
     |          with self.assertLogs('foo', level='INFO') as cm:
     |              logging.getLogger('foo').info('first message')
     |              logging.getLogger('foo.bar').error('second message')
     |          self.assertEqual(cm.output, ['INFO:foo:first message',
     |                                       'ERROR:foo.bar:second message'])
     |  
     |  assertMultiLineEqual(self, first, second, msg=None)
     |      Assert that two multi-line strings are equal.
     |  
     |  assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None)
     |      Fail if the two objects are equal as determined by their
     |      difference rounded to the given number of decimal places
     |      (default 7) and comparing to zero, or by comparing that the
     |      difference between the two objects is less than the given delta.
     |      
     |      Note that decimal places (from zero) are usually not the same
     |      as significant digits (measured from the most significant digit).
     |      
     |      Objects that are equal automatically fail.
     |  
     |  assertNotAlmostEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotEqual(self, first, second, msg=None)
     |      Fail if the two objects are equal as determined by the '!='
     |      operator.
     |  
     |  assertNotEquals = deprecated_func(*args, **kwargs)
     |  
     |  assertNotIn(self, member, container, msg=None)
     |      Just like self.assertTrue(a not in b), but with a nicer default message.
     |  
     |  assertNotIsInstance(self, obj, cls, msg=None)
     |      Included for symmetry with assertIsInstance.
     |  
     |  assertNotRegex(self, text, unexpected_regex, msg=None)
     |      Fail the test if the text matches the regular expression.
     |  
     |  assertNotRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertRaises(self, expected_exception, *args, **kwargs)
     |      Fail unless an exception of class expected_exception is raised
     |      by the callable when invoked with specified positional and
     |      keyword arguments. If a different type of exception is
     |      raised, it will not be caught, and the test case will be
     |      deemed to have suffered an error, exactly as for an
     |      unexpected exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertRaises(SomeException):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertRaises
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the exception as
     |      the 'exception' attribute. This allows you to inspect the
     |      exception after the assertion::
     |      
     |          with self.assertRaises(SomeException) as cm:
     |              do_something()
     |          the_exception = cm.exception
     |          self.assertEqual(the_exception.error_code, 3)
     |  
     |  assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs)
     |      Asserts that the message in a raised exception matches a regex.
     |      
     |      Args:
     |          expected_exception: Exception class expected to be raised.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertRaisesRegex is used as a context manager.
     |  
     |  assertRaisesRegexp = deprecated_func(*args, **kwargs)
     |  
     |  assertRegex(self, text, expected_regex, msg=None)
     |      Fail the test unless the text matches the regular expression.
     |  
     |  assertRegexpMatches = deprecated_func(*args, **kwargs)
     |  
     |  assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None)
     |      An equality assertion for ordered sequences (like lists and tuples).
     |      
     |      For the purposes of this function, a valid ordered sequence type is one
     |      which can be indexed, has a length, and has an equality operator.
     |      
     |      Args:
     |          seq1: The first sequence to compare.
     |          seq2: The second sequence to compare.
     |          seq_type: The expected datatype of the sequences, or None if no
     |                  datatype should be enforced.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertSetEqual(self, set1, set2, msg=None)
     |      A set-specific equality assertion.
     |      
     |      Args:
     |          set1: The first set to compare.
     |          set2: The second set to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |      
     |      assertSetEqual uses ducktyping to support different types of sets, and
     |      is optimized for sets specifically (parameters must support a
     |      difference method).
     |  
     |  assertTrue(self, expr, msg=None)
     |      Check that the expression is true.
     |  
     |  assertTupleEqual(self, tuple1, tuple2, msg=None)
     |      A tuple-specific equality assertion.
     |      
     |      Args:
     |          tuple1: The first tuple to compare.
     |          tuple2: The second tuple to compare.
     |          msg: Optional message to use on failure instead of a list of
     |                  differences.
     |  
     |  assertWarns(self, expected_warning, *args, **kwargs)
     |      Fail unless a warning of class warnClass is triggered
     |      by the callable when invoked with specified positional and
     |      keyword arguments.  If a different type of warning is
     |      triggered, it will not be handled: depending on the other
     |      warning filtering rules in effect, it might be silenced, printed
     |      out, or raised as an exception.
     |      
     |      If called with the callable and arguments omitted, will return a
     |      context object used like this::
     |      
     |           with self.assertWarns(SomeWarning):
     |               do_something()
     |      
     |      An optional keyword argument 'msg' can be provided when assertWarns
     |      is used as a context object.
     |      
     |      The context manager keeps a reference to the first matching
     |      warning as the 'warning' attribute; similarly, the 'filename'
     |      and 'lineno' attributes give you information about the line
     |      of Python code from which the warning was triggered.
     |      This allows you to inspect the warning after the assertion::
     |      
     |          with self.assertWarns(SomeWarning) as cm:
     |              do_something()
     |          the_warning = cm.warning
     |          self.assertEqual(the_warning.some_attribute, 147)
     |  
     |  assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs)
     |      Asserts that the message in a triggered warning matches a regexp.
     |      Basic functioning is similar to assertWarns() with the addition
     |      that only warnings whose messages also match the regular expression
     |      are considered successful matches.
     |      
     |      Args:
     |          expected_warning: Warning class expected to be triggered.
     |          expected_regex: Regex (re pattern object or string) expected
     |                  to be found in error message.
     |          args: Function to be called and extra positional args.
     |          kwargs: Extra kwargs.
     |          msg: Optional message used in case of failure. Can only be used
     |                  when assertWarnsRegex is used as a context manager.
     |  
     |  assert_ = deprecated_func(*args, **kwargs)
     |  
     |  countTestCases(self)
     |  
     |  debug(self)
     |      Run the test without collecting errors in a TestResult
     |  
     |  defaultTestResult(self)
     |  
     |  doCleanups(self)
     |      Execute all cleanup functions. Normally called for you after
     |      tearDown.
     |  
     |  fail(self, msg=None)
     |      Fail immediately, with the given message.
     |  
     |  failIf = deprecated_func(*args, **kwargs)
     |  
     |  failIfAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failIfEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnless = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessAlmostEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessEqual = deprecated_func(*args, **kwargs)
     |  
     |  failUnlessRaises = deprecated_func(*args, **kwargs)
     |  
     |  id(self)
     |  
     |  run(self, result=None)
     |  
     |  shortDescription(self)
     |      Returns a one-line description of the test, or None if no
     |      description has been provided.
     |      
     |      The default implementation of this method returns the first line of
     |      the specified test method's docstring.
     |  
     |  skipTest(self, reason)
     |      Skip this test.
     |  
     |  subTest(self, msg=<object object at 0x7f267fce1280>, **params)
     |      Return a context manager that will return the enclosed block
     |      of code in a subtest identified by the optional message and
     |      keyword parameters.  A failure in the subtest marks the test
     |      case as failed but resumes execution at the end of the enclosed
     |      block, allowing further test code to be executed.
     |  
     |  tearDown(self)
     |      Hook method for deconstructing the test fixture after testing it.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from unittest.case.TestCase:
     |  
     |  setUpClass() from builtins.type
     |      Hook method for setting up class fixture before running tests in the class.
     |  
     |  tearDownClass() from builtins.type
     |      Hook method for deconstructing the class fixture after running all tests in the class.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from unittest.case.TestCase:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from unittest.case.TestCase:
     |  
     |  failureException = <class 'AssertionError'>
     |      Assertion failed.
     |  
     |  longMessage = True
     |  
     |  maxDiff = 640


```

