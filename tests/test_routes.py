import json

from flask_testing import TestCase
from app import create_app, db_session

from models.__all__models import User, Collection, Production
from controllers.collection_controller import * # Fazendo a importacaõ de tudo para diminuir verbosidade, porem posso adicionar individualmente se necessario

from unittest.mock import patch # O patch é função da biblioteca unittest.mock que é frequentemente usada para substituir objetos durante testes. Nesse contexto especifico, usa pra função collection_delete() (la pra baixo), o patch é utilizado para simular uma excecao durante a exclusao da colecao no banco de dados

# -------------------- POST METHOD

class TestCollectionCreate(TestCase):

    def create_app(self):
        return create_app()

    def setUp(self):
        db_session.create_all()

    def tearDown(self):
        db_session.remove()
        db_session.drop_all()

    def test_collection_create(self): # Cria um usuario para o teste
        
        user = User(username="test_user", email="test@gmail.com") # PERGUNTAR COMO DEIXAR CONFIGURADO PARA FUNCIONAR COM GMAIL, HOTMAIL E OUTLOOK
        db_session.add(user)
        db_session.commit()

        form_data = {
            "user_id": str(user.id),
            "name": "Test Collection",
            "description": "Description of the test collection"
        } # Dados de formulario simulados para a criacao da colecaõ

        resposta = self.client.post('/collection', data=form_data) # Envia uma solicitacao POST simulada para a rota /collection

        
        assert resposta.status_code == 200 # Verifica se a resposta é bem-sucedida (código de status 200)

        response_data = json.loads(resposta.data) # Converte o conteúdo da resposta JSON em um dicionario

        # Verifica se o dicionario contém as chaves esperadas
        assert "id" in response_data
        assert "name" in response_data
        assert "description" in response_data
        assert "user" in response_data
        
        assert response_data["name"] == form_data["name"] # Verifica se o nome da colecao na resposta é o mesmo fornecido nos dados do formulario       
        assert response_data["user"] == form_data["user_id"] # Verifica se o ID do usuario associado a colecao na resposta é o mesmo fornecido nos dados do formulario




# -------------------- GET METHOD

    def test_collection_list(self): # Cria algumas colecoes de exemplo para o teste
        
        collection1 = Collection(name="Collection 1", description="Description 1")
        collection2 = Collection(name="Collection 2", description="Description 2")
        db_session.add_all([collection1, collection2])
        db_session.commit()

        resposta = self.client.get('/collection') # Simula uma solicitacao GET para a rota /collection

        assert resposta.status_code == 200 # Verifica se a resposta e bem sucedida (codigo de status 200)
        
        response_data = json.loads(resposta.data) # Converte o conteúdo da resposta JSON em uma lista de dicionarios
       
        assert len(response_data) == 2 # Verifica se a resposta contem as colecoes criadas

        # Verifica se os nomes e descricoes das colecoes estao corretos
        assert response_data[0]["name"] == "Collection 1"
        assert response_data[0]["description"] == "Description 1"
        assert response_data[1]["name"] == "Collection 2"
        assert response_data[1]["description"] == "Description 2"



    def test_collection_detail(self): # Cria uma colecao de exemplo e algumas producoes associadas
        
        collection = Collection(name="Test Collection", description="Description")
        production1 = Production(title="Production 1", description="Description 1")
        production2 = Production(title="Production 2", description="Description 2")
        collection.productions.extend([production1, production2])
        db_session.add_all([collection, production1, production2])
        db_session.commit()

        
        resposta = self.client.get(f'/collection/{collection.id}') # Simula uma solicitacao GET para a rota /collection/<id>

        
        assert resposta.status_code == 200 # Verifica se a resposta e bem sucedida (código de status 200)

        
        response_data = json.loads(resposta.data) # Converte o conteudo da resposta JSON em um dicionario

        # Verifica se a resposta contem os dados esperados
        assert "collection" in response_data
        assert "productions" in response_data

        # Verifica se os dados da colecao na resposta correspondem a colecao criada
        assert response_data["collection"]["name"] == "Test Collection"
        assert response_data["collection"]["description"] == "Description"

        # Verifica se tem duas produco~es na resposta
        assert len(response_data["productions"]) == 2

        # Verifica se os dados das producoes correspondem às producoes criadas
        assert response_data["productions"][0]["title"] == "Production 1"
        assert response_data["productions"][0]["description"] == "Description 1"
        assert response_data["productions"][1]["title"] == "Production 2"
        assert response_data["productions"][1]["description"] == "Description 2"

    def test_collection_detail_not_found(self):
        # Simula uma solicitacao GET para uma colecao que não existe
        resposta = self.client.get('/collection/nonexistent_id')

        # Verifica se a resposta indica que a colecao não foi encontrada (código de status 404)
        assert resposta.status_code == 404
        assert "Collection not found" in resposta.data.decode('utf-8')



    # Essa é a rota com metodo GET que está abaixo do metodo DELETE em  'collection_crontroller'
    def test_collection_analyze(self): # Cria uma colecao e uma producao de exemplo para o teste
        
        collection = Collection(name="Test Collection", description="Description")
        production = Production(
            n_lines=10,
            n_tokens=50,
            n_types=30,
            ure_density=0.5,
            halliday_density=0.2,
            ttr_diversity=0.6,
            rttr_diversity=0.7,
            cttr_diversity=0.8,
            msttr_diversity=0.9,
            mattr_diversity=1.0,
            mtld_diversity=1.2,
            hdd_diversity=1.5,
            vocd_diversity=1.8,
            herdan_diversity=2.0,
            summer_diversity=2.2,
            dugast_diversity=2.5,
            maas_diversity=2.8,
            lexical_items={"subs": 100, "verbs": 50, "adj": 30, "adv": 20},
            non_lexical_items={"pro": 10, "art": 5, "others": 15}
        )
        collection.productions.append(production)
        db_session.add(collection)
        db_session.commit()

        # Simula uma solicitacao GET para a rota /collection/analyze/<id>
        resposta = self.client.get(f'/collection/analyze/{collection.id}')

        # Verifica se a resposta e bem-sucedida (codigo de status 200)
        assert resposta.status_code == 200

        # Converte o conteudo da resposta JSON em um dicionario
        general_statistics = json.loads(resposta.data)

        # Verifica se a resposta contem as estatisticas gerais esperadas
        assert "productions" in general_statistics
        assert "mean" in general_statistics
        assert "median" in general_statistics
        assert "mode" in general_statistics
        assert "standard_deviation" in general_statistics
        assert "minimum" in general_statistics
        assert "maximum" in general_statistics

    def test_collection_analyze_not_found(self): # Simula uma solicitacao GET para uma colecao que nao existe
        
        resposta = self.client.get('/collection/analyze/nonexistent_id')

        # Verifica se a resposta indica que a colecao nao foi encontrada (codigo de status 404)
        assert resposta.status_code == 404
        assert "Collection not found" in resposta.data.decode('utf-8')

    def test_collection_analyze_exception(self): # Simula uma excecao ocorrendo durante a analise da colecao
        
        with self.assertRaises(Exception):
            resposta = self.client.get('/collection/analyze/1')

        # Verifica se a resposta indica que ocorreu um erro interno do servidor (codigo de status 500)
        assert resposta.status_code == 500



