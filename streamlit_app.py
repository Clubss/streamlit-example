import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

st.write("# Dashboard für: Data Science & Visualisierung")

df = pd.read_csv("capitalbikeshare-complete.csv") 


min_wind_speed = df['wind_speed'].min()
max_wind_speed = df['wind_speed'].max()



line_colors = ['red', 'blue', 'green', 'yellow', 'black', 'purple', 'orange', 'lime', 'darkgray', 'pink', 'cyan']

tab1, tab2, tab3, tab4= st.tabs(["Balkendiagramm", "Liniendiagramm", 
                                 "Kreisdiagramm", 
                                 "Streudiagramm"])

with tab1:
  
    st.write("## Wie häufig traten die unterschiedlichen Arten von Wetter auf?")  
  
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
    st.write("## Bei welchen Wetterbedingungen wurden die meisten Fahrräder ausgeliehen?")
    
    # Konvertierung der 'datetime' Spalte und Erstellung einer 'year' Spalte, falls noch nicht geschehen
    if 'year' not in df:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['year'] = df['datetime'].dt.year

    # Erstellung von zwei Auswahlboxen für das Start- und Endjahr
    start_year = st.selectbox('Wählen Sie das Startjahr:', sorted(df['year'].unique()), index=0)
    end_year = st.selectbox('Wählen Sie das Endjahr:', sorted(df['year'].unique()), index=len(df['year'].unique())-1)

    # Filtern der Daten basierend auf dem ausgewählten Jahresbereich
    filtered_yearly_data = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
    weather_yearly = filtered_yearly_data.groupby(['year', 'weather_main'])['count'].sum().reset_index()

    # Definieren der millions_formatter Funktion innerhalb von tab2
    def millions_formatter(x, pos):
        return f'{x / 1e6:.2f} Mio.'

    # Liniendiagramm für den ausgewählten Jahresbereich zeichnen
    plt.figure(figsize=(6, 6))
    sns.lineplot(data=weather_yearly, x='year', y='count', hue='weather_main', palette=line_colors)
    plt.title('Jährliche Fahrradausleihen nach Wetterbedingung', fontweight="bold")
    plt.xlabel('Jahr', fontweight="bold")
    plt.ylabel('Gesamtanzahl der Ausleihen in Millionen', fontweight="bold")
    plt.xticks(sorted(filtered_yearly_data['year'].unique()))
    plt.legend(title='Wetterbedingung', loc='best', fontsize=9)

    # Formatter für die Y-Achse anwenden
    plt.gca().yaxis.set_major_formatter(FuncFormatter(millions_formatter))

    plt.tight_layout()
    st.pyplot(plt)

        
with tab3:
    st.write("## Waren am Wochenende oder an Werktagen mehr Leihfahrräder unterwegs?")

    # Datums-/Zeitspalte in datetime umwandeln und den Wochentag extrahieren
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['weekend'] = df['day_of_week'].apply(lambda x: 'Wochenende' if x >= 5 else 'Werktag')

    # Daten aggregieren
    weekend_counts = df.groupby('weekend')['count'].sum()

    # Funktion zum Anzeigen von Prozentsatz und absoluten Werten in Millionen
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val_in_millions = total / 1e6  # Umwandlung in Millionen
            val = pct*val_in_millions/100.0  # Berechnung des Werts für das Segment
            return f'{pct:.1f}%\n({val:.2f} Mio. Fahrräder ausgeliehen)'
        return my_autopct

    # Kreisdiagramm
    plt.figure(figsize=(6, 6))
    plt.pie(weekend_counts, labels=weekend_counts.index, autopct=make_autopct(weekend_counts.values), 
            colors=['lightblue', 'lightgreen'], startangle=140)
    plt.title("Anteil der Fahrradausleihen an Wochenenden vs. Werktagen", fontweight="bold")
    st.pyplot(plt)
    
with tab4:
    st.write("## Beeinflussen die Windbedingungen den Fahrradausleih?")

    # Slider für Benutzer, um den Bereich der Windgeschwindigkeit zu wählen
    wind_speed_range = st.slider(
        'Wählen Sie den Windgeschwindigkeitsbereich:',
        min_value=min_wind_speed,
        max_value=max_wind_speed,
        value=(min_wind_speed, max_wind_speed)
    )
    
    # Daten basierend auf Slider-Auswahl filtern
    filtered_data = df[(df['wind_speed'] >= wind_speed_range[0]) & (df['wind_speed'] <= wind_speed_range[1])]
    wind_speed_counts = filtered_data.groupby('wind_speed')['count'].mean().reset_index()

    # Scatter-Plot mit gefilterten Daten
    plt.figure(figsize=(6, 6))
    sns.scatterplot(data=wind_speed_counts, x='wind_speed', y='count', color='blue')
    plt.title('Einfluss der Windgeschwindigkeit auf Fahrradausleihen', fontweight="bold")
    plt.xlabel('Windgeschwindigkeit (m/s)', fontweight="bold")
    plt.ylabel('Durchschnittliche Anzahl der Ausleihen', fontweight="bold")
    plt.tight_layout()
    st.pyplot(plt)



    
