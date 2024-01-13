import pandas as pd
import streamlit as st

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                             #
# Onderdeel van de Streamlit presentatie voor de Hogeschool Utrecht, AI Gilde.                #
#                                                                                             #
# Gemaakt door: Sid van Vliet                                                                 #
# Gebruikte: https://kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020/data #
#                                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Hier laden we alle data in
df = pd.read_csv("data/pit_stops.csv")
drivers_df = pd.read_csv("data/drivers.csv")

# We selecteren alleen de races uit 2022, omdat we daarvan zeker weten dat ze allemaal data hebben
races_2022_df = pd.read_csv("data/races.csv")
races_2022_df = races_2022_df[races_2022_df['year'] == 2022]

# F1 logo
st.image("assets/F1.png", width=200)

# Hier maken we een selection box aan, opgebouwd met 't ID van de race, naam en het jaar
selected_race = st.selectbox(
    "Selecteer een race uit 2022:", races_2022_df[['raceId', 'name', 'year']].apply(
        lambda x: f"{x['name']} {x['year']} (#{x['raceId']})",
        axis=1
    )
)

# Je kunt in Streamlit d.m.v. een if-statement een callback toevoegen aan het gebruik van een button
if st.button("Race selecteren"):
    # We pakken hier de ID race de race uit de geselecteerde optie
    selected_raceId = int(selected_race.split("(#")[1].split(")")[0])
    st.divider()

    # Hier selecteren we enkel de kolommen van de race met het geselecteerde ID
    race_data = df[df['raceId'] == selected_raceId]

    # Hier pakken we de snelste pitstop per coureur
    race_data['duration'] = pd.to_numeric(
        race_data['duration'], errors='coerce')
    best_pitstops = race_data.groupby('driverId')['duration'].idxmin()

    best_pitstops_df = race_data.loc[best_pitstops]
    best_pitstops_df = pd.merge(best_pitstops_df, drivers_df[[
                                'driverId', 'forename', 'surname']], on='driverId', how='left')
    best_pitstops_df = best_pitstops_df.sort_values(by='duration')

    # En om af te sluiten laten we de titel zien en een bar chart met de snelste pitstops
    grand_prix_title = selected_race.split("2022")[0]
    st.title(f"De snelste pitstops tijdens de {grand_prix_title}")
    st.write("")

    st.bar_chart(
        best_pitstops_df[['driverId', 'duration']].set_index('driverId'))

    # En een tabel waar we de gebruikte waarden terug kunnen vinden
    st.table(
        best_pitstops_df[['driverId', 'forename', 'surname', 'duration']])
