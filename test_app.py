import pytest
from fastapi.testclient import TestClient
from app import app

# Criar cliente de teste
client = TestClient(app)
VALID_AUTH = ("usuario", "senha123")
INVALID_AUTH = ("usuario", "senha_errada")

class TestAPITarefas:
    """Testes para a API de Gerenciamento de Tarefas"""
    
    def setup_method(self):
        """Limpar tarefas antes de cada teste"""
        # Importar tarefas do módulo app
        from app import tarefas
        tarefas.clear()
    
    def test_root_endpoint(self):
        """Testa o endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        assert "mensagem" in response.json()
        assert "endpoints" in response.json()
    
    def test_autenticacao_obrigatoria_para_tarefas(self):
        """Testa que as rotas de tarefas exigem autenticação"""
        response = client.get("/tarefas")
        assert response.status_code == 401
        assert response.json()["detail"] == "Credenciais inválidas"
    
    def test_adicionar_tarefa(self):
        """Testa adição de uma tarefa"""
        tarefa_data = {
            "nome": "Estudar Python",
            "descricao": "Aprender o básico de Python"
        }
        response = client.post("/tarefas", json=tarefa_data, auth=VALID_AUTH)
        
        assert response.status_code == 200
        assert response.json()["mensagem"] == "Tarefa adicionada com sucesso!"
        assert response.json()["tarefa"]["nome"] == "Estudar Python"
        assert response.json()["tarefa"]["concluida"] is False
    
    def test_listar_tarefas_vazio(self):
        """Testa listagem de tarefas quando não há nenhuma"""
        response = client.get("/tarefas", auth=VALID_AUTH)
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_listar_tarefas_com_dados(self):
        """Testa listagem de tarefas quando há dados"""
        # Adicionar primeira tarefa
        client.post("/tarefas", json={
            "nome": "Tarefa 1",
            "descricao": "Descrição 1"
        }, auth=VALID_AUTH)
        
        # Adicionar segunda tarefa
        client.post("/tarefas", json={
            "nome": "Tarefa 2",
            "descricao": "Descrição 2"
        }, auth=VALID_AUTH)
        
        # Listar tarefas
        response = client.get("/tarefas", auth=VALID_AUTH)
        
        assert response.status_code == 200
        tarefas = response.json()
        assert len(tarefas) == 2
        assert tarefas[0]["nome"] == "Tarefa 1"
        assert tarefas[1]["nome"] == "Tarefa 2"
    
    def test_listar_tarefas_com_paginacao_e_ordenacao(self):
        """Testa paginação e ordenação na listagem de tarefas"""
        client.post("/tarefas", json={"nome": "B tarefa", "descricao": "Segunda"}, auth=VALID_AUTH)
        client.post("/tarefas", json={"nome": "A tarefa", "descricao": "Primeira"}, auth=VALID_AUTH)
        client.post("/tarefas", json={"nome": "C tarefa", "descricao": "Terceira"}, auth=VALID_AUTH)

        response = client.get("/tarefas?page=1&size=1&sort_by=nome", auth=VALID_AUTH)
        assert response.status_code == 200
        assert response.json() == [{"nome": "A tarefa", "descricao": "Primeira", "concluida": False}]

        response = client.get("/tarefas?page=2&size=1&sort_by=nome", auth=VALID_AUTH)
        assert response.status_code == 200
        assert response.json() == [{"nome": "B tarefa", "descricao": "Segunda", "concluida": False}]
    
    def test_listar_tarefas_ordenacao_invalida(self):
        """Testa erro ao usar campo de ordenação inválido"""
        client.post("/tarefas", json={"nome": "Tarefa X", "descricao": "Descrição"}, auth=VALID_AUTH)

        response = client.get("/tarefas?sort_by=concluida", auth=VALID_AUTH)
        assert response.status_code == 400
        assert response.json()["detail"] == "Campo de ordenação inválido. Use 'nome' ou 'descricao'."
    
    def test_listar_tarefas_paginacao_invalida(self):
        """Testa erro ao usar parâmetros de paginação inválidos"""
        response = client.get("/tarefas?page=0&size=5", auth=VALID_AUTH)
        assert response.status_code == 400
        assert "Parâmetros de paginação inválidos" in response.json()["detail"]
    
    def test_credenciais_invalidas(self):
        """Testa resposta quando as credenciais estão incorretas"""
        response = client.get("/tarefas", auth=INVALID_AUTH)
        assert response.status_code == 401
        assert response.json()["detail"] == "Credenciais inválidas"
    
    def test_marcar_tarefa_como_concluida(self):
        """Testa marcação de tarefa como concluída"""
        # Adicionar uma tarefa
        client.post("/tarefas", json={
            "nome": "Tarefa Concluir",
            "descricao": "Esta tarefa será concluída"
        }, auth=VALID_AUTH)
        
        # Marcar como concluída
        response = client.put("/tarefas/Tarefa%20Concluir", auth=VALID_AUTH)
        
        assert response.status_code == 200
        assert response.json()["mensagem"] == "Tarefa marcada como concluída!"
        assert response.json()["tarefa"]["concluida"] is True
    
    def test_marcar_tarefa_inexistente(self):
        """Testa tentativa de marcar tarefa inexistente como concluída"""
        response = client.put("/tarefas/Tarefa%20Inexistente", auth=VALID_AUTH)
        
        assert response.status_code == 404
        assert "não encontrada" in response.json()["detail"]
    
    def test_remover_tarefa(self):
        """Testa remoção de uma tarefa"""
        # Adicionar uma tarefa
        client.post("/tarefas", json={
            "nome": "Tarefa Remover",
            "descricao": "Esta tarefa será removida"
        }, auth=VALID_AUTH)
        
        # Verificar que a tarefa existe
        response = client.get("/tarefas", auth=VALID_AUTH)
        assert len(response.json()) == 1
        
        # Remover a tarefa
        response = client.delete("/tarefas/Tarefa%20Remover", auth=VALID_AUTH)
        
        assert response.status_code == 200
        assert response.json()["mensagem"] == "Tarefa removida com sucesso!"
        
        # Verificar que a tarefa foi removida
        response = client.get("/tarefas", auth=VALID_AUTH)
        assert len(response.json()) == 0
    
    def test_remover_tarefa_inexistente(self):
        """Testa tentativa de remover tarefa inexistente"""
        response = client.delete("/tarefas/Tarefa%20Inexistente", auth=VALID_AUTH)
        
        assert response.status_code == 404
        assert "não encontrada" in response.json()["detail"]
    
    def test_fluxo_completo(self):
        """Testa um fluxo completo de operações"""
        # 1. Adicionar tarefas
        client.post("/tarefas", json={
            "nome": "Tarefa A",
            "descricao": "Descrição A"
        }, auth=VALID_AUTH)
        client.post("/tarefas", json={
            "nome": "Tarefa B",
            "descricao": "Descrição B"
        }, auth=VALID_AUTH)
        
        # 2. Listar tarefas (deve ter 2)
        response = client.get("/tarefas", auth=VALID_AUTH)
        assert len(response.json()) == 2
        
        # 3. Marcar Tarefa A como concluída
        client.put("/tarefas/Tarefa%20A", auth=VALID_AUTH)
        
        # 4. Listar novamente
        response = client.get("/tarefas", auth=VALID_AUTH)
        tarefas = response.json()
        assert tarefas[0]["concluida"] is True
        assert tarefas[1]["concluida"] is False
        
        # 5. Remover Tarefa B
        client.delete("/tarefas/Tarefa%20B", auth=VALID_AUTH)
        
        # 6. Listar novamente (deve ter 1)
        response = client.get("/tarefas", auth=VALID_AUTH)
        assert len(response.json()) == 1
        assert response.json()[0]["nome"] == "Tarefa A"
    
    def test_case_insensitive_busca(self):
        """Testa se a busca é case-insensitive"""
        # Adicionar tarefa
        client.post("/tarefas", json={
            "nome": "Tarefa Teste",
            "descricao": "Test"
        }, auth=VALID_AUTH)
        
        # Tentar marcar com case diferente
        response = client.put("/tarefas/tarefa%20teste", auth=VALID_AUTH)
        
        assert response.status_code == 200
        assert response.json()["tarefa"]["concluida"] is True
    
    def test_multiplas_tarefas_mesmo_status(self):
        """Testa múltiplas tarefas com o mesmo status"""
        # Adicionar várias tarefas
        for i in range(3):
            client.post("/tarefas", json={
                "nome": f"Tarefa {i}",
                "descricao": f"Descrição {i}"
            }, auth=VALID_AUTH)
        
        # Marcar primeira como concluída
        client.put("/tarefas/Tarefa%200", auth=VALID_AUTH)
        
        # Listar e verificar
        response = client.get("/tarefas", auth=VALID_AUTH)
        tarefas = response.json()
        
        assert tarefas[0]["concluida"] is True
        assert tarefas[1]["concluida"] is False
        assert tarefas[2]["concluida"] is False

if __name__ == "__main__":
    # Executar os testes
    pytest.main([__file__, "-v"])
