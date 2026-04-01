# Guia Completo - API de Gerenciamento de Tarefas

## 📋 Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Como Testar](#como-testar)
- [Documentação da API](#documentação-da-api)

---

## 🗂️ Estrutura do Projeto

```
FastApiTarefa/
│
├── app.py                    # Arquivo principal da aplicação FastAPI
├── test_app.py              # Testes automatizados com pytest
├── requirements.txt         # Dependências do projeto
├── README.md                # Documentação completa da API
├── TESTE_MANUAL.md          # Tutorial de teste manual no Insomnia/Postman
├── GUIA_COMPLETO.md         # Este arquivo
└── exemplos_requisicoes.json # Exemplos de requisições
```

---

## 🚀 Instalação

### Pré-requisitos
- **Python 3.8 ou superior** instalado
- **Windows, macOS ou Linux**

### Paso 1: Instalar Dependências

Abra um terminal/PowerShell na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

**Ou** se estiver usando Python 3:

```bash
pip3 install -r requirements.txt
```

---

## 🎯 Como Executar

### Opção 1: Usando Python diretamente

```bash
python app.py
```

Você deverá ver uma saída similar a:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Opção 2: Usando Uvicorn com recarregamento automático

```bash
uvicorn app:app --reload
```

A flag `--reload` reinicia o servidor automaticamente quando você salva mudanças no código.

### Verificar se está funcionando

Abra seu navegador e acesse:
- **Raiz da API:** `http://127.0.0.1:8000/`
- **Documentação Swagger:** `http://127.0.0.1:8000/docs`
- **Documentação ReDoc:** `http://127.0.0.1:8000/redoc`

---

## 🧪 Como Testar

### Opção 1: Documentação Interativa (Recomendado)

1. Com o servidor rodando, acesse `http://127.0.0.1:8000/docs`
2. Expanda cada rota clicando nela
3. Clique em **Try it out**
4. Preencha os dados necessários
5. Clique em **Execute**

### Opção 2: Usando Insomnia

1. Baixe o [Insomnia](https://insomnia.rest/)
2. Crie uma nova requisição
3. Configure URL e método conforme exemplos em [TESTE_MANUAL.md](TESTE_MANUAL.md)
4. Envie as requisições

### Opção 3: Usando Postman

1. Baixe o [Postman](https://www.postman.com/)
2. Crie uma nova coleção
3. Configure as requisições conforme exemplos em [TESTE_MANUAL.md](TESTE_MANUAL.md)
4. Envie as requisições

### Opção 4: Testes Automatizados (Pytest)

Para rodar os testes automatizados:

```bash
pytest test_app.py
```

Para mais detalhes:

```bash
pytest test_app.py -v
```

Para coverage (cobertura de testes):

```bash
pytest test_app.py --cov=app
```

**O que os testes verificam:**
- ✓ Endpoint raiz funcionando corretamente
- ✓ Adição de tarefas
- ✓ Listagem de tarefas
- ✓ Marcação de tarefas como concluídas
- ✓ Remoção de tarefas
- ✓ Tratamento de erros (tarefa não encontrada)
- ✓ Busca case-insensitive
- ✓ Fluxo completo de operações

### Opção 5: Usando cURL (Terminal/PowerShell)

#### Adicionar tarefa
```bash
curl -X POST "http://127.0.0.1:8000/tarefas" -H "Content-Type: application/json" -d "{\"nome\": \"Minha Tarefa\", \"descricao\": \"Descrição aqui\"}"
```

#### Listar tarefas
```bash
curl -X GET "http://127.0.0.1:8000/tarefas"
```

#### Marcar como concluída
```bash
curl -X PUT "http://127.0.0.1:8000/tarefas/Minha%20Tarefa"
```

#### Remover tarefa
```bash
curl -X DELETE "http://127.0.0.1:8000/tarefas/Minha%20Tarefa"
```

---

## 📚 Documentação da API

### Endpoints Disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Informações sobre os endpoints |
| `POST` | `/tarefas` | Adicionar nova tarefa |
| `GET` | `/tarefas` | Listar todas as tarefas |
| `PUT` | `/tarefas/{nome_tarefa}` | Marcar tarefa como concluída |
| `DELETE` | `/tarefas/{nome_tarefa}` | Remover tarefa |

### Estrutura de uma Tarefa

```json
{
  "nome": "string",           // Nome da tarefa (obrigatório)
  "descricao": "string",      // Descrição da tarefa (obrigatório)
  "concluida": false          // Status: true ou false
}
```

### Exemplos de Requisições

#### POST - Adicionar Tarefa
```
POST http://127.0.0.1:8000/tarefas
Content-Type: application/json

{
  "nome": "Estudar FastAPI",
  "descricao": "Aprender conceitos de FastAPI"
}
```

**Resposta (200 OK):**
```json
{
  "mensagem": "Tarefa adicionada com sucesso!",
  "tarefa": {
    "nome": "Estudar FastAPI",
    "descricao": "Aprender conceitos de FastAPI",
    "concluida": false
  }
}
```

#### GET - Listar Tarefas
```
GET http://127.0.0.1:8000/tarefas
```

**Resposta (200 OK):**
```json
[
  {
    "nome": "Estudar FastAPI",
    "descricao": "Aprender conceitos de FastAPI",
    "concluida": false
  }
]
```

#### PUT - Marcar como Concluída
```
PUT http://127.0.0.1:8000/tarefas/Estudar%20FastAPI
```

**Resposta (200 OK):**
```json
{
  "mensagem": "Tarefa marcada como concluída!",
  "tarefa": {
    "nome": "Estudar FastAPI",
    "descricao": "Aprender conceitos de FastAPI",
    "concluida": true
  }
}
```

#### DELETE - Remover Tarefa
```
DELETE http://127.0.0.1:8000/tarefas/Estudar%20FastAPI
```

**Resposta (200 OK):**
```json
{
  "mensagem": "Tarefa removida com sucesso!",
  "tarefa": {
    "nome": "Estudar FastAPI",
    "descricao": "Aprender conceitos de FastAPI",
    "concluida": false
  }
}
```

---

## 🔧 Dicas Úteis

### Acessando a documentação interativa
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### Encoding de URLs
Quando uma tarefa tem espaços, eles devem ser substituídos por `%20`:
- Tarefa: "Estudar FastAPI"
- Na URL: `/tarefas/Estudar%20FastAPI`

### Busca case-insensitive
A busca funciona independente de maiúsculas/minúsculas:
- `/tarefas/estudar%20fastapi` = `/tarefas/Estudar%20FastAPI`

### Reiniciar a aplicação
Para parar o servidor no terminal, pressione `Ctrl + C`

---

## 📝 Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `app.py` | Arquivo principal com todas as rotas |
| `test_app.py` | Testes automatizados |
| `requirements.txt` | Dependências do projeto |
| `README.md` | Documentação completa da API |
| `TESTE_MANUAL.md` | Tutorial passo a passo de testes |
| `exemplos_requisicoes.json` | Exemplos de requisições |

---

## 🐛 Solução de Problemas

### "Address already in use"
A porta 8000 já está em uso. Use outra porta:
```bash
uvicorn app:app --reload --port 8001
```

### "ModuleNotFoundError: No module named 'fastapi'"
Instale as dependências:
```bash
pip install -r requirements.txt
```

### "pip: command not found"
Tente usar `pip3` em vez de `pip`:
```bash
pip3 install -r requirements.txt
```

---

## 🎓 Próximos Passos (Melhorias)

1. **Banco de Dados**: Usar SQLite, PostgreSQL ou MongoDB para persistência
2. **Autenticação**: Adicionar JWT ou OAuth
3. **Validação**: Usar mais validações com Pydantic
4. **IDs Únicos**: Usar UUIDs em vez de nomes
5. **Timestamps**: Adicionar data de criação e modificação
6. **Paginação**: Implementar para grandes listas
7. **Filtros**: Adicionar filtros by status
8. **Rate Limiting**: Limitar requisições por IP
9. **CORS**: Configurar para requisições do frontend
10. **Logging**: Adicionar logs detalhados

---

## 📞 Suporte

Para dúvidas sobre FastAPI, consulte:
- [Documentação Oficial FastAPI](https://fastapi.tiangolo.com/)
- [Documentação Pydantic](https://docs.pydantic.dev/)
- [Documentação Uvicorn](https://www.uvicorn.org/)

---

**Versão**: 1.0.0  
**Última atualização**: Março de 2024  
**Status**: ✅ Pronto para uso
