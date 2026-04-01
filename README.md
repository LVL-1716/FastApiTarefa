# API de Gerenciamento de Tarefas com FastAPI

Uma aplicação simples e intuitiva para gerenciar suas tarefas através de uma API REST.

## Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## Instalação

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

## Executando a Aplicação

1. **Inicie o servidor:**
```bash
python app.py
```

Ou alternativamente:
```bash
uvicorn app:app --reload
```

2. **A aplicação estará disponível em:**
   - API: `http://127.0.0.1:8000`
   - Documentação Swagger: `http://127.0.0.1:8000/docs`
   - Documentação ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints (Rotas)

### 1. GET / - Raiz da API
**Descrição:** Retorna informações sobre os endpoints disponíveis.

**Requisição:**
```
GET http://127.0.0.1:8000/
```

**Resposta (200 OK):**
```json
{
  "mensagem": "Bem-vindo à API de Gerenciamento de Tarefas!",
  "versao": "1.0.0",
  "endpoints": {
    "POST /tarefas": "Adicionar uma nova tarefa",
    "GET /tarefas": "Listar todas as tarefas",
    "PUT /tarefas/{nome_tarefa}": "Marcar uma tarefa como concluída",
    "DELETE /tarefas/{nome_tarefa}": "Remover uma tarefa"
  }
}
```

---

### 2. POST /tarefas - Adicionar uma Nova Tarefa

**Descrição:** Adiciona uma nova tarefa com nome e descrição.

**Requisição:**
```
POST http://127.0.0.1:8000/tarefas
Content-Type: application/json

{
  "nome": "Estudar FastAPI",
  "descricao": "Aprender conceitos de FastAPI e criar uma API REST"
}
```

**Resposta (200 OK):**
```json
{
  "mensagem": "Tarefa adicionada com sucesso!",
  "tarefa": {
    "nome": "Estudar FastAPI",
    "descricao": "Aprender conceitos de FastAPI e criar uma API REST",
    "concluida": false
  }
}
```

---

### 3. GET /tarefas - Listar Todas as Tarefas

**Descrição:** Retorna a lista de todas as tarefas cadastradas.

**Requisição:**
```
GET http://127.0.0.1:8000/tarefas
```

**Resposta (200 OK):**
```json
[
  {
    "nome": "Estudar FastAPI",
    "descricao": "Aprender conceitos de FastAPI e criar uma API REST",
    "concluida": false
  },
  {
    "nome": "Fazer exercícios",
    "descricao": "Praticar programação em Python",
    "concluida": false
  }
]
```

---

### 4. PUT /tarefas/{nome_tarefa} - Marcar Tarefa como Concluída

**Descrição:** Marca uma tarefa específica como concluída.

**Requisição:**
```
PUT http://127.0.0.1:8000/tarefas/Estudar%20FastAPI
```

**Obs:** O nome da tarefa deve ser URL encoded (espaços substituídos por %20).

**Resposta (200 OK):**
```json
{
  "mensagem": "Tarefa marcada como concluída!",
  "tarefa": {
    "nome": "Estudar FastAPI",
    "descricao": "Aprender conceitos de FastAPI e criar uma API REST",
    "concluida": true
  }
}
```

**Resposta (404 Not Found) - Se a tarefa não existir:**
```json
{
  "detail": "Tarefa 'Tarefa Inexistente' não encontrada"
}
```

---

### 5. DELETE /tarefas/{nome_tarefa} - Remover uma Tarefa

**Descrição:** Remove uma tarefa específica da lista.

**Requisição:**
```
DELETE http://127.0.0.1:8000/tarefas/Estudar%20FastAPI
```

**Resposta (200 OK):**
```json
{
  "mensagem": "Tarefa removida com sucesso!",
  "tarefa": {
    "nome": "Estudar FastAPI",
    "descricao": "Aprender conceitos de FastAPI e criar uma API REST",
    "concluida": false
  }
}
```

**Resposta (404 Not Found) - Se a tarefa não existir:**
```json
{
  "detail": "Tarefa 'Tarefa Inexistente' não encontrada"
}
```

---

## Testando com Insomnia ou Postman

### No Insomnia:

1. **Abra o Insomnia**
2. **Crie uma nova coleção** para organizar suas requisições
3. **Adicione requisições** seguindo os exemplos abaixo:

#### Exemplo de Teste Completo:

1. **POST** - Adicionar primeira tarefa
   - URL: `http://127.0.0.1:8000/tarefas`
   - Body (JSON): 
   ```json
   {
     "nome": "Comprar leite",
     "descricao": "Ir ao mercado e comprar leite integral"
   }
   ```

2. **POST** - Adicionar segunda tarefa
   - URL: `http://127.0.0.1:8000/tarefas`
   - Body (JSON):
   ```json
   {
     "nome": "Fazer lição de casa",
     "descricao": "Fazer exercícios de matemática do capítulo 5"
   }
   ```

3. **GET** - Listar todas as tarefas
   - URL: `http://127.0.0.1:8000/tarefas`
   - Método: GET

4. **PUT** - Marcar tarefa como concluída
   - URL: `http://127.0.0.1:8000/tarefas/Comprar%20leite`
   - Método: PUT

5. **GET** - Listar novamente para verificar
   - URL: `http://127.0.0.1:8000/tarefas`
   - Método: GET

6. **DELETE** - Remover tarefa
   - URL: `http://127.0.0.1:8000/tarefas/Fazer%20lição%20de%20casa`
   - Método: DELETE

### Dicas:

- A API diferencia letras maiúsculas e minúsculas para os nomes das tarefas
- Os nomes com espaços devem ser URL encoded (%20) nas rotas PUT e DELETE
- A documentação interativa da API está em `/docs` (Swagger)
- O campo "concluida" é caso-sensitivo e sempre inicia como `false`

## Estrutura de Dados

Cada tarefa é um dicionário com os seguintes campos:

```python
{
    "nome": str,           # Nome da tarefa (obrigatório)
    "descricao": str,      # Descrição da tarefa (obrigatório)
    "concluida": bool      # Status de conclusão (inicialmente False)
}
```

## Notas Importantes

1. **Dados em Memória:** As tarefas são armazenadas em uma lista na memória da aplicação. Quando você reinicia a aplicação, todas as tarefas são perdidas.

2. **Tamanho Ilimitado:** Não há limite de tarefas que você pode adicionar.

3. **Case-Sensitive:** Os nomes das tarefas diferenciam maiúsculas de minúsculas ao buscar (PUT e DELETE).

## Futuras Melhorias

Para uma aplicação em produção, considere:
- Usar um banco de dados persistente (SQLite, PostgreSQL, etc.)
- Adicionar autenticação e autorização
- Implementar validação mais robusta
- Adicionar testes automatizados
- Adicionar IDs únicos para as tarefas
- Implementar data de criação e modificação
- Adicionar paginação para listas grandes
