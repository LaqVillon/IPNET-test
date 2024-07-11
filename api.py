from flask import Flask, request, jsonify
import pickle
import xgboost as xgb


# Flask app
flask_app = Flask(__name__)


# Carregando o banco de dados dos features
with open('test.pkl', 'rb') as file:
    test = pickle.load(file)


# Carregando o modelo trainado
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)


@flask_app.route("/predict", methods=["POST"])
def predict():
    try:
        # Verificando se as chaves necessárias estão na solicitação
        if 'shop_id' not in request.json or 'item_id' not in request.json:
            raise KeyError('shop_id and item_id are required')

        # Obteendo e validando shop_id e item_id
        shop_id = int(request.json['shop_id'])
        item_id = int(request.json['item_id'])
        if not (0 <= shop_id <= 59) or not (0 <= item_id <= 22169):
            raise ValueError('Value out of range')

        # Filtraando os dados de teste para o shop_id e item_id fornecidos
        features = test[(test['date_block_num'] == 34) & (test['shop_id'] == shop_id) & (test['item_id'] == item_id)]
        if features.empty:
            raise LookupError('There is no data to provide a prediction')

        # Realizar a predição
        prediction = model.predict(features)
        prediction_rounded = round(prediction[0], 0)
        
        # Preparando os resultados
        result = {
            'prediction': str(prediction_rounded),
            'shop_id': str(shop_id),
            'item_id': str(item_id),
        }
        return jsonify(result)

    except KeyError as e:
        return jsonify({'error': str(e)}), 400

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    except LookupError as e:
        return jsonify({'error': str(e)}), 404

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500


if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', debug=True)
