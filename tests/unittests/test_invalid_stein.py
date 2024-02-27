# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from azure_functions_worker import protos
from tests.utils import testutils

STEIN_INVALID_APP_FUNCTIONS_DIR = testutils.UNIT_TESTS_FOLDER / \
    'broken_functions' / \
    'invalid_app_stein'
STEIN_INVALID_FUNCTIONS_DIR = testutils.UNIT_TESTS_FOLDER / \
    'broken_functions' / \
    'invalid_stein'


class TestInvalidAppStein(testutils.AsyncTestCase):

    async def test_indexing_not_app(self):
        """Test if the functions metadata response will be
            an error when an invalid app is provided
        """
        async with testutils.start_mockhost(
                script_root=STEIN_INVALID_APP_FUNCTIONS_DIR) as host:
            await host.init_worker()
            r = await host.get_functions_metadata()
            self.assertIsInstance(r.response, protos.FunctionMetadataResponse)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)
            self.assertIsNotNone(r.response.result.exception.message)
            self.assertRegex(r.response.result.exception.message,
                             r"ValueError: Could not find top level function app instances in function_app.py.")


class TestInvalidStein(testutils.AsyncTestCase):

    async def test_indexing_invalid_app(self):
        """Test if the functions metadata response will be
            an error when an invalid app is provided
        """
        async with testutils.start_mockhost(
                script_root=STEIN_INVALID_FUNCTIONS_DIR) as host:
            await host.init_worker()
            r = await host.get_functions_metadata()
            self.assertIsInstance(r.response, protos.FunctionMetadataResponse)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)
            self.assertIsNotNone(r.response.result.exception.message)
            self.assertRegex(r.response.result.exception.message,

                             r"FunctionLoadError: cannot load the main function: the following parameters "
                             r"are declared in function.json but not in Python: "
                             r".*'req'.*")
