import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter


st.markdown("""
# Willkommen zu meinem Dashboard: Data Science & Visualisierung

Im Rahmen meines Universitätsmoduls für Data Science und Visualisierung präsentiere ich dieses interaktive Dashboard, das Einblicke in die Nutzung von Leihfahrrädern bietet. Ziel ist es, durch Datenvisualisierung komplexe Muster verständlich zu machen.

## Überblick:
- **Balkendiagramm**: Analysiert die Häufigkeit verschiedener Wetterbedingungen.
- **Liniendiagramm**: Zeigt die Fahrradausleihen über die Jahre hinweg.
- **Kreisdiagramm**: Vergleicht die Ausleihen an Wochenenden und Werktagen.
- **Streudiagramm**: Untersucht den Einfluss der Windgeschwindigkeit.
- **Liniendiagramm für Tageszeiten**: Betrachtet die Ausleihen zu verschiedenen Tageszeiten.

""", unsafe_allow_html=True)


df = pd.read_csv("capitalbikeshare-complete.csv") 

st.write(df)

min_wind_speed = df['wind_speed'].min()
max_wind_speed = df['wind_speed'].max()



line_colors = ['red', 'blue', 'green', 'yellow', 'black', 'purple', 'orange', 'lime', 'darkgray', 'pink', 'cyan']



tab1, tab2, tab3, tab4, tab5= st.tabs(["Balkendiagramm", "Liniendiagramm", 
                                 "Kreisdiagramm", 
                                 "Streudiagramm",
                                 "Liniendiagramm"])

with tab1:
  
    st.write("## Wie häufig traten die unterschiedlichen Arten von Wetter auf?")  
  
    weather_counts = df['weather_main'].value_counts()

    plt.figure(figsize=(5, 5))
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
    plt.xlabel('Gesamtanzahl wie häufig das Wetter aufgetreten ist', fontweight='bold')
    plt.ylabel('Wetterbedingungen', fontweight='bold')

    st.pyplot(plt)

with tab2:
    st.write("## Bei welchen Wetterbedingungen wurden die meisten Fahrräder ausgeliehen?")
    
    
    if 'year' not in df:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['year'] = df['datetime'].dt.year

    
    start_year = st.selectbox('Wählen Sie das Startjahr:', sorted(df['year'].unique()), index=0)
    end_year = st.selectbox('Wählen Sie das Endjahr:', sorted(df['year'].unique()), index=len(df['year'].unique())-1)

    
    filtered_yearly_data = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
    weather_yearly = filtered_yearly_data.groupby(['year', 'weather_main'])['count'].sum().reset_index()

    def millions_formatter(x, pos):
        return f'{x / 1e6:.2f} Mio.'

    plt.figure(figsize=(5, 5))
    sns.lineplot(data=weather_yearly, x='year', y='count', hue='weather_main', palette=line_colors)
    plt.title('Jährliche Fahrradausleihen nach Wetterbedingung', fontweight="bold")
    plt.xlabel('Jahr', fontweight="bold")
    plt.ylabel('Gesamtanzahl der Ausleihen in Millionen', fontweight="bold")
    plt.xticks(sorted(filtered_yearly_data['year'].unique()))
    plt.legend(title='Wetterbedingung', loc='best', fontsize=9)

    plt.gca().yaxis.set_major_formatter(FuncFormatter(millions_formatter))

    plt.tight_layout()
    st.pyplot(plt)

        
with tab3:
    st.write("## Waren am Wochenende oder an Werktagen mehr Leihfahrräder unterwegs?")

    df['datetime'] = pd.to_datetime(df['datetime'])
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['weekend'] = df['day_of_week'].apply(lambda x: 'Wochenende' if x >= 5 else 'Werktag')

    weekend_counts = df.groupby('weekend')['count'].sum()

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val_in_millions = total / 1e6  # Umwandlung in Millionen
            val = pct*val_in_millions/100.0  # Berechnung des Werts für das Segment
            return f'{pct:.1f}%\n({val:.2f} Mio. Fahrräder ausgeliehen)'
        return my_autopct

    plt.figure(figsize=(5, 5))
    plt.pie(weekend_counts, labels=weekend_counts.index, autopct=make_autopct(weekend_counts.values), 
            colors=['lightblue', 'lightgreen'], startangle=140)
    plt.title("Anteil der Fahrradausleihen an Wochenenden vs. Werktagen", fontweight="bold")
    st.pyplot(plt)
    
with tab4:
    st.write("## Beeinflussen die Windbedingungen den Fahrradausleih?")

    wind_speed_range = st.slider(
        'Wählen Sie den Windgeschwindigkeitsbereich:',
        min_value=min_wind_speed,
        max_value=max_wind_speed,
        value=(min_wind_speed, max_wind_speed)
    )
    
    filtered_data = df[(df['wind_speed'] >= wind_speed_range[0]) & (df['wind_speed'] <= wind_speed_range[1])]
    wind_speed_counts = filtered_data.groupby('wind_speed')['count'].mean().reset_index()

    plt.figure(figsize=(5, 5))
    sns.scatterplot(data=wind_speed_counts, x='wind_speed', y='count', color='blue')
    plt.title('Einfluss der Windgeschwindigkeit auf Fahrradausleihen', fontweight="bold")
    plt.xlabel('Windgeschwindigkeit (m/s)', fontweight="bold")
    plt.ylabel('Durchschnittliche Anzahl der Ausleihen', fontweight="bold")
    plt.tight_layout()
    st.pyplot(plt)
    
with tab5:
    st.write("## Gibt es bestimmte Tageszeiten zu denen Fahrräder besonders gern ausgeliehen werden?")

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    selected_days = st.multiselect('Wählen Sie die Tage der Woche aus:', days_of_week, default=days_of_week)

    df['day_of_week_name'] = df['datetime'].dt.day_name()

    filtered_data = df[df['day_of_week_name'].isin(selected_days)]

    filtered_data['hour'] = filtered_data['datetime'].dt.hour

    hourly_counts = filtered_data.groupby('hour')['count'].mean().reset_index()

    plt.figure(figsize=(9, 5))
    sns.lineplot(data=hourly_counts, x='hour', y='count', marker="o")
    plt.title('Durchschnittliche Fahrradausleihen nach Tageszeit für ausgewählte Tage', fontweight='bold')
    plt.xlabel('Stunde des Tages', fontweight='bold')
    plt.ylabel('Durchschnittliche Anzahl der Ausleihen', fontweight='bold')
    plt.xticks(range(0, 24))
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)
