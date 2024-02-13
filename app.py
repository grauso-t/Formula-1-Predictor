from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__, template_folder='./templates', static_folder='./static')

# Caricamento modello regressione e scaler
rf_model = joblib.load('rf_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['POST'])
def handle_data():
    
    # Dizionario per mappare gli ID dei piloti ai loro nomi
    piloti_nomi = {
        1: "Lewis Hamilton",
        3: "Nico Rosberg",
        4: "Fernando Alonso",
        8: "Kimi Räikkönen",
        9: "Robert Kubica",
        13: "Felipe Massa",
        16: "Adrian Sutil",
        18: "Jenson Button",
        20: "Sebastian Vettel",
        154: "Romain Grosjean",
        155: "Kamui Kobayashi",
        814: "Paul di Resta",
        815: "Sergio Pérez",
        817: "Daniel Ricciardo",
        818: "Jean-Éric Vergne",
        820: "Max Chilton",
        821: "Esteban Gutiérrez",
        822: "Valtteri Bottas",
        824: "Jules Bianchi",
        825: "Kevin Magnussen",
        826: "Daniil Kvyat",
        827: "André Lotterer",
        828: "Marcus Ericsson",
        829: "Will Stevens",
        830: "Max Verstappen",
        831: "Felipe Nasr",
        832: "Carlos Sainz",
        833: "Roberto Merhi",
        834: "Alexander Rossi",
        835: "Jolyon Palmer",
        836: "Pascal Wehrlein",
        837: "Rio Haryanto",
        838: "Stoffel Vandoorne",
        839: "Esteban Ocon",
        840: "Lance Stroll",
        841: "Antonio Giovinazzi",
        842: "Pierre Gasly",
        843: "Brendon Hartley",
        844: "Charles Leclerc",
        845: "Sergey Sirotkin",
        846: "Lando Norris",
        847: "George Russell",
        848: "Alexander Albon",
        849: "Nicholas Latifi",
        850: "Pietro Fittipaldi",
        851: "Jack Aitken",
        852: "Yuki Tsunoda",
        853: "Nikita Mazepin",
        854: "Mick Schumacher"
    }

    # Valori inviati dal form
    circuito = request.form.get('circuito')
    meteo = float(request.form.get('meteo').split(",")[0])
    numGiri = int(request.form.get('number-lap'))

    # Valori dei piloti
    piloti_ids = [int(request.form.get(f'pilota{i}')) for i in range(1, len(request.form)+1) if f'pilota{i}' in request.form]

   # Lista tempi totali per ogni pilota
    tempi_totali = []

    # Simulazione giri per ogni pilota
    for pilota_id in piloti_ids:
        pilota_nome = piloti_nomi.get(pilota_id, f"Pilota con ID {pilota_id}")
        tempo_totale = 0
        for giro in range(1, numGiri+1):
            input_data = pd.DataFrame({'driverId': [pilota_id], 'circuitId': [circuito], 'lap': [giro], 'weather_code': [meteo]})
            lap_time = rf_model.predict(input_data)
            tempo_totale += lap_time[0]

        # Conversione tempo_totale in ore:minuti:secondi:decimi
        ore, resto = divmod(tempo_totale / 10, 3600)
        minuti, resto = divmod(resto, 60)
        secondi = resto // 1
        decimi = tempo_totale % 10
        tempo_convertito = f"{int(ore):02d}:{int(minuti):02d}:{int(secondi):02d}.{int(decimi)}"
        tempi_totali.append((pilota_nome, tempo_convertito))

    # Ordina i tempi totali in ordine crescente
    tempi_totali.sort(key=lambda x: x[1])

    # Stampa i tempi totali per ogni pilota
    for pilota_nome, tempo_convertito in tempi_totali:
        print(f"{pilota_nome}: {tempo_convertito}")


    # Restituzione tempi totali ordinati come stringa
    result = "\n".join([f"{pilota}: {tempo}" for pilota, tempo in tempi_totali])
    print(result)

    # Non restituiamo alcuna risposta al client
    return result

if __name__ == '__main__':
    app.run(debug=True)
