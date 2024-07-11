# Teste Técnico

## Entendendo o objetivo e o problema de negócio

A partir de dados históricos diários de vendas de lojas e produtos, devemos prever o total de produtos vendidos em cada loja e item para o conjunto de teste.

O notebook [test-eda.ipynb](test-eda.ipynb) mostra os principais insights do banco de dados de treino, o tratamento necessário dos dados e os seguintes passos a seguir antes de criar o API Flask.

### Seleção de características e modelo de regressão

Visto que os dados de vendas seguem uma série temporal, consideramos que uma forma apropriada de tratar o problema é mediante a criação de "lag features".

O modelo de regressão utilizado foi o XGboost dada a sua alta performance, tanto no tempo de execução quanto na corretude. Além disso, um modelo baseado em árvore de decisão é uma escolha interessante visto que temos um dataset estruturado e algumas features categóricas.

### Validação e persistência do modelo

Utilizamos uma validação em splits consecutivos no tempo porque queremos treinar dados do passado para prever dados do futuro.

A persistência do modelo foi implementada mediante pickle. Foram salvos tanto o modelo quanto os dados dos features adicionais criados.

## Uso de API Flask e Docker

Para usar o modelo criado em ambiente produção, implementamos um API Flask no script [api.py](api.py). 

Criamos e rodamos o container por meio do comando:

```
docker compose up --build
```

Para realizar uma requisição, é necessário ter acesso a outro terminal local. Como exemplo, para realizar uma requisição utilizamos o comando:

```
curl -X POST -H "Content-Type: application/json" -d '{"shop_id": 55, "item_id": 10585}' http://0.0.0.0:5000/predict
```

Neste exemplo, o terminal deve mostrar:
```
{
  "item_id": "10585",
  "prediction": "1.0",
  "shop_id": "55"
}
```

A previsão de vendas é de 1 unidade para esse produto e loja no mês de novembro de 2015.

### Requisitos do projeto completo:
  - flask 3.0.3
  - pandas 2.2.2
  - scikit-learn 1.4.2
  - numpy 1.26.4
  - seaborn 0.13.2
  - matplotlib 3.8.4
  - xgboost 2.1.0
