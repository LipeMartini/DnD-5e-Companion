# Como Criar o Executável do D&D Character Sheet

## Opção 1: Usando o Script Automático (Recomendado)

1. Instale o PyInstaller (se ainda não tiver):
```bash
pip install pyinstaller
```

2. Execute o script de build:
```bash
python build_exe.py
```

3. O executável será criado em: `dist/DnD Character Sheet.exe`

---

## Opção 2: Comando Manual

Se preferir executar manualmente, use:

```bash
pyinstaller --name="DnD Character Sheet" --onefile --windowed --add-data="data;data" --optimize=2 main.py
```

---

## Opção 3: Comando Simples (Mais Rápido)

Para um build rápido sem otimizações:

```bash
pyinstaller --onefile --windowed main.py
```

---

## Notas Importantes

- **--onefile**: Cria um único arquivo .exe (mais fácil de distribuir)
- **--windowed**: Remove a janela do console (apenas GUI)
- **--add-data**: Inclui a pasta `data` com spells, classes, etc.
- O executável ficará em: `dist/DnD Character Sheet.exe`
- Primeira execução pode demorar alguns minutos
- O arquivo .exe será grande (~50-100MB) pois inclui Python e PyQt6

---

## Testando o Executável

Após criar, teste executando:
```bash
cd dist
"DnD Character Sheet.exe"
```

---

## Distribuição

Para distribuir para outros usuários:
1. Copie apenas o arquivo `DnD Character Sheet.exe` da pasta `dist`
2. O executável é standalone - não precisa de Python instalado
3. Usuários podem executar diretamente clicando duas vezes

---

## Troubleshooting

**Erro: "PyInstaller not found"**
- Solução: `pip install pyinstaller`

**Erro: "data folder not found"**
- Certifique-se de que a pasta `data` existe no diretório do projeto

**Executável muito grande**
- Normal! Inclui Python + PyQt6 + todas as dependências
- Tamanho típico: 50-100MB

**Antivírus bloqueia o executável**
- Normal para executáveis criados com PyInstaller
- Adicione exceção no antivírus ou distribua o código-fonte
