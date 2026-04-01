import pytest
from fastapi.testclient import TestClient
from app import app

# Criar cliente de teste
client = TestClient(app)

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
    
    def test_adicionar_tarefa(self):
        """Testa adição de uma tarefa"""
        tarefa_data = {
            "nome": "Estudar Python",
            "descricao": "Aprender o básico de Python"
        }
        response = client.post("/tarefas", json=tarefa_data)
        
        assert response.status_code == 200
        assert response.json()["mensagem"] == "Tarefa adicionada com sucesso!"
        assert response.json()["tarefa"]["nome"] == "Estudar Python"
        assert response.json()["tarefa"]["concluida"] == False
    
    def test_listar_tarefas_vazio(self):
        """Testa listagem de tarefas quando não há nenhuma"""
        response = client.get("/tarefas")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_listar_tarefas_com_dados(self):
        """Testa listagem de tarefas quando há dados"""
        # Adicionar primeira tarefa
        client.post("/tarefas", json={
            "nome": "Tarefa 1",
            "descricao": "Descrição 1"
        })
        
        # Adicionar segunda tarefa
        client.post("/tarefas", json={
            "nome": "Tarefa 2",
            "descricao": "Descrição 2"
        })
        
        # Listar tarefas
        response = client.get("/tarefas")
        
        assert response.status_code == 200
        tarefas = response.json()
        assert len(tarefas) == 2
        assert tarefas[0]["nome"] == "Tarefa 1"
        assert tarefas[1]["nome"] == "Tarefa 2"
    
    def test_marcar_tarefa_como_concluida(self):
        """Testa marcação de tarefa como concluída"""
        # Adicionar uma tarefa
        client.post("/tarefas", json={
            "nome": "Tarefa Concluir",
            "descricao": "Esta tarefa será concluída"
        })
        
        # Marcar como concluída
        response = client.put("/tarefas/Tarefa%20Concluir")
        
        assert response.status_code == 200
        assert response.json()["mensagem"] == "Tarefa marcada como concluída!"
        assert response.json()["tarefa"]["concluida"] == True
    
    def test_marcar_tarefa_inexistente(self):
        """Testa tentativa de marcar tarefa inexistente como concluída"""
        response = client.put("/tarefas/Tarefa%20Inexistente")
        
        assert response.status_code == 404
        assert "não encontrada" in response.json()["detail"]
    
    def test_remover_tarefa(self):
        """Testa remoção de uma tarefa"""
        # Adicionar uma tarefa
        client.post("/tarefas", json={
            "nome": "Tarefa Remover",
            "descricao": "Esta tarefa será removida"
        })
        
        # Verificar que a tarefa existe
        response = client.get("/tarefas")
        assert len(response.json()) == 1
        
        # Remover a tarefa
        response = client.delete("/tarefas/Tarefa%20Remover")
        
        assert response.status_code == 200
        assert response.json()["mensagem"] == "Tarefa removida com sucesso!"
        
        # Verificar que a tarefa foi removida
        response = client.get("/tarefas")
        assert len(response.json()) == 0
    
    def test_remover_tarefa_inexistente(self):
        """Testa tentativa de remover tarefa inexistente"""
        response = client.delete("/tarefas/Tarefa%20Inexistente")
        
        assert response.status_code == 404
        assert "não encontrada" in response.json()["detail"]
    
    def test_fluxo_completo(self):
        """Testa um fluxo completo de operações"""
        # 1. Adicionar tarefas
        client.post("/tarefas", json={
            "nome": "Tarefa A",
            "descricao": "Descrição A"
        })
        client.post("/tarefas", json={
            "nome": "Tarefa B",
            "descricao": "Descrição B"
        })
        
        # 2. Listar tarefas (deve ter 2)
        response = client.get("/tarefas")
        assert len(response.json()) == 2
        
        # 3. Marcar Tarefa A como concluída
        client.put("/tarefas/Tarefa%20A")
        
        # 4. Listar novamente
        response = client.get("/tarefas")
        tarefas = response.json()
        assert tarefas[0]["concluida"] == True
        assert tarefas[1]["concluida"] == False
        
        # 5. Remover Tarefa B
        client.delete("/tarefas/Tarefa%20B")
        
        # 6. Listar novamente (deve ter 1)
        response = client.get("/tarefas")
        assert len(response.json()) == 1
        assert response.json()[0]["nome"] == "Tarefa A"
    
    def test_case_insensitive_busca(self):
        """Testa se a busca é case-insensitive"""
        # Adicionar tarefa
        client.post("/tarefas", json={
            "nome": "Tarefa Teste",
            "descricao": "Test"
        })
        
        # Tentar marcar com case diferente
        response = client.put("/tarefas/tarefa%20teste")  # minúsculas
        
        assert response.status_code == 200
        assert response.json()["tarefa"]["concluida"] == True
    
    def test_multiplas_tarefas_mesmo_status(self):
        """Testa múltiplas tarefas com o mesmo status"""
        # Adicionar várias tarefas
        for i in range(3):
            client.post("/tarefas", json={
                "nome": f"Tarefa {i}",
                "descricao": f"Descrição {i}"
            })
        
        # Marcar primeira como concluída
        client.put("/tarefas/Tarefa%200")
        
        # Listar e verificar
        response = client.get("/tarefas")
        tarefas = response.json()
        
        assert tarefas[0]["concluida"] == True
        assert tarefas[1]["concluida"] == False
        assert tarefas[2]["concluida"] == False

if __name__ == "__main__":
    # Executar os testes
    pytest.main([__file__, "-v"])
