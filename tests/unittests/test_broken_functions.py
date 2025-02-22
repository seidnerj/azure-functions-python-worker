# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from azure_functions_worker import protos
from tests.utils import testutils


class TestMockHost(testutils.AsyncTestCase):
    broken_funcs_dir = testutils.UNIT_TESTS_FOLDER / 'broken_functions'

    async def test_load_broken__missing_py_param(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('missing_py_param')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r".*cannot load the missing_py_param function"
                r".*parameters are declared in function.json"
                r".*'req'.*")

    async def test_load_broken__missing_json_param(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('missing_json_param')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r".*cannot load the missing_json_param function"
                r".*parameters are declared in Python"
                r".*'spam'.*")

    async def test_load_broken__wrong_param_dir(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('wrong_param_dir')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the wrong_param_dir function'
                r'.*binding foo is declared to have the "out".*')

    async def test_load_broken__bad_out_annotation(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('bad_out_annotation')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the bad_out_annotation function'
                r'.*binding foo has invalid Out annotation.*')

    async def test_load_broken__wrong_binding_dir(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('wrong_binding_dir')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the wrong_binding_dir function'
                r'.* binding foo is declared to have the "in" direction'
                r'.*but its annotation is.*Out.*')

    async def test_load_broken__invalid_context_param(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('invalid_context_param')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the invalid_context_param function'
                r'.*the "context" parameter.*')

    async def test_load_broken__syntax_error(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('syntax_error')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertIn('SyntaxError', r.response.result.exception.message)

    async def test_load_broken__module_not_found_error(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('module_not_found_error')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertIn('ModuleNotFoundError',
                          r.response.result.exception.message)

    async def test_load_broken__import_error(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('import_error')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertIn('ImportError',
                          r.response.result.exception.message)
            self.assertNotIn('<frozen importlib._bootstrap>',
                             r.response.result.exception.message)
            self.assertNotIn('<frozen importlib._bootstrap_external>',
                             r.response.result.exception.message)

    async def test_load_broken__inout_param(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('inout_param')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the inout_param function'
                r'.*"inout" bindings.*')

    async def test_load_broken__return_param_in(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('return_param_in')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the return_param_in function'
                r'.*"\$return" .* set to "out"')

    async def test_load_broken__invalid_return_anno(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('invalid_return_anno')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the invalid_return_anno function'
                r'.*Python return annotation "int" does not match '
                r'binding type "http"')

    async def test_load_broken__invalid_return_anno_non_type(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function(
                'invalid_return_anno_non_type')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the invalid_return_anno_non_type function: '
                r'has invalid non-type return annotation 123')

    async def test_load_broken__invalid_http_trigger_anno(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('invalid_http_trigger_anno')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertEqual(
                r.response.result.exception.message,
                'FunctionLoadError: cannot load the invalid_http_trigger_anno'
                ' function: type of req binding in function.json "httpTrigger" '
                'does not match its Python annotation "int"')

    async def test_load_broken__invalid_out_anno(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('invalid_out_anno')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertEqual(
                r.response.result.exception.message,
                'FunctionLoadError: cannot load the invalid_out_anno function: '
                r'type of ret binding in function.json "http" '
                r'does not match its Python annotation "HttpRequest"')

    async def test_load_broken__invalid_in_anno(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('invalid_in_anno')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertEqual(
                r.response.result.exception.message,
                'FunctionLoadError: cannot load the invalid_in_anno function: '
                r'type of req binding in function.json "httpTrigger" '
                r'does not match its Python annotation "HttpResponse"')

    async def test_load_broken__invalid_datatype(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('invalid_datatype')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the invalid_datatype function: '
                r'.*binding type "httpTrigger" and dataType "1" in '
                r'function.json do not match the corresponding function '
                r'parameter.* Python type annotation "HttpResponse"')

    async def test_load_broken__invalid_in_anno_non_type(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('invalid_in_anno_non_type')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the invalid_in_anno_non_type function: '
                r'binding req has invalid non-type annotation 123')

    async def test_import_module_troubleshooting_url(self):
        async with testutils.start_mockhost(
                script_root=self.broken_funcs_dir) as host:
            await host.init_worker()
            func_id, r = await host.load_function('missing_module')

            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*ModuleNotFoundError')
