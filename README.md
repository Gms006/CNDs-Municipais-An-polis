# Emissor Automático de Certidões de Regularidade Fiscal
## Requisitos
- Python 3.10+
- Navegador Chrome instalado no caminho:
  `C:/Program Files/Google/Chrome/Application/chrome.exe`

## Instalação

1. Clone o repositório e crie um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Baixe os binários do navegador utilizados pelo Playwright:

```bash
playwright install
```

4. Crie um arquivo `.env` na raiz do projeto com sua chave da 2Captcha:

```env
API_KEY_2CAPTCHA=sua_chave_aqui
```

5. Verifique se os seguintes caminhos estão corretos (ajuste conforme necessidade):
- Planilha de CNPJs: `G:/PMA/LISTA EMPRESAS - NETO CONTABILIDADE 2025.xlsm`
- Diretório das empresas: `G:/EMPRESAS/`

## Execução

Para rodar o script:

```bash
python nome_do_script.py
```

Durante a execução, serão mostradas barras de progresso e logs coloridos. Os logs completos são salvos na pasta:

```
G:/PMA/SCRIPTS/CNDs/logs/
```

## Modo de Teste
Se desejar testar o script sem resolver captchas automaticamente:

```python
MODO_TESTE = True
```

Nesse modo, o script aguarda que o usuário resolva o captcha manualmente.
