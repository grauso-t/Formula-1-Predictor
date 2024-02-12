from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Caricamento modello regressione e scaler
rf_model = joblib.load('rf_model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['POST'])
def handle_data():
    
    # Dizionario per mappare gli ID dei piloti ai loro nomi
    piloti_nomi = {
        1: "Lewis Hamilton",
        4: "Fernando Alonso",
        20: "Sebastian Vettel",
        807: "Nico Hülkenberg",
        815: "Sergio Pérez",
        817: "Daniel Ricciardo",
        822: "Valtteri Bottas",
        825: "Kevin Magnussen",
        830: "Max Verstappen",
        832: "Carlos Sainz",
        839: "Esteban Ocon",
        840: "Lance Stroll",
        842: "Pierre Gasly",
        844: "Charles Leclerc",
        846: "Lando Norris",
        847: "George Russell",
        848: "Alexander Albon",
        849: "Nicholas Latifi",
        852: "Yuki Tsunoda",
        854: "Mick Schumacher",
        855: "Guanyu Zhou",
        856: "Nyck de Vries",
        857: "Oscar Piastri",
        858: "Logan Sargeant"
    }

    # Valori inviati dal form
    circuito = request.form.get('circuito')
    meteo = float(request.form.get('meteo').split(",")[0])

    # Valori dei piloti
    piloti_ids = [int(request.form.get(f'pilota{i}')) for i in range(1, len(request.form)+1) if f'pilota{i}' in request.form]

    # Lista tempi totali per ogni pilota
    tempi_totali = []

    # Simulazione giri per ogni pilota
    for pilota_id in piloti_ids:
        pilota_nome = piloti_nomi.get(pilota_id, f"Pilota con ID {pilota_id}")
        input_data = pd.DataFrame({'driverId': [pilota_id], 'circuitId': [circuito], 'weather_code': [meteo]})
        scaled_input = scaler.transform(input_data)
        tempo_totale = rf_model.predict(scaled_input)
            
        millisecondi = int(tempo_totale)
        secondi, millisecondi = divmod(millisecondi, 1000)
        minuti, secondi = divmod(secondi, 60)
        millisecondi = f"{millisecondi:03d}"
        tempo_convertito = f"{int(minuti):02d}:{int(secondi):02d}.{millisecondi}"
        tempi_totali.append((pilota_nome, tempo_convertito))


    # Ordina i tempi totali in ordine crescente
    tempi_totali.sort(key=lambda x: x[1])

    # Restituzione tempi totali ordinati come stringa
    result = "\n".join([f"{pilota}: {tempo}" for pilota, tempo in tempi_totali])
    print(result)

    # Non restituiamo alcuna risposta al client
    return result

if __name__ == '__main__':
    app.run(debug=True)
