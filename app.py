from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializar a aplicação FastAPI
app = FastAPI()

# Definir modelo para requisição de tarefa (POST)
class TarefaCreate(BaseModel):
    nome: str
    descricao: str

# Definir modelo para resposta de tarefa
class TarefaResponse(BaseModel):
    nome: str
    descricao: str
    concluida: bool

# Lista de tarefas (banco de dados em memória)
tarefas = []

# ROTA 1: Adicionar uma nova tarefa (POST)
@app.post("/tarefas", response_model=dict)
def adicionar_tarefa(tarefa: TarefaCreate):
    """
    Adiciona uma nova tarefa à lista.
    
    Args:
        tarefa: Objeto contendo nome e descrição
        
    Returns:
        Dicionário com a tarefa adicionada
    """
    nova_tarefa = {
        "nome": tarefa.nome,
        "descricao": tarefa.descricao,
        "concluida": False
    }
    tarefas.append(nova_tarefa)
    return {"mensagem": "Tarefa adicionada com sucesso!", "tarefa": nova_tarefa}

# ROTA 2: Listar todas as tarefas (GET)
@app.get("/tarefas", response_model=list)
def listar_tarefas():
    """
    Retorna a lista de todas as tarefas cadastradas.
    
    Returns:
        Lista de tarefas
    """
    return tarefas

# ROTA 3: Marcar uma tarefa como concluída (PUT)
@app.put("/tarefas/{nome_tarefa}")
def marcar_concluida(nome_tarefa: str):
    """
    Marca uma tarefa como concluída.
    
    Args:
        nome_tarefa: Nome da tarefa a ser marcada como concluída
        
    Returns:
        Dicionário com a tarefa atualizada
        
    Raises:
        HTTPException: Se a tarefa não for encontrada
    """
    for tarefa in tarefas:
        if tarefa["nome"].lower() == nome_tarefa.lower():
            tarefa["concluida"] = True
            return {"mensagem": "Tarefa marcada como concluída!", "tarefa": tarefa}
    
    raise HTTPException(status_code=404, detail=f"Tarefa '{nome_tarefa}' não encontrada")

# ROTA 4: Remover uma tarefa (DELETE)
@app.delete("/tarefas/{nome_tarefa}")
def remover_tarefa(nome_tarefa: str):
    """
    Remove uma tarefa da lista.
    
    Args:
        nome_tarefa: Nome da tarefa a ser removida
        
    Returns:
        Dicionário com mensagem de sucesso
        
    Raises:
        HTTPException: Se a tarefa não for encontrada
    """
    for i, tarefa in enumerate(tarefas):
        if tarefa["nome"].lower() == nome_tarefa.lower():
            tarefa_removida = tarefas.pop(i)
            return {"mensagem": "Tarefa removida com sucesso!", "tarefa": tarefa_removida}
    
    raise HTTPException(status_code=404, detail=f"Tarefa '{nome_tarefa}' não encontrada")

# ROTA EXTRA: Raiz da API
@app.get("/", response_model=dict)
def root():
    """
    Retorna uma mensagem de boas-vindas.
    """
    return {
        "mensagem": "Bem-vindo à API de Gerenciamento de Tarefas!",
        "versao": "1.0.0",
        "endpoints": {
            "POST /tarefas": "Adicionar uma nova tarefa",
            "GET /tarefas": "Listar todas as tarefas",
            "PUT /tarefas/{nome_tarefa}": "Marcar uma tarefa como concluída",
            "DELETE /tarefas/{nome_tarefa}": "Remover uma tarefa"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
