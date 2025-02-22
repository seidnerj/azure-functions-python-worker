import asyncio
import unittest
from unittest.mock import patch, MagicMock

from azure_functions_worker import protos
from tests.unittests.test_dispatcher import FUNCTION_APP_DIRECTORY
from tests.utils import testutils


class TestOpenTelemetry(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.dispatcher = testutils.create_dummy_dispatcher()

    def tearDown(self):
        self.loop.close()

    def test_update_opentelemetry_status_import_error(self):
        # Patch the built-in import mechanism
        with patch('builtins.__import__', side_effect=ImportError):
            self.dispatcher.update_opentelemetry_status()
            # Verify that otel_libs_available is set to False due to ImportError
            self.assertFalse(self.dispatcher._otel_libs_available)

    @patch('builtins.__import__')
    def test_update_opentelemetry_status_success(
            self, mock_imports):
        mock_imports.return_value = MagicMock()
        self.dispatcher.update_opentelemetry_status()
        self.assertTrue(self.dispatcher._otel_libs_available)

    @patch('builtins.__import__')
    def test_init_request_otel_capability_enabled(
            self, mock_imports):
        mock_imports.return_value = MagicMock()

        init_request = protos.StreamingMessage(
            worker_init_request=protos.WorkerInitRequest(
                host_version="2.3.4",
                function_app_directory=str(FUNCTION_APP_DIRECTORY)
            )
        )

        init_response = self.loop.run_until_complete(
            self.dispatcher._handle__worker_init_request(init_request))

        self.assertEqual(init_response.worker_init_response.result.status,
                         protos.StatusResult.Success)

        # Verify that WorkerOpenTelemetryEnabled capability is set to _TRUE
        capabilities = init_response.worker_init_response.capabilities
        self.assertIn("WorkerOpenTelemetryEnabled", capabilities)
        self.assertEqual(capabilities["WorkerOpenTelemetryEnabled"], "true")

    def test_init_request_otel_capability_disabled(self):

        init_request = protos.StreamingMessage(
            worker_init_request=protos.WorkerInitRequest(
                host_version="2.3.4",
                function_app_directory=str(FUNCTION_APP_DIRECTORY)
            )
        )

        init_response = self.loop.run_until_complete(
            self.dispatcher._handle__worker_init_request(init_request))

        self.assertEqual(init_response.worker_init_response.result.status,
                         protos.StatusResult.Success)

        capabilities = init_response.worker_init_response.capabilities
        self.assertNotIn("WorkerOpenTelemetryEnabled", capabilities)
