import asyncio
import sys
import types
from importlib.machinery import SourceFileLoader
import unittest
import logging

# Cria módulos fictícios para dependências ausentes
if "dotenv" not in sys.modules:
    dotenv_stub = types.ModuleType("dotenv")
    dotenv_stub.load_dotenv = lambda *a, **kw: None
    sys.modules["dotenv"] = dotenv_stub

if "playwright" not in sys.modules:
    playwright_stub = types.ModuleType("playwright")
    async_api_stub = types.ModuleType("playwright.async_api")
    playwright_stub.async_api = async_api_stub
    async_api_stub.async_playwright = lambda: None
    async_api_stub.expect = None
    sys.modules["playwright"] = playwright_stub
    sys.modules["playwright.async_api"] = async_api_stub

for mod_name in ["requests", "openpyxl", "colorama"]:
    if mod_name not in sys.modules:
        mod = types.ModuleType(mod_name)
        if mod_name == "colorama":
            mod.Fore = types.SimpleNamespace(GREEN="", BLUE="", RED="", CYAN="", YELLOW="", WHITE="")
            mod.Back = types.SimpleNamespace()
            mod.Style = types.SimpleNamespace(RESET_ALL="")
            mod.init = lambda *a, **kw: None
        sys.modules[mod_name] = mod

# Evitar que o script tente criar arquivos de log durante os testes
original_file_handler = logging.FileHandler
class DummyFileHandler(logging.Handler):
    def __init__(self, *a, **kw):
        super().__init__()
    def emit(self, record):
        pass
logging.FileHandler = DummyFileHandler

script = SourceFileLoader('script', 'script').load_module()

# Restaurar FileHandler original para não afetar outros testes
logging.FileHandler = original_file_handler

class ProcessarCNPJsTestCase(unittest.TestCase):
    def test_falha_quando_emitir_certidao_retorna_false(self):
        async def fake_emitir_certidao(page, cnpj, api_key, idx, total, empresas_dict):
            return False

        async def fake_acessar_pagina_certidao(page):
            return None

        original_emitir = script.emitir_certidao
        original_acessar = script.acessar_pagina_certidao
        script.emitir_certidao = fake_emitir_certidao
        script.acessar_pagina_certidao = fake_acessar_pagina_certidao
        try:
            async def run_test():
                sucessos, falhas = await script.processar_cnpjs(None, ['1','2'], 'key', {})
                self.assertEqual(sucessos, 0)
                self.assertEqual(falhas, 2)
            asyncio.run(run_test())
        finally:
            script.emitir_certidao = original_emitir
            script.acessar_pagina_certidao = original_acessar

if __name__ == '__main__':
    unittest.main()
