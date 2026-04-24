from typing import Optional
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

# Inicializar a aplicação FastAPI
app = FastAPI()
security = HTTPBasic(auto_error=False)

VALID_USER = "usuario"
VALID_PASSWORD = "senha123"
ALLOWED_SORT_FIELDS = {"nome", "descricao"}

# Definir modelo para tarefa
class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

# Lista de tarefas (banco de dados em memória)
tarefas = []


def validar_credenciais(credentials: Optional[HTTPBasicCredentials] = Depends(security)) -> str:
    """Valida o usuário e senha fornecidos via autenticação básica."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )

    username_valid = secrets.compare_digest(credentials.username, VALID_USER)
    password_valid = secrets.compare_digest(credentials.password, VALID_PASSWORD)

    if not (username_valid and password_valid):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


# ROTA 1: Adicionar uma nova tarefa (POST)
@app.post("/tarefas", response_model=dict)
def adicionar_tarefa(tarefa: Tarefa, usuario: str = Depends(validar_credenciais)):
    """
    Adiciona uma nova tarefa à lista.
    
    Args:
        tarefa: Objeto contendo nome e descrição
        usuario: Usuário autenticado
        
    Returns:
        Dicionário com a tarefa adicionada
    """
    tarefas.append(tarefa)
    return {"mensagem": "Tarefa adicionada com sucesso!", "tarefa": tarefa}


# ROTA 2: Listar todas as tarefas (GET)
@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas(
    page: int = 1,
    size: int = 10,
    sort_by: Optional[str] = None,
    usuario: str = Depends(validar_credenciais),
):
    """
    Retorna a lista de todas as tarefas cadastradas.
    
    Args:
        page: Número da página a ser retornada
        size: Quantidade de tarefas por página
        sort_by: Campo para ordenar os resultados
        usuario: Usuário autenticado
    
    Returns:
        Lista paginada de tarefas
    """
    if page < 1 or size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parâmetros de paginação inválidos. page e size devem ser maiores que zero.",
        )

    if sort_by is not None and sort_by not in ALLOWED_SORT_FIELDS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campo de ordenação inválido. Use 'nome' ou 'descricao'.",
        )

    tarefas_ordenadas = tarefas
    if sort_by is not None:
        tarefas_ordenadas = sorted(tarefas, key=lambda tarefa: getattr(tarefa, sort_by))

    inicio = (page - 1) * size
    fim = inicio + size
    return tarefas_ordenadas[inicio:fim]


# ROTA 3: Marcar uma tarefa como concluída (PUT)
@app.put("/tarefas/{nome_tarefa}")
def marcar_concluida(nome_tarefa: str, usuario: str = Depends(validar_credenciais)):
    """
    Marca uma tarefa como concluída.
    
    Args:
        nome_tarefa: Nome da tarefa a ser marcada como concluída
        usuario: Usuário autenticado
    
    Returns:
        Dicionário com a tarefa atualizada
        
    Raises:
        HTTPException: Se a tarefa não for encontrada
    """
    for tarefa in tarefas:
        if tarefa.nome.lower() == nome_tarefa.lower():
            tarefa.concluida = True
            return {"mensagem": "Tarefa marcada como concluída!", "tarefa": tarefa}
    
    raise HTTPException(status_code=404, detail=f"Tarefa '{nome_tarefa}' não encontrada")


# ROTA 4: Remover uma tarefa (DELETE)
@app.delete("/tarefas/{nome_tarefa}")
def remover_tarefa(nome_tarefa: str, usuario: str = Depends(validar_credenciais)):
    """
    Remove uma tarefa da lista.
    
    Args:
        nome_tarefa: Nome da tarefa a ser removida
        usuario: Usuário autenticado
    
    Returns:
        Dicionário com mensagem de sucesso
        
    Raises:
        HTTPException: Se a tarefa não for encontrada
    """
    for i, tarefa in enumerate(tarefas):
        if tarefa.nome.lower() == nome_tarefa.lower():
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
