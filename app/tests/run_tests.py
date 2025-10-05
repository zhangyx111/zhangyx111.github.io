import unittest
import sys
import os

# Add the project root directory to the path so we can import the app
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Import the test modules
from test_auth import AuthTestCase

# Create a test suite
def create_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuthTestCase))
    return suite

# Run the tests
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    suite = create_test_suite()
    result = runner.run(suite)
    
    # Exit with error code if tests failed
    sys.exit(not result.wasSuccessful())