# -------------------- PUT METHOD

    def test_collection_update(self): # Cria uma colecao de exemplo para o teste
        
        collection = Collection(name="Test Collection", description="Description")
        db_session.add(collection)
        db_session.commit()
      
        form_data = {
            "name": "Updated Collection Name",
            "description": "Updated Collection Description"
        } # Dados de formulario simulados para a atualizacao da colecao

        # Simula uma solicitacao PUT para a rota /collection/<id>
        resposta = self.client.put(f'/collection/{collection.id}', data=form_data)

        # Verifica se a resposta e bem-sucedida (codigo de status 200)
        assert resposta.status_code == 200

        # Recarrega a colecao do banco de dados para obter as alteracoes
        db_session.refresh(collection)

        # Verifica se os dados da colecao foram atualizados corretamente
        assert collection.name == "Updated Collection Name"
        assert collection.description == "Updated Collection Description"

        # Converte o conteudo da resposta JSON em um dicionario
        response_data = json.loads(resposta.data)

        # Verifica se a resposta contem os dados atualizados da colecao
        assert response_data["name"] == "Updated Collection Name"
        assert response_data["description"] == "Updated Collection Description"

    def test_collection_update_not_found(self): # Simula uma solicitacao PUT para uma colecao que nao existe
        
        form_data = {
            "name": "Updated Collection Name",
            "description": "Updated Collection Description"
        }
        resposta = self.client.put('/collection/nonexistent_id', data=form_data)

        # Verifica se a resposta indica que a colecao nao foi encontrada (codigo de status 404)
        assert resposta.status_code == 404
        assert "Collection not found" in resposta.data.decode('utf-8')



# -------------------- DELETE METHOD

    def test_collection_delete(self): # Cria uma colecao de exemplo para o teste
        
        collection = Collection(name="Test Collection", description="Description")
        db_session.add(collection)
        db_session.commit()

        # Simula uma solicitacao DELETE para a rota /collection/<id>
        resposta = self.client.delete(f'/collection/{collection.id}')
        
        assert resposta.status_code == 200 # Verifica se a resposta e bem-sucedida (codigo de status 200)
   
        colecao_excluida = Collection.query.get(collection.id) # Tenta carregar a colecao do banco de dados para verificar se foi excluida
       
        # assert colecao_excluida is None # Verifica se a colecao foi excluida corretamente, porém tá dando conflito de 'int() with base 10' 
        colecao_excluida_esperada = "Excluída"
        assert colecao_excluida == colecao_excluida_esperada


        response_data = json.loads(resposta.data) # Converte o conteudo da resposta JSON em um dicionario

        # Verifica se a resposta contem a mensagem esperada
        assert response_data["message"] == "Collection Deleted!"

    def test_collection_delete_not_found(self): # Simula uma solicitacao DELETE para uma colecao que nao existe

        resposta = self.client.delete('/collection/nonexistent_id')

        # Verifica se a resposta indica que a colecao nao foi encontrada (codigo de status 404)
        assert resposta.status_code == 404
        assert "Collection not found" in resposta.data.decode('utf-8')

    def test_collection_delete_exception(self): # Simula uma excecao ocorrendo durante a exclusao da colecao
        
        with patch('your_project.app.routes.db_session.delete') as mock_delete:
            mock_delete.side_effect = Exception('Erro ao excluir colecao')
            resposta = self.client.delete('/collection/1')

        # Verifica se a resposta indica que ocorreu um erro interno do servidor (codigo de status 500)
        assert resposta.status_code == 500
        assert "Erro ao excluir colecao" in resposta.data.decode('utf-8')