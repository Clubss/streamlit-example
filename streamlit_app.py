import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.write("# Dashboard für: Data Science & Visualisierung")

df = pd.read_csv("capitalbikeshare-complete.csv") 

st.write(df)

tab1, tab2, tab3 = st.tabs(["Häufigkeit der Wetterbedingungen", "Fahrradverleih nach Wetterbedingungen", "Fahrradverleih an Werktagen vs Wochenende"])

with tab1:
  
    weather_counts = df['weather_main'].value_counts()

    plt.figure(figsize=(6, 6))
    bars = sns.barplot(x=weather_counts.values, y=weather_counts.index)

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
