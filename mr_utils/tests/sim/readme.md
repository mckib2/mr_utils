
## mr_utils.tests.sim.test_bloch_simulator

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/sim/test_bloch_simulator.py)

```
NAME
    mr_utils.tests.sim.test_bloch_simulator - Test numerical Bloch simulations.

CLASSES
    unittest.case.TestCase(builtins.object)
        TestBloch
    
    class TestBloch(unittest.case.TestCase)
     |  Verify bloch simulations.
     |  
     |  Method resolution order:
     |      TestBloch
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_against_gre(self)
     |      Test implementation against GRE simulation.
     |  
     |  test_matrix_against_loop(self)
     |      Test matrix implementation against naive loop implementation.
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


## mr_utils.tests.sim.test_gre

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/sim/test_gre.py)

```
NAME
    mr_utils.tests.sim.test_gre - Test GRE contrast simulations.

CLASSES
    unittest.case.TestCase(builtins.object)
        TestGRE
    
    class TestGRE(unittest.case.TestCase)
     |  Verify GRE simulations against various implementations.
     |  
     |  Method resolution order:
     |      TestGRE
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_gre_sim_against_closed_form_solution(self)
     |      Verify iterative solution against closed form solution.
     |      
     |      Uses fixed number of iterations.
     |  
     |  test_gre_sim_mat_against_gre_sim_loop(self)
     |      Verify against loop implementation.
     |  
     |  test_gre_sim_using_tol_against_closed_form_sol(self)
     |      Verify iterative solution against closed form solution.
     |      
     |      Used tolerance instead of fixed number of iterations.
     |  
     |  test_gre_unspoiled_and_bssfp(self)
     |      Very balanced steady state solution.
     |  
     |  test_spoiled_gre(self)
     |      Sanity check -- all nonzero pixels should be the same intensity.
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


## mr_utils.tests.sim.test_motion

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/sim/test_motion.py)

```
NAME
    mr_utils.tests.sim.test_motion

CLASSES
    unittest.case.TestCase(builtins.object)
        SimMotionTestCase
    
    class SimMotionTestCase(unittest.case.TestCase)
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
     |      SimMotionTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  test_motion(self)
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


## mr_utils.tests.sim.test_rayleigh

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/sim/test_rayleigh.py)

```
NAME
    mr_utils.tests.sim.test_rayleigh - Test generation of Rayleigh noise.

CLASSES
    unittest.case.TestCase(builtins.object)
        RayleighNoiseTestCase
    
    class RayleighNoiseTestCase(unittest.case.TestCase)
     |  Tests against scipy's statistics module.
     |  
     |  Method resolution order:
     |      RayleighNoiseTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_rayleigh_high_noise(self)
     |      Verify rayleigh high noise case against scipy's statistics module.
     |  
     |  test_rayleigh_is_rician_high_noise(self)
     |      Verify rayleigh becomes rician high noise scipy's statistics module.
     |  
     |  test_rayleigh_is_rician_low_noise(self)
     |      Verify rayleigh becomes rician low noise scipy's statistics module.
     |  
     |  test_rayleigh_low_noise(self)
     |      Verify rayleigh low noise case against scipy's statistics module.
     |  
     |  test_rayleigh_mean_high_noise(self)
     |      Verify mean of high noise case with scipy's statistics module.
     |  
     |  test_rayleigh_mean_low_noise(self)
     |      Verify mean of low noise case with scipy's statistics module.
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


## mr_utils.tests.sim.test_rician

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/sim/test_rician.py)

```
NAME
    mr_utils.tests.sim.test_rician - Test generation of Rician noise.

CLASSES
    unittest.case.TestCase(builtins.object)
        RicianNoiseTestCase
    
    class RicianNoiseTestCase(unittest.case.TestCase)
     |  Tests against scipy's statistics module.
     |  
     |  Method resolution order:
     |      RicianNoiseTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_rician_high_noise(self)
     |      Verify high noise case against scipy statistics module.
     |  
     |  test_rician_low_noise(self)
     |      Verify low noise case against scipy statistics module.
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


## mr_utils.tests.sim.test_single_voxel

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/sim/test_single_voxel.py)

```
NAME
    mr_utils.tests.sim.test_single_voxel

