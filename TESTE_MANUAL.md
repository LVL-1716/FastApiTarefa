# Tutorial de Testes da API de Gerenciamento de Tarefas

## Pré-requisitos

1. **FastAPI instalado** via `pip install -r requirements.txt`
2. **Servidor rodando** com `python app.py` ou `uvicorn app:app --reload`
3. **Insomnia** ou **Postman** instalado
4. **URL Base:** `http://127.0.0.1:8000`

---

## Teste Passo a Passo no Insomnia

### Passo 1: Criar uma Nova Requisição GET

1. Abra o **Insomnia**
2. Crie uma nova requisição (Ctrl + K ou Cmd + K)
3. Selecione o método **GET**
4. Digite a URL: `http://127.0.0.1:8000/`
5. Clique em **Send**

**Resultado Esperado:**
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

### Passo 2: Adicionar Primeira Tarefa (POST)

1. Crie uma nova requisição
2. Selecione o método **POST**
3. Digite a URL: `http://127.0.0.1:8000/tarefas`
4. Na aba **Body**, selecione **JSON**
5. Cole o seguinte corpo:

```json
{
  "nome": "Estudar FastAPI",
  "descricao": "Aprender conceitos de FastAPI e criar uma API REST"
}
```

6. Clique em **Send**

**Resultado Esperado (Status 200):**
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

### Passo 3: Adicionar Segunda Tarefa (POST)

1. Crie outra requisição POST para `http://127.0.0.1:8000/tarefas`
2. Body (JSON):

```json
{
  "nome": "Fazer exercícios",
  "descricao": "Praticar programação em Python"
}
```

3. Clique em **Send**

**Resultado Esperado (Status 200):**
```json
{
  "mensagem": "Tarefa adicionada com sucesso!",
  "tarefa": {
    "nome": "Fazer exercícios",
    "descricao": "Praticar programação em Python",
    "concluida": false
  }
}
```

---

### Passo 4: Adicionar Terceira Tarefa (POST)

1. Requisição POST para `http://127.0.0.1:8000/tarefas`
2. Body (JSON):

```json
{
  "nome": "Comprar leite",
  "descricao": "Ir ao mercado e comprar leite integral"
}
```

3. Clique em **Send**

---

### Passo 5: Listar Todas as Tarefas (GET)

1. Crie uma nova requisição GET
2. URL: `http://127.0.0.1:8000/tarefas`
3. Clique em **Send**

**Resultado Esperado (Status 200):**
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
  },
  {
    "nome": "Comprar leite",
    "descricao": "Ir ao mercado e comprar leite integral",
    "concluida": false
  }
]
```

---

### Passo 6: Marcar Tarefa como Concluída (PUT)

1. Crie uma nova requisição
2. Selecione o método **PUT**
3. URL: `http://127.0.0.1:8000/tarefas/Estudar%20FastAPI`
   - **Nota:** O espaço é codificado como `%20`
4. Clique em **Send**

**Resultado Esperado (Status 200):**
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

---

### Passo 7: Tentar Marcar Novamente (PUT - com erro esperado)

1. Crie outra requisição PUT
2. URL: `http://127.0.0.1:8000/tarefas/Tarefa%20Inexistente`
3. Clique em **Send**

**Resultado Esperado (Status 404):**
```json
{
  "detail": "Tarefa 'Tarefa Inexistente' não encontrada"
}
```

---

### Passo 8: Remover uma Tarefa (DELETE)

1. Crie uma nova requisição
2. Selecione o método **DELETE**
3. URL: `http://127.0.0.1:8000/tarefas/Comprar%20leite`
4. Clique em **Send**

**Resultado Esperado (Status 200):**
```json
{
  "mensagem": "Tarefa removida com sucesso!",
  "tarefa": {
    "nome": "Comprar leite",
    "descricao": "Ir ao mercado e comprar leite integral",
    "concluida": false
  }
}
```

---

### Passo 9: Listar Novamente (GET)

1. Use a requisição GET anterior
2. URL: `http://127.0.0.1:8000/tarefas`
3. Clique em **Send**

**Resultado Esperado (Status 200):**
```json
[
  {
    "nome": "Estudar FastAPI",
    "descricao": "Aprender conceitos de FastAPI e criar uma API REST",
    "concluida": true
  },
  {
    "nome": "Fazer exercícios",
    "descricao": "Praticar programação em Python",
    "concluida": false
  }
]
```

Note que:
- A tarefa "Comprar leite" foi removida
- A tarefa "Estudar FastAPI" está marcada como concluída (concluida: true)
- A tarefa "Fazer exercícios" continua não concluída

---

## Teste no Postman

O processo é similar ao Insomnia:

1. **Crie uma nova coleção** chamada "API de Tarefas"
2. **Adicione requisições** com os exemplos acima
3. Configure o **URL** e o **método** corretamente
4. Na aba **Body**, selecione **raw** e **JSON** para requisições POST
5. Clique em **Send** para cada requisição

---

## Teste via cURL (Terminal/PowerShell)

Se preferir testar via linha de comando:

### 1. Adicionar Tarefa
```bash
curl -X POST "http://127.0.0.1:8000/tarefas" ^
  -H "Content-Type: application/json" ^
  -d "{\"nome\": \"Estudar FastAPI\", \"descricao\": \"Aprender FastAPI\"}"
```

### 2. Listar Tarefas
```bash
curl -X GET "http://127.0.0.1:8000/tarefas"
```

### 3. Marcar como Concluída
```bash
curl -X PUT "http://127.0.0.1:8000/tarefas/Estudar%20FastAPI"
```

### 4. Remover Tarefa
```bash
curl -X DELETE "http://127.0.0.1:8000/tarefas/Estudar%20FastAPI"
```

---

## Usando Documentação Automática (Swagger)

FastAPI gera documentação automática em `/docs`:

1. Com o servidor rodando, acesse: `http://127.0.0.1:8000/docs`
2. Você verá a **Swagger UI** com todas as rotas
3. Expanda cada rota clicando nela
4. Clique em **Try it out**
5. Preencha os parâmetros/body necessários
6. Clique em **Execute** para fazer a requisição

Esta é a forma mais prática e visual de testar a API!

---

## Checklist de Testes

Após completar todos os passos, você deve ter:

- ✓ Requisição GET para raiz funcionando
- ✓ Requisição POST adicionando tarefas
- ✓ Requisição GET listando todas as tarefas
- ✓ Requisição PUT marcando tarefas como concluídas
- ✓ Requisição DELETE removendo tarefas
- ✓ Requisição PUT com erro 404 para tarefa inexistente
- ✓ Requisição DELETE com erro 404 para tarefa inexistente
- ✓ Lista atualizada refletindo todas as operações

Parabéns! Sua API está funcionando corretamente!
