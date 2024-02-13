const piloti = [
    { name: "Nico Rosberg", value: "3" },
    { name: "Daniel Ricciardo", value: "817" },
    { name: "Kevin Magnussen", value: "825" },
    { name: "Nico Hülkenberg", value: "807" },
    { name: "Fernando Alonso", value: "4" },
    { name: "Jean-Éric Vergne", value: "818" },
    { name: "Kimi Räikkönen", value: "8" },
    { name: "Daniil Kvyat", value: "826" },
    { name: "Jenson Button", value: "18" },
    { name: "Marcus Ericsson", value: "828" },
    { name: "Pastor Maldonado", value: "813" },
    { name: "Sebastian Vettel", value: "20" },
    { name: "Max Chilton", value: "820" },
    { name: "Romain Grosjean", value: "154" },
    { name: "Sergio Pérez", value: "815" },
    { name: "Esteban Gutiérrez", value: "821" },
    { name: "Jules Bianchi", value: "824" },
    { name: "Lewis Hamilton", value: "1" },
    { name: "Valtteri Bottas", value: "822" },
    { name: "Adrian Sutil", value: "16" },
    { name: "Felipe Massa", value: "13" },
    { name: "Kamui Kobayashi", value: "155" },
    { name: "André Lotterer", value: "827" },
    { name: "Will Stevens", value: "829" },
    { name: "Carlos Sainz", value: "832" },
    { name: "Felipe Nasr", value: "831" },
    { name: "Max Verstappen", value: "830" },
    { name: "Roberto Merhi", value: "833" },
    { name: "Alexander Rossi", value: "834" },
    { name: "Jolyon Palmer", value: "835" },
    { name: "Pascal Wehrlein", value: "836" },
    { name: "Rio Haryanto", value: "837" },
    { name: "Stoffel Vandoorne", value: "838" },
    { name: "Esteban Ocon", value: "839" },
    { name: "Lance Stroll", value: "840" },
    { name: "Antonio Giovinazzi", value: "841" },
    { name: "Paul di Resta", value: "814" },
    { name: "Pierre Gasly", value: "842" },
    { name: "Brendon Hartley", value: "843" },
    { name: "Sergey Sirotkin", value: "845" },
    { name: "Charles Leclerc", value: "844" },
    { name: "Lando Norris", value: "846" },
    { name: "Alexander Albon", value: "848" },
    { name: "George Russell", value: "847" },
    { name: "Robert Kubica", value: "9" },
    { name: "Nicholas Latifi", value: "849" },
    { name: "Jack Aitken", value: "851" },
    { name: "Pietro Fittipaldi", value: "850" },
    { name: "Yuki Tsunoda", value: "852" },
    { name: "Mick Schumacher", value: "854" },
    { name: "Nikita Mazepin", value: "853" },
    { name: "Nicholas Latifi", value: "849" },
    { name: "Jack Aitken", value: "851" },
    { name: "Pietro Fittipaldi", value: "850" },
    { name: "Yuki Tsunoda", value: "852" },
    { name: "Mick Schumacher", value: "854" }
];

const circuiti = [
    { name: "Australian Grand Prix", value: "1" },
    { name: "Bahrain Grand Prix", value: "3" },
    { name: "Spanish Grand Prix", value: "4" },
    { name: "Monaco Grand Prix", value: "6" },
    { name: "Canadian Grand Prix", value: "7" },
    { name: "British Grand Prix", value: "9" },
    { name: "Hungarian Grand Prix", value: "11" },
    { name: "Belgian Grand Prix", value: "13" },
    { name: "Italian Grand Prix", value: "14" },
    { name: "Singapore Grand Prix", value: "15" },
    { name: "Brazilian Grand Prix", value: "18" },
    { name: "Emilia Romagna Grand Prix", value: "21" },
    { name: "Japanese Grand Prix", value: "22" },
    { name: "Abu Dhabi Grand Prix", value: "24" },
    { name: "Mexico City Grand Prix", value: "32" },
    { name: "French Grand Prix", value: "34" },
    { name: "Dutch Grand Prix", value: "39" },
    { name: "United States Grand Prix", value: "69" },
    { name: "Austrian Grand Prix", value: "70" },
    { name: "Azerbaijan Grand Prix", value: "73" },
    { name: "Saudi Arabian Grand Prix", value: "77" },
    { name: "Miami Grand Prix", value: "79" }
];

const meteoOptions = [
    { name: "Clear sky", value: ["0", "1"] },
    { name: "Cloudy", value: ["2", "3", "4"] },
    { name: "Rain", value: ["50", "51", "52", "53", "55", "60", "62", "63", "64", "65", "66", "67", "68"] }
];


// Ordinamento array in ordine alfabetico
piloti.sort((a, b) => a.name.localeCompare(b.name));
circuiti.sort((a, b) => a.name.localeCompare(b.name));
meteoOptions.sort((a, b) => a.name.localeCompare(b.name));

// Creazione opzioni per il menu a discesa
function createOptions(container, options) {
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option.value;
        optionElement.textContent = option.name;
        container.appendChild(optionElement);
    });
}

createOptions(document.getElementById('circuito'), circuiti);
createOptions(document.getElementById('meteo'), meteoOptions);

const gridContainer = document.getElementById('grid-container');

