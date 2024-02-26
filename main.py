import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# Datenbankverbindung herstellen und Tabelle erstellen, falls noch nicht vorhanden
def init_db():
    conn = sqlite3.connect('finanzen.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transaktionen
                 (id INTEGER PRIMARY KEY, typ TEXT, betrag REAL, kategorie TEXT, datum TEXT)''')
    conn.commit()
    conn.close()

# Neue Transaktion hinzufügen
def transaktion_hinzufuegen(typ, betrag, kategorie, datum):
    conn = sqlite3.connect('finanzen.db')
    c = conn.cursor()
    c.execute("INSERT INTO transaktionen (typ, betrag, kategorie, datum) VALUES (?, ?, ?, ?)",
              (typ, betrag, kategorie, datum))
    conn.commit()
    conn.close()

# Alle Transaktionen anzeigen
def transaktionen_anzeigen():
    conn = sqlite3.connect('finanzen.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM transaktionen'):
        print(row)
    conn.close()

# Transaktion löschen
def transaktion_loeschen(id):
    conn = sqlite3.connect('finanzen.db')
    c = conn.cursor()
    c.execute("DELETE FROM transaktionen WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Transaktion mit der ID {id} wurde gelöscht.")


def ausgaben_diagramm_anzeigen():
    conn = sqlite3.connect('finanzen.db')
    c = conn.cursor()
    c.execute("SELECT kategorie, SUM(betrag) FROM transaktionen WHERE typ='Ausgabe' GROUP BY kategorie")
    daten = c.fetchall()
    conn.close()

    kategorien = [row[0] for row in daten]
    betraege = [row[1] for row in daten]

    plt.figure(figsize=(10, 7))
    plt.pie(betraege, labels=kategorien, autopct='%1.1f%%', startangle=140)
    plt.title('Ausgaben nach Kategorie')
    plt.axis('equal')  # Kreisdiagramm
    plt.show()

if __name__ == '__main__':
    init_db()
    while True:
        aktion = input("Was möchten Sie tun? [Hinzufügen, Anzeigen, Löschen, Diagramm, Beenden]: ").lower()
        if aktion == 'beenden':
            break
        elif aktion == 'hinzufügen':
            typ = input("Typ (Einnahme/Ausgabe): ")
            betrag = float(input("Betrag: "))
            kategorie = input("Kategorie: ")
            datum = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transaktion_hinzufuegen(typ, betrag, kategorie, datum)
        elif aktion == 'anzeigen':
            transaktionen_anzeigen()
        elif aktion == 'löschen':
            id = int(input("Geben Sie die ID der zu löschenden Transaktion ein: "))
            transaktion_loeschen(id)
        elif aktion == 'diagramm':
            ausgaben_diagramm_anzeigen()