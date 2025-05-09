import streamlit as st
import pandas as pd
from datetime import datetime, date
from PIL import Image
import PIL
import plotly.express as px

from streamlit_extras.stylable_container import stylable_container

# Page configuration
st.set_page_config(
    page_title="uni-assist: Monitoring",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for width constraint and styling
st.markdown("""
    <style>
        .reportview-container .main .block-container {
            max-width: 1000px;
            padding-top: 2rem;
            padding-bottom: 2rem;
            background-color: grey;
        }
        h1 {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .stImage {
            margin: 1rem 0;
        }
        .highlight {
            padding: 1rem;
            margin: 1rem 0;
        }
        .gray-section {
            background-color: #dbd9d9;
            padding: 1rem;
            margin: 1rem 0;
            height: 10px
        }
        .yellow-section {
            background-color: #ffe163;
            padding: 20px;
            margin: 20px 0;
        }
    </style>
""", unsafe_allow_html=True)

TODAY_tmp = datetime.today().date()
decr = 1
if TODAY_tmp.weekday()==0:
    decr = 3
TODAY     = datetime(TODAY_tmp.year,TODAY_tmp.month,TODAY_tmp.day-decr).date()

heute =  TODAY.strftime("%d.%m.%Y")

# Title section with yellow background
st.markdown(f"""<div class="yellow-section"><h4><b>Monitoring WSV 2025/26</b>: {heute} (Stichtag)</h4></div>""", unsafe_allow_html=True)

# logo-uniassist-newsletter.png
image_logo = Image.open("uni-assist_nur_logo.png")
w = int(0.35*(image_logo.width))
h = int(0.35*(image_logo.height))
image_logo = image_logo.resize((w,h)) 
st.image(image_logo)

image = Image.open('ua_img.png')
image_green = Image.open('traffic-light-green.png')
image_red = Image.open('red.png')
image_yellow = Image.open('yellow.png')

h = 110 #int(0.145*(image_green.height))
w = int(0.25*(image_green.width))
image_green = image_green.resize(size=(w,h))
#

sem_agg_df = pd.read_csv("antrag_nach_semester_agg.csv",sep=";")
ldf1 = sem_agg_df[sem_agg_df.Semester=="WS 2025"]
ldf2 = sem_agg_df[sem_agg_df.Semester=="WS 2024"]
act_antraege = ldf1.Antragsnummer.iat[0]-ldf1["zurückgezogen"].iat[0]
alt_antraege = ldf2.Antragsnummer.iat[0]-ldf2["zurückgezogen"].iat[0]

print(ldf1 )
print(act_antraege )
print(ldf2 )
print(alt_antraege)

diff1 = round(100.0*round(abs(act_antraege-alt_antraege)/alt_antraege, 2),2)
#act_weiter_antraege = ldf1["weiterleiten"].iat[0]
#alt_weiter_antraege = ldf2["weiterleiten"].iat[0]

act_bearb_antraege = ldf1["weitergeleitet"].iat[0]
alt_bearb_antraege = ldf2["weitergeleitet"].iat[0]

print("***act_bearb_antraege:",act_bearb_antraege)
print("***alt_bearb_antraege:",alt_bearb_antraege)
    
diff2 = round(100.0*abs(act_bearb_antraege-alt_bearb_antraege)/alt_bearb_antraege, 2)
act_fehlerhaft = ldf1["fehlerhaft"].iat[0]
alt_fehlerhaft = ldf2["fehlerhaft"].iat[0]

image = Image.open('ua_img.png')
image_green = Image.open('traffic-light-green.png')
image_red = Image.open('red.png')
image_yellow = Image.open('yellow.png')

h = int(0.09*(image_green.height))
w = int(0.25*(image_green.width))
image_green = image_green.resize(size=(w,h))

col01, col02 = st.columns([1, 10])

with col02:
    st.image(image)

with stylable_container(
        key="container_with_border1",
        css_styles="""
            {
                width = 900px

                border-color: red;
                padding: calc(1em);
                background-color: #F1F3F4;            
            }
            """,
    ):
    st.header("Einführung")
    st.markdown(f"""
            <p style='font-size:16px; margin-bottom:10px; margin-left:10px;margin-right:10px; white-space: normal;'>
Dieses Dashboard zeigt die Fortschritte des laufenden ua-Semesterverfahrens.
Dargestellt werden in fünf Grafiken zentrale Indikatoren der Zulassungsvorbereitung im Verein.
Sie sollen den Mitgliedern dabei helfen, die eigenen Zulassungsverfahren adäquat zu planen und vorzubereiten.
</p>
<p style='font-size:16px; margin-bottom:10px; margin-left:10px;margin-right:10px; white-space: normal;'>
Eine Ampelanzeige dokumentiert das Verfahrensrisiko nach Einschätzung der Geschäftsstelle:
</p>
<p style='font-size:16px; margin-bottom:10px; margin-left:10px;margin-right:10px; white-space: normal;'>
<table border="none"  bgcolor="#F1F3F4" width="95%">
    <tr border="none" ><td align="left" colspan="3" border="none">Bearbeitung eingegangener Studienbewerbungen in allen Länderbereichen binnen sechs Wochen</td>
    <td align="left" colspan="1" ><font color="green">Grün</font></td>
    </tr>
    <tr><td align="left" colspan="3">Bearbeitung eingegangener Studienbewerbungen in einzelnen Länderbereichen zwischen sechs und acht Wochen</td>
    <td align="left" colspan="1" ><font color="#FFBF00">Gelb</font></td>
    </tr>
    <tr><td align="left" colspan="3">Bearbeitung eingegangener Studienbewerbungen in einzelnen Länderbereichen  über acht Wochen</td>
    <td align="left" colspan="1" ><font color="red">Rot</font></td>
    </tr>
</p>
        """, unsafe_allow_html=True)
    
    # Main statistics section
    # Create three columns for KPIs
    
    
    st.header("Verfahrensstand zum Stichtag")
    col1, col2, col3= st.columns(3)

    act_antraege=f"{act_antraege:,}"
    act_antraege=act_antraege.replace(",", ".")
    
    alt_antraege=f"{alt_antraege:,}"
    alt_antraege=alt_antraege.replace(",", ".")
    
    print("xxxxxxact_bearb_antraege:",act_bearb_antraege)
    print("xxxxxxalt_bearb_antraege:",alt_bearb_antraege)
    
    act_bearb_antraege=f"{act_bearb_antraege:,}"
    act_bearb_antraege=act_bearb_antraege.replace(",", ".")
    
    alt_bearb_antraege=f"{alt_bearb_antraege:,}"
    alt_bearb_antraege=alt_bearb_antraege.replace(",", ".")
    
    print("zzzzzzact_bearb_antraege:",act_bearb_antraege)
    print("zzzzzzalt_bearb_antraege:",alt_bearb_antraege)
    
    act_fehlerhaft=f"{act_fehlerhaft:,}"
    act_fehlerhaft=act_fehlerhaft.replace(",", ".")
    
    print("act_antraege:",act_antraege)
    print("alt_antraege:",alt_antraege)
    print("act_bearb_antraege:",act_bearb_antraege)
    print("alt_bearb_antraege:",alt_bearb_antraege)
    
    with col1:
        st.metric(label="Anträge (Eingang)", 
                        value=f"{act_antraege}",
                        delta=f"-{diff1}% zum Vorjahr", border=True)

    with col2:
        st.metric(label="Anträge (Weitergeleitet)",
                value=f"{act_bearb_antraege}",
                delta=f"+{diff2}% zum Vorjahr", border=True)

    with col3:
        with st.container(border=True, height=127):
            st.image(image_green)
        st.markdown("<p style='font-size:14px; margin-top:1px; margin-left:10px;margin-right:1px; white-space: normal;'> Abb. 1: Status - <font color='green'><b>Grün</b></font></p>", unsafe_allow_html=True)

    #with st.markdown('<div>', unsafe_allow_html=True):
    st.markdown(f"""
            <p style='font-size:16px; margin-bottom:10px; margin-left:10px;margin-right:10px; white-space: normal;'><b><i>
            uni-assist-Geschäftssstelle Berlin, {heute}:</i></b>
            </p>
            <p style='font-size:16px; margin-bottom:10px; margin-left:10px;margin-right:10px; white-space: normal;'>
            Der Eingang von Studienbewerbungen aus aller Welt liegt zum Stichtag gegenüber dem Vorjahr <br>noch leicht zurück. 
            Von den wichtigsten zehn Herkunftsländern liegen zwischenzeitlich nur Bangladesch und Pakistan gegenüber dem Vorjahr deutlicher zurück. Die übrigen <br>TOP Herkunftsländer, v.a. Ghana und die Türkei, weisen bereits Überschüsse gegenüber dem Vorjahr aus und lassen einen weiteren Zuwachs in 2025 erwarten. 
            </p>
            <p style='font-size:16px; margin-bottom:10px; margin-left:10px;margin-right:10px; white-space: normal;'>
            In der Bearbeitung von Studienbewerbungen kam die Geschäftsstelle absolut wie relativ deutlich zügiger voran als im Vorjahr: Mit beinahe 8% mehr bearbeiteten Studienbewerbungen liegt das aktuelle ToDo erheblich unter dem des Vorjahres, die durchschnittliche Bearbeitungszeit aktuell <br> bei 3 Wochen.
            </p>
            <p style='font-size:16px; margin-bottom:10px; margin-left:10px;margin-right:10px; white-space: normal;'>
            Auch wenn der Eingang an Studienbewerbungen absolut noch leicht zurück liegt, deutet die Entwicklung der Bewerbungseingänge an, dass der Rückstand in den kommenden Wochen durchaus ausgeglichen und in ein Wachstum gedreht werden kann.
            </p>
            
            <p style='font-size:16px; margin-bottom:10px; margin-left:10px;margin-right:10px; white-space: normal;'>
            Eine Deutung der Gewinne und Verluste nach Herkunftsländern ist  früh im Verfahren wenig aussagekräftig.
            </p>
        """, unsafe_allow_html=True)

as_df = pd.read_csv("status_df.csv",sep=";")

print(as_df)
print("=====================================")
with stylable_container(
        key="container_with_border2",
        css_styles="""
            {
                width = 900px

                border-color: red;
                padding: calc(1em);
                background-color: "#F2F2F2"; 
        
            }
            """,
    ):
        # Create pie chart
        print(as_df)
        
        fig = px.pie(as_df,  values='Antraege', names='Status', title=f"Abb. 2: Kuchengrafik Anträge", color_discrete_sequence=['#808080', '#c9aa4c', '#800020']  # uni-assist colors
        )
        fig.update_traces(sort=False,title_position='top center',textinfo='percent+value', selector=dict(type='pie')) 
        # Update layout
        fig.update_layout(

            font_family="Ubuntu, Helvetica, Arial, sans-serif",
             title={
                'y': 0.98,
                'x': 0.4,
                'xanchor': 'right',
                'yanchor': 'top', 
                },
            titlefont={
                'size': 20
                },
            
            autosize=False,
            width=800,
            height=500,
            legend=dict( orientation="h", y=-0.13,  yanchor="bottom", xanchor="left"),
            #plot_bgcolor= "#F2F2F2",
            #paper_bgcolor="#F2F2F2",
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=False)
        
        st.markdown(f"""           
            <p style='font-size:16px; margin-bottom:10px; margin-left:10px;margin-right:10px; white-space: normal;'>
            Das Kuchendiagramm zeigt in absoluten Zahlen und prozentualen Anteilen das Aufkommen an Studienbewerbungen zum Stichtag sowie die Arbeitsfortschritte.
            </p>
        """, unsafe_allow_html=True)

st.divider()
with stylable_container(
        key="container_with_border3",
        css_styles="""
            {
                width = 900px

                border-color: red;
                padding: calc(1em);
                background-color: white;
                    
            }
            """,
    ):
        # Main statistics section
        # Create three columns for KPIs

        st.header("Bewerbungseingang")
        #with st.markdown('<div>', unsafe_allow_html=True):
        #st.markdown(f"""
        #        <p style='font-size:16px; margin-bottom:10px; margin-left:10px;margin-right:10px; white-space: normal;'>
         #       Die Berliner Geschäftsstelle hat im Vergleich zum WSV 2024 bisher kein Wachstum an eingegangenen #Studienbewerbungen zu verzeichnen. Die Bearbeitung geht schneller im Vergleich zum WSV 2024 zum gleichem Zeitpunkt.
               # </p>


        #    """, unsafe_allow_html=True)

# Applications data

kw_df = pd.read_csv("antrag_nach_Eingangswoche_agg.csv",sep=";")

xsticks = [f"Kw{x}" for x in list(kw_df.Eingangswoche.values)]

fig = px.bar(kw_df,x=xsticks, y = ["WS 2024","WS 2025"], 
       labels={'x': 'Eingangswoche', 'value':'Anträge', 'variable':'Semester'},
        barmode="group", title=f"Abb. 3: Doppelbalken-Grafik Bewerbungseingang nach KW (am Stichtag)",template="gridon", 
                    height=500, range_y=[0,15000])

fig.update_layout(
    width=900,
    height=500,
    margin=dict(l=40, r=40, t=40, b=40),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_family="Ubuntu, Helvetica, Arial, sans-serif",
    title={
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top', 
                },
    titlefont={
                'size': 20
                },
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""           
            <p style='font-size:16px; margin-bottom:10px; margin-left:10px;margin-right:10px; white-space: normal;'>
            Die Doppelbalken-Grafik zeigt den Eingang von Bewerbungen aus allen Herkunftsländern binnen der jeweiligen Kalenderwoche (orange) im Vergleich zum Eingang pro KW im Vorjahres-Semester (blau).
            </p>
        """, unsafe_allow_html=True)

##################################################################


################################################################

st.divider()

# Top 5 countries section
st.header("Herkunftsländer")

st.divider()

laenderTop10_df = pd.read_csv("Top10BewerberNachLaender.csv", sep=";")
#countries_data["color"] = ['#c9aa4c','#800020', '#B26679',  '#808080','#D3D3D3']
fig_countries = px.pie(laenderTop10_df,  values='WS 2025', names='Herkunftsland', title="Abb. 4: Kuchengrafik Herkunftsländer", labels={'value':'Herkunftsland'} ,
)

#fig_countries = px.bar(countries_data,                     x='Land',                      y='Anteil',      title='Top 5 Herkunftsländer der Bewerber*innen')
fig_countries.update_traces(sort=False,title_position='top center',textinfo='percent+value', selector=dict(type='pie')) 
fig_countries.update_layout(
    width=900,
    height=450,
    margin=dict(l=40, r=40, t=40, b=40),
    title={
                'y': 0.98,
                'x': 0.3,
                'xanchor': 'center',
                'yanchor': 'top', 
                },
    titlefont={
                'size': 20
                },
)

#fig_countries.update_traces(marker_color='#1d1d1b')
st.plotly_chart(fig_countries, use_container_width=True)
# '#808080', '#c9aa4c', '#800020'

st.write("""
Die Kuchengrafik 'Herkunftsländer' weist die Anteile aller Studienbewerber*innen im aktuellen Semesterverfahren nach Nationalität aus.
Dabei werden die TOP 10 Herkunftsländer einzeln, alle weiteren als 'Tortenstück' ausgewiesen.
""")

st.divider()

######################################################################
st.header("Gewinne und Verluste")
colors = []
for x in laenderTop10_df["Diff (%)"].values:
    if x >= 0:
        colors.append("Zuwachs")
    else:
        colors.append("Rückgang")
print(colors)
laenderTop10_df['Änderung zum Vorjahr'] = colors

fig = px.bar(laenderTop10_df,x="Herkunftsland", y = ["Diff (%)"], color = "Änderung zum Vorjahr",
       labels={'x': 'Herkunftsland', 'value':'Dfifferenz (%)', 'variable':'Änderung zum Vorjahr'},
       color_discrete_map={'Rückgang':'red','Zuwachs':'green'},
       barmode="group", title="Abb. 5: Gewinne und Verluste an Bewerber*innen aus den TOP 10 Herkunftsländern",template="gridon", 
                    height=500, range_y=[-50,50])


fig.update_layout(
    width=900,
    height=500,
    margin=dict(l=40, r=40, t=40, b=40),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_family="Ubuntu, Helvetica, Arial, sans-serif",
    title={
                'y': 0.98,
                'x': 0.50,
                'xanchor': 'center',
                'yanchor': 'top', 
                },
    titlefont={
                'size': 19
                },
)

st.plotly_chart(fig, use_container_width=True)

st.write("""
Für die TOP 10 Herkunftsländer zeigt die Balkengrafik 'Gewinne/Verluste'  die prozentualen Zuwächse bzw. die Rückgänge an Studienbewerber*innen im Vergleich zum Vorjahr jeweils zum Stichtag.
""")
#######################################################################

st.divider()
with stylable_container(
        key="container_with_border5",
        css_styles="""
            {
                width = 900px

                border-color: red;
                padding: calc(1em);
                    
            }
            """,
    ):
        # Main st
        # Footer
        st.markdown("""
        © 2025 uni assist e.V.

        Kontakt: [hochschulservice@uni-assist.de](mailto:hochschulservice@uni-assist.de)
        """)
