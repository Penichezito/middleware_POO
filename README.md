# Middleware Automation Programs

## 📋 Descrição
Esse Middleware é um serviço de automação que gerencia e executa tarefas programadas através de uma API central. O sistema monitora continuamente uma fila de tarefas, executando programas específicos conforme necessário e mantendo registros detalhados de todas as operações.

## 🚀 Funcionalidades
- Monitoramento contínuo de tarefas via API
- Execução automática de programas
- Sistema de logging completo
- Tratamento robusto de erros
- Suporte a execução como serviço Windows
- Compatibilidade com ambientes sem Python instalado

## 🔧 Requisitos do Sistema
- Windows 7 ou superior (64 bits)
- 2GB de RAM (mínimo)
- 500MB de espaço em disco
- Acesso à internet para comunicação com a API

## 📦 Instalação

### Versão Executável
1. Baixe o arquivo `OctopusTaxMiddleware.exe` da última release
2. Coloque o executável na pasta desejada
3. Execute o programa (recomenda-se executar como administrador)

### Desenvolvimento
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/octopustax-middleware.git
cd octopustax-middleware
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🛠️ Build do Executável

1. Certifique-se de ter o ambiente de desenvolvimento configurado
2. Execute o script de build:
```bash
python build.py
```
3. O executável será gerado na pasta `dist/`

## 📄 Configuração

### Estrutura de Arquivos
```
projeto/
├── dist/
│   └── OctopusTaxMiddleware.exe
├── logs/
│   └── octopusTax-middleware.log
├── middleware.py
├── build.py
├── requirements.txt
└── README.md
```

### Logs
Os logs são gerados automaticamente em:
- Modo desenvolvimento: `./octopusTax-middleware.log`
- Modo executável: Na mesma pasta do `.exe`

## 🚦 Uso

### Executável
1. Execute `OctopusTaxMiddleware.exe`
2. O programa iniciará automaticamente o monitoramento
3. Verifique os logs para acompanhar a execução

### Desenvolvimento
```bash
python middleware.py
```

## 🔍 Monitoramento
- Os logs são gerados continuamente durante a execução
- Cada execução de tarefa é registrada com timestamp
- Erros são registrados com stack trace completo

## ⚠️ Resolução de Problemas

### Problemas Comuns

1. Erro "Arquivo não encontrado":
   - Verifique se o caminho do programa está correto na API
   - Confirme se o programa existe no local especificado
   - Verifique permissões de acesso

2. Erro de conexão com API:
   - Verifique sua conexão com a internet
   - Confirme se a URL da API está correta
   - Verifique se a API está online

3. Programa não executa:
   - Verifique permissões de administrador
   - Confirme se o programa é um executável válido
   - Verifique os logs para erros específicos

## 🔐 Segurança
- O middleware executa apenas programas especificados na API
- Logs são mantidos para auditoria
- Verificações de segurança antes da execução
- Tratamento seguro de caminhos de arquivo

## 📝 Notas de Desenvolvimento
- Desenvolvido em Python 3.9+
- Usa asyncio para operações assíncronas
- Sistema de logging estruturado
- Compatível com PyInstaller para distribuição

## 🤝 Suporte
Para suporte, entre em contato:
- Email: suporte@octopustax.com.br
- Telefone: (XX) XXXX-XXXX

## 📜 Licença
Copyright © 2024 OctopusTax. Todos os direitos reservados.
