# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import unittest
import sys

import azure.functions as func

from azure_functions_worker import protos
from azure_functions_worker.bindings import datumdef, meta
from tests.utils import testutils

# Even if the tests are skipped for <=3.8, the library is still imported as
# it is used for these tests.
if sys.version_info.minor >= 9:
    from azurefunctions.extensions.bindings.blob import BlobClient, BlobClientConverter

DEFERRED_BINDINGS_ENABLED_DIR = testutils.EXTENSION_TESTS_FOLDER / \
    'deferred_bindings_tests' / \
    'deferred_bindings_functions' / \
    'deferred_bindings_enabled'
DEFERRED_BINDINGS_DISABLED_DIR = testutils.EXTENSION_TESTS_FOLDER / \
    'deferred_bindings_tests' / \
    'deferred_bindings_functions' / \
    'deferred_bindings_disabled'

DEFERRED_BINDINGS_ENABLED_DUAL_DIR = testutils.EXTENSION_TESTS_FOLDER / \
    'deferred_bindings_tests' / \
    'deferred_bindings_functions' / \
    'deferred_bindings_enabled_dual'


class MockMBD:
    def __init__(self, version: str, source: str,
                 content_type: str, content: str):
        self.version = version
        self.source = source
        self.content_type = content_type
        self.content = content


@unittest.skipIf(sys.version_info.minor <= 8, "The base extension"
                                              "is only supported for 3.9+.")
class TestDeferredBindingsEnabled(testutils.AsyncTestCase):

    async def test_deferred_bindings_metadata(self):
        async with testutils.start_mockhost(
                script_root=DEFERRED_BINDINGS_ENABLED_DIR) as host:
            await host.init_worker()
            r = await host.get_functions_metadata()
            self.assertIsInstance(r.response, protos.FunctionMetadataResponse)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Success)


@unittest.skipIf(sys.version_info.minor <= 8, "The base extension"
                                              "is only supported for 3.9+.")
class TestDeferredBindingsEnabledDual(testutils.AsyncTestCase):

    async def test_deferred_bindings_dual_metadata(self):
        async with testutils.start_mockhost(
                script_root=DEFERRED_BINDINGS_ENABLED_DUAL_DIR) as host:
            await host.init_worker()
            r = await host.get_functions_metadata()
            self.assertIsInstance(r.response, protos.FunctionMetadataResponse)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Success)


@unittest.skipIf(sys.version_info.minor <= 8, "The base extension"
                                              "is only supported for 3.9+.")
class TestDeferredBindingsDisabled(testutils.AsyncTestCase):

    async def test_non_deferred_bindings_metadata(self):
        async with testutils.start_mockhost(
                script_root=DEFERRED_BINDINGS_DISABLED_DIR) as host:
            await host.init_worker()
            r = await host.get_functions_metadata()
            self.assertIsInstance(r.response, protos.FunctionMetadataResponse)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Success)


@unittest.skipIf(sys.version_info.minor <= 8, "The base extension"
                                              "is only supported for 3.9+.")
class TestDeferredBindingsHelpers(testutils.AsyncTestCase):

    def test_deferred_bindings_decode(self):
        binding = BlobClientConverter
        pb = protos.ParameterBinding(name='test',
                                     data=protos.TypedData(
                                         string='test'))
        sample_mbd = MockMBD(version="1.0",
                             source="AzureStorageBlobs",
                             content_type="application/json",
                             content="{\"Connection\":\"AzureWebJobsStorage\","
                                     "\"ContainerName\":"
                                     "\"python-worker-tests\","
                                     "\"BlobName\":"
                                     "\"test-blobclient-trigger.txt\"}")
        datum = datumdef.Datum(value=sample_mbd, type='model_binding_data')

        obj = meta.deferred_bindings_decode(binding=binding, pb=pb,
                                            pytype=BlobClient, datum=datum, metadata={})

        self.assertIsNotNone(obj)

    async def test_check_deferred_bindings_enabled(self):
        """
        check_deferred_bindings_enabled checks if deferred bindings is enabled at fx
        and single binding level.

        The first bool represents if deferred bindings is enabled at a fx level. This
        means that at least one binding in the function is a deferred binding type.

        The second represents if the current binding is deferred binding. If this is
        True, then deferred bindings must also be enabled at the function level.
        """
        async with testutils.start_mockhost(
                script_root=DEFERRED_BINDINGS_DISABLED_DIR) as host:
            await host.init_worker()

            self.assertEqual(meta.check_deferred_bindings_enabled(
                func.InputStream, False), (False, False))

            self.assertEqual(meta.check_deferred_bindings_enabled(
                func.InputStream, True), (True, False))

            self.assertEqual(meta.check_deferred_bindings_enabled(
                BlobClient, False), (True, True))

            self.assertEqual(meta.check_deferred_bindings_enabled(
                BlobClient, True), (True, True))
