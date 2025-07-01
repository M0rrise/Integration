from sympy import symbols, sympify, integrate, lambdify
import numpy as np
import matplotlib.pyplot as plt

# Eingabe durch Benutzer
def Eingaben():
    f = input("Geben Sie eine Funktion wie z. B. x**2 ein: ")
    a = float(input("Bitte geben Sie den Anfangswert des Integrals an: "))
    b = float(input("Bitte geben Sie den Endwert des Integrals an: "))
    n = int(input("Anzahl der Teilintervalle n: "))
    methode = input("Methode (rechteck, trapez, simpson, links, rechts, mitte): ").lower()
    return f, a, b, n, methode


# Funktion zum Umwandeln eines eingegebenen Funktions-Strings in eine ausführbare Funktion
def funktion(f):
    x = symbols("x")
    f_sym = sympify(f)
    return lambdify(x, f_sym)

# Mittelpunktsregel (auch Rechteckregel genannt)
def rechteck(f, a, b, n):
    h = (b - a) / n
    summe = 0
    for i in range(n):
        x_i = a + (i + 0.5) * h
        summe += f(x_i)
    return summe * h

# Trapezregel
def trapez(f, a, b, n):
    h = (b - a) / n
    summe = 0.5 * f(a) + 0.5 * f(b)
    for i in range(1, n):
        x_i = a + i * h
        summe += f(x_i)
    return summe * h

# Simpsonsche Regel
def simpson(f, a, b, n):
    if n % 2 != 0:
        n += 1  # n muss gerade sein für Simpsons Regel
    h = (b - a) / n
    summe = f(a) + f(b)
    for i in range(1, n):
        x_i = a + i * h
        faktor = 4 if i % 2 == 1 else 2
        summe += faktor * f(x_i)
    return (h / 3) * summe

# Rechte Rechteckregel
def rechts(f, a, b, n):
    h = (b - a) / n
    summe = 0
    for i in range(1, n + 1):
        x_i = a + i * h
        summe += f(x_i)
    return summe * h

# Linke Rechteckregel
def links(f, a, b, n):
    h = (b - a) / n
    summe = 0
    for i in range(n):
        x_i = a + i * h
        summe += f(x_i)
    return summe * h

# Mittelpunktsregel (nochmals, aber unter anderem Namen)
def mitte(f, a, b, n):
    h = (b - a) / n
    summe = 0
    for i in range(n):
        x_i = a + (i + 0.5) * h
        summe += f(x_i)
    return summe * h



# Zuordnung Methodenname → Funktion
methoden_dict = {
    "rechteck": rechteck,
    "trapez": trapez,
    "simpson": simpson,
    "rechts": rechts,
    "links": links,
    "mitte": mitte
}

# --- Hauptprogramm ---
f_text, a, b, n, methode_name = Eingaben()
f = funktion(f_text)
x = symbols("x")
f_sym = sympify(f_text)
sollwert = float(integrate(f_sym, (x, a, b)))
berechnete_methode = methoden_dict.get(methode_name)

if berechnete_methode is None:
    print(f"Unbekannte Methode: {methode_name}")
    exit()

erg = berechnete_methode(f, a, b, n)
print(f"\nExakter Wert des Integrals von {f_text} auf [{a}, {b}]: {sollwert:.10f}")
print(f"{methode_name.capitalize()}-Ergebnis mit n={n}: {erg:.10f}")
print(f"Fehler: {erg - sollwert:+.5e}\n")

# --- Vergleich verschiedener Methoden mit wachsendem n ---
x_liste = list(range(1, 101))
l_werte, r_werte, m_werte, t_werte, s_werte = [], [], [], [], []

for m in x_liste:
    l_werte.append(links(f, a, b, m))
    r_werte.append(rechts(f, a, b, m))
    m_werte.append(mitte(f, a, b, m))
    t_werte.append(trapez(f, a, b, m))
    s_werte.append(simpson(f, a, b, m))

# --- Plot ---
plt.plot(x_liste, [sollwert] * len(x_liste), label="Sollwert",color="black")
plt.plot(x_liste, l_werte, label="Links",color="green")
plt.plot(x_liste, r_werte, label="Rechts",color="blue")
plt.plot(x_liste, m_werte, label="Mitte",color="orange")
plt.plot(x_liste, t_werte, label="Trapez",color="yellow")
plt.plot(x_liste, s_werte, label="Simpson",color="red")
plt.xlabel("Anzahl der Intervalle")
plt.ylabel("Integralwert")
plt.title(f"Näherung des Integrals von {f_text}")
plt.legend()
plt.grid()
plt.show()

# --- Ausgabe Tabelle ---
print(f"\nWertetabelle für die Funktion {f_text} mit exaktem Wert {sollwert:.10f}")
print(f"Gitter\tRechts\tFehler\t\tLinks\tFehler\t\tMitte\tFehler")
for i in range(len(x_liste)):
    print(f"{x_liste[i]}\t{r_werte[i]:.5f}\t{r_werte[i]-sollwert:+.5e}  "
          f"{l_werte[i]:.5f}\t{l_werte[i]-sollwert:+.5e}  "
          f"{m_werte[i]:.5f}\t{m_werte[i]-sollwert:+.5e}")






