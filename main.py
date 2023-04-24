import streamlit as st
import pandas as pd
import altair as alt


st.title('Impact of the COVID-19 Pandemic on American Time Use')

st.subheader(
    'Jenna Bedrava, Ruiling Kang, Devon Kleeblatt, Kavitha Panicker, Xinyu Wang')
st.subheader('SI 649')

st.markdown("The tradition of complaining about how COVID-19 has impacted our lives is rather cliche in 2023. "
            "Family members, journalists, politicians and even our pets have opinions on how life has been irreversibly altered by a simple virus. "
            "You are likely tired of listening to every schmuck with a repository of invaluable anictdotes collected from the most esteemed local news channels, Facebook groups, neighborhood dog walkers and delicatessen patrons. "
            "Unlike your geriatric in-laws, our data-driven exploration is fueled by the unrelenting power of the U.S. Bureau of Labor Statistics. "
            "Since 2003, the American Time Use Survey (ATUS) has been documenting what the people of our great republic do with their time. "
            "This massive effort has enabled humble graduate students to access 26,879 detailed accounts of daily time use between 2019-2021. "
            "For your viewing pleasure, we have assembled a tour-de-force of interactive visualizations to quantitively analyze exactly how daily life has been altered by COVID-19. "
            "Thanks to our efforts, the next time you are cornered into a conversation with a poorly-informed citizen, simply refer them to our omniscient guide.")
