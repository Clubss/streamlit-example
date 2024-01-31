import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

st.write("# Dashboard für: Data Science & Visualisierung")

df = pd.read_csv("capitalbikeshare-complete.csv") 

st.write(df)

# Definieren Sie eine Liste von 11 Farben
line_colors = ['red', 'blue', 'green', 'yellow', 'black', 'purple', 'orange', 'lime', 'darkgray', 'pink', 'cyan']

tab1, tab2, tab3 = st.tabs(["Häufigkeit der Wetterbedingungen", "Fahrradverleih nach Wetterbedingungen", "Fahrradverleih an Werktagen vs Wochenende"])

with tab1:
  
    weather_counts = df['weather_main'].value_counts()

    plt.figure(figsize=(6, 6))
    bars = sns.barplot(x=weather_counts.values, y=weather_counts.index, palette=line_colors[:len(weather_counts)])

    plt.xlim(0, max(weather_counts.values) * 1.13)

    for bar in bars.patches:
        plt.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f'{int(bar.get_width())}',
            va='center',
        )

    plt.title("Häufigkeit der Wetterbedingungen", fontsize=12, fontweight='bold')
    plt.xlabel('Wie oft ist dieses Wetter aufgetreten?', fontweight='bold')
    plt.ylabel('Wetterbedingungen', fontweight='bold')

    st.pyplot(plt)

with tab2:
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime'].dt.year

    # Daten nach Jahr und Wetterbedingung gruppieren und die Gesamtanzahl der Ausleihen berechnen
    weather_yearly = df.groupby(['year', 'weather_main'])['count'].sum().reset_index()

    # Funktion, um die Y-Achsen-Werte in Millionen umzuwandeln
    def millions_formatter(x, pos):
        return f'{x / 1e6} Mio'

    # Liniendiagramm erstellen und die Farben aus der Liste zuweisen
    plt.figure(figsize=(6, 6))
    sns.lineplot(data=weather_yearly, x='year', y='count', hue='weather_main', palette=line_colors)

    plt.title('Jährliche Fahrradausleihen nach Wetterbedingung', fontweight="bold")
    plt.xlabel('Jahr', fontweight="bold")
    plt.ylabel('Gesamtanzahl der Ausleihen in Millionen', fontweight="bold")
    plt.xticks(df['year'].unique())  # Stellt sicher, dass alle Jahre auf der X-Achse erscheinen
    plt.legend(title='Wetterbedingung', loc='best', fontsize=9)

    # Setzen des Formatters für die Y-Achse
    formatter = FuncFormatter(millions_formatter)
    plt.gca().yaxis.set_major_formatter(formatter)

    plt.tight_layout()  # Passt das Layout an, so dass alles in die Figur passt
    st.pyplot(plt)
