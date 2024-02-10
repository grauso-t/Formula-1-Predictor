from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Carica i modelli e lo scaler salvati
rf_model = joblib.load('rf_model.pkl')
svr_model = joblib.load('svr_model.pkl')
mlp_model = joblib.load('mlp_model.pkl')
scaler = joblib.load('scaler.pkl')

# Funzione per fare previsioni
def make_prediction(driverId, circuitId, lap, weather_code):
    input_data = pd.DataFrame({'driverId': [driverId], 'circuitId': [circuitId], 'lap': [lap], 'weather_code': [weather_code]})
    input_data_scaled = scaler.transform(input_data)
    rf_prediction = rf_model.predict(input_data_scaled)[0]
    svr_prediction = svr_model.predict(input_data_scaled)[0]
    mlp_prediction = mlp_model.predict(input_data_scaled)[0]
    return rf_prediction, svr_prediction, mlp_prediction

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    driverId = float(request.form['driverId'])
    circuitId = float(request.form['circuitId'])
    lap = float(request.form['lap'])
    weather_code = float(request.form['weather_code'])
    
    rf_prediction, svr_prediction, mlp_prediction = make_prediction(driverId, circuitId, lap, weather_code)
    
    return jsonify({
        'rf_prediction': rf_prediction,
        'svr_prediction': svr_prediction,
        'mlp_prediction': mlp_prediction
    })

if __name__ == '__main__':
    app.run(debug=True)