CLASSES
    unittest.case.TestCase(builtins.object)
        SingleVoxelImagingTestCase
    
    class SingleVoxelImagingTestCase(unittest.case.TestCase)
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
     |      SingleVoxelImagingTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  test_combine_images(self)
     |  
     |  test_single_voxel(self)
     |  
     |  test_single_voxel_phantom_data(self)
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


## mr_utils.tests.sim.test_ssfp

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/sim/test_ssfp.py)

```
NAME
    mr_utils.tests.sim.test_ssfp - Test cases for SSFP simulation.

CLASSES
    unittest.case.TestCase(builtins.object)
        DictionaryTestCase
        EllipticalSignalTestCase
        MultiplePhaseCycleTestCase
    
    class DictionaryTestCase(unittest.case.TestCase)
     |  Look up df in a dictionary of T1,T2,alpha.
     |  
     |  Method resolution order:
     |      DictionaryTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_dictionary(self)
     |      Verify implementation against a naive loop implementation.
     |  
     |  test_find_atom(self)
     |      Test method that finds atom in a given dictionary.
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
    
    class EllipticalSignalTestCase(unittest.case.TestCase)
     |  Test elliptical signal model functions against cartesian, NMR funcs.
     |  
     |  Method resolution order:
     |      EllipticalSignalTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_banding_sim_2d(self)
     |      Make sure banding looks the same coming from NMR params and ESM.
     |  
     |  test_center_of_mass(self)
     |      Make sure we can find the center of mass of an ellipse.
     |  
     |  test_cross_point(self)
     |      Find cross point from cartesian and ESM function.
     |  
     |  test_make_ellipse(self)
     |      Make an ellipse given NMR params and elliptical params.
     |  
     |  test_spectrum(self)
     |      Generate bSSFP spectrum.
     |  
     |  test_ssfp_sim(self)
     |      Generate signal from bSSFP signal eq and elliptical model.
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
    
    class MultiplePhaseCycleTestCase(unittest.case.TestCase)
     |  Compute multiple phase-cycles at once.
     |  
     |  Method resolution order:
     |      MultiplePhaseCycleTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_many_phase_cycles_single_point(self)
     |      Make sure we can do a bunch of them at once.
     |  
     |  test_two_phase_cycles_multiple_point(self)
     |      Now make MxN param maps and simulate multiple phase-cycles.
     |  
     |  test_two_phase_cycles_single_point(self)
     |      Try doing two phase-cycles.
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


## mr_utils.tests.sim.test_ssfp_2d_sim

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/sim/test_ssfp_2d_sim.py)

```
NAME
    mr_utils.tests.sim.test_ssfp_2d_sim - Make sure 2D SSFP contrast simulation works.

CLASSES
    unittest.case.TestCase(builtins.object)
        BSSFP2DSimTestCase
    
    class BSSFP2DSimTestCase(unittest.case.TestCase)
     |  Test Cases for bSSFP contrast simulation.
     |  
     |  Method resolution order:
     |      BSSFP2DSimTestCase
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_gs(self)
     |      Test GS recon using simulated data.
     |  
     |  test_t1_t2_field_map_mats(self)
     |      Generate simulation given t1,t2, and field maps.
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


## mr_utils.tests.sim.test_ssfp_quantitative_field_mapping

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/tests/sim/test_ssfp_quantitative_field_mapping.py)

```
NAME
    mr_utils.tests.sim.test_ssfp_quantitative_field_mapping - Test Quantitative field map functions.

CLASSES
    unittest.case.TestCase(builtins.object)
        TestQuantitativeFieldMap
    
    class TestQuantitativeFieldMap(unittest.case.TestCase)
     |  Test quantitative field mapping functions.
     |  
     |  Method resolution order:
     |      TestQuantitativeFieldMap
     |      unittest.case.TestCase
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  setUp(self)
     |      Hook method for setting up the test fixture before exercising it.
     |  
     |  test_simulated_field_maps(self)
     |      Simulate the field maps and see if we can recover them.
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