for (let i = 0; i < 20; i++) {
    const selectId = 'pilota' + (i + 1);
    const div = document.createElement('div');
    div.className = 'list-view';
    div.innerHTML = `<select name="${selectId}" id="${selectId}" style="color: #7a7a7a;">
                        <option value="" disabled selected">Seleziona un pilota</option>
                      </select>`;

    const select = div.querySelector('select');
    piloti.forEach(pilota => {
        const option = document.createElement('option');
        option.value = pilota.value; // Utilizza il valore del pilota come value
        option.textContent = pilota.name;
        select.appendChild(option);
        select.selectedIndex = 0;
    });

    gridContainer.appendChild(div);
}

// Gestione invio modulo
document.getElementById('data-form').addEventListener('submit', async (event) => {
event.preventDefault(); // Evita il comportamento predefinito del modulo (il refresh della pagina)

// Richiesta POST all'endpoint
const formData = new FormData(document.getElementById('data-form'));
const response = await fetch('/api/data', {
    method: 'POST',
    body: formData
});

if (response.ok) {

    const resultText = await response.text();
    
    // Rimuovi la leaderboard precedente
    const leaderboardDiv = document.getElementById('leaderboard');
    leaderboardDiv.innerHTML = '';

    // Creazione della tabella per la classifica
    leaderboardDiv.style.display = "block";
    const table = document.createElement('table');
    const tableHead = document.createElement('thead');
    const tableBody = document.createElement('tbody');

    // Aggiunta intestazione della tabella
    const headerRow = document.createElement('tr');
    const headerCell1 = document.createElement('th');
    headerCell1.textContent = 'Pilota';
    headerCell1.style.textTransform = 'uppercase';
    headerCell1.style.fontFamily = "'Formula1', Formula1-Regular";
    const headerCell2 = document.createElement('th');
    headerCell2.textContent = 'Tempo Previsto';
    headerCell2.style.textTransform = 'uppercase';
    headerCell2.style.fontFamily = "'Formula1', Formula1-Regular";
    headerRow.appendChild(headerCell1);
    headerRow.appendChild(headerCell2);
    tableHead.appendChild(headerRow);
    table.appendChild(tableHead);

    let i = 1;
    // Aggiunta righe dei risultati alla tabella
    resultText.split('\n').forEach(result => {
        const [pilota, tempo] = result.split(': ');
        const row = document.createElement('tr');
        const cell1 = document.createElement('td');
        cell1.textContent = i + ") " + pilota;
        const cell2 = document.createElement('td');
        cell2.textContent = tempo;
        row.appendChild(cell1);
        row.appendChild(cell2);
        tableBody.appendChild(row);
        i++;
    });

    // Aggiunta del corpo della tabella e stili CSS
    table.appendChild(tableBody);
    table.style.borderCollapse = 'collapse';
    table.style.width = '100%';
    table.style.border = '1px solid #ddd';
    table.style.fontFamily = 'Arial, sans-serif';
    table.style.fontSize = '16px';

    // Aggiunta della tabella alla leaderboardDiv
    leaderboardDiv.appendChild(table);
    window.scrollTo(0, document.body.scrollHeight);
} else {
    console.error('Errore durante il recupero dei dati:', response.statusText);
}
});

function rimuoviTabella() {
    const leaderboardDiv = document.getElementById('leaderboard'); // Ottieni l'elemento leaderboard
    const table = leaderboardDiv.querySelector('table'); // Ottieni l'elemento della tabella all'interno di leaderboardDiv

    if (table) {
        leaderboardDiv.removeChild(table); // Rimuovi la tabella se esiste
    }
    leaderboardDiv.style.display = "none";
}

const selects = document.querySelectorAll('#grid-container select');

function resetSelects() {
    selects.forEach(select => {
        select.selectedIndex = 0; // Imposta l'opzione predefinita
        select.style.border = 'solid 2px #000000';
        select.style.color = '#7a7a7a';
        rimuoviTabella();
    });
}

function randomSelects() {
    const opzioniTotali = 24;
    const selezionati = new Set();
    
    // Imposta gli elementi selezionati nei select
    selects.forEach(select => {
        select.style.border = 'solid 2px #ef0000';
        select.style.color = '#000000';
        // Otteniamo tutte le opzioni disponibili nel select
        const opzioniDisponibili = Array.from(select.options).filter(option => option.value !== "");
        
        // Genera 20 numeri casuali univoci da 1 a 24 per ogni select
        while (selezionati.size < 20) {
            let numeroCasuale = Math.floor(Math.random() * opzioniTotali) + 1;
            if (!selezionati.has(numeroCasuale)) {
                selezionati.add(numeroCasuale);
                let opzioneCasuale = opzioniDisponibili[numeroCasuale - 1];
                opzioneCasuale.selected = true;
                break;
            }
        }
    });
}

// Aggiungi un listener per l'evento change a ciascun select
selects.forEach(select => {
    select.addEventListener('change', () => {
        if (select.textContent !== "Seleziona un pilota") {
            // Se è stato selezionato un pilota diverso da "Seleziona un pilota", imposta il bordo a #ef0000
            select.style.border = 'solid 2px #ef0000';
            select.style.color = '#000000';
        } else {
            // Altrimenti, reimposta il colore del bordo al valore predefinito
            select.style.border = 'solid 2px #000000';
            select.style.color = '#7a7a7a';
        }
    });
});

var inputElement = document.getElementById('number-lap');

    // Imposta il valore predefinito a 0
    inputElement.value = '1';

    // Aggiungi un listener per gestire l'input e garantire solo numeri positivi
    inputElement.addEventListener('input', function() {
        if (this.value < 0) {
            this.value = 0;
        }
        if (this.value > 100) {
            this.value = 100;
        }
    });