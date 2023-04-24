import streamlit as st


st.title("Let's talk data")

st.subheader(
    'What kind of data was collected by the ATUS, and how did we clean it?')

st.markdown("ATUS surveys people by randomly selecting each person and then calling them. They want their data to be nationally representative, so they calculated weights for each person using a weighting scheme they’ve developed. They too recognize that 2020 was a weird year, so that year gets its own set of specially calculated weights. So when you see any averages in this story, know that they were weighted according to their ATUS-calculated weights.")
st.markdown("We have data on 9,276 people's days in 2019, 8,647 people's days in 2020, and 8,956 people's days in 2021. We thought you’d want to know about non-holidays, so we removed observations that took place on a holiday.")
st.markdown("""
Here's a run-down of the activities the ATUS captured:
- Caring for Household: This category includes caring for and helping household members, including but not limited to caring for children and caring for other adults in the household.
- Caring for Non-Household: This category includes caring for and helping non-household members(like maybe your elder neighbor).
- Education: This includes any educational activities (attending class, working on homework assignments, etc.)
- Eating and Drinking: This one speaks for itself.
- Civic Duties: This category includes government services and civic obligations. We’ll admit this wasn’t a popular one.
- Household Activities: This category includes housework(like cleaning and laundry), food preparation, interior and exterior maintenance and decoration, and taking care of plants and animals.
- Household Services: This category includes any house-related services not performed yourself. This includes, but is not limited to, cleaning services, home maintenance, pet services, lawn services, and vehicle maintenance and repair.
- Personal Care: This category includes sleeping, grooming, health-related self care, and private activities with other people(that’s all we’ll say about that one).
- Phone Calls: Time spent talking on the phone or waiting for a phone call.
- Care Services: This category is a little broad. This includes any professional and personal care services, so any time spent related to childcare, financial services and banking, medical services, personal care services(like getting a haircut), and a few other niche categories.
- Consumer Purchasing: This category is pretty self explanatory - it includes shopping and purchasing research.
- Religious/Spiritual Activities: This includes any time spent attending religious services or participating in religious or spiritual practices.
- Socializing and Leisure: This category includes any time spent socializing with others(either in your home or outside of it), attending or hosting social events, relaxing(which includes watching TV, tobacco and drug use, listening to music, playing games, arts and crafts, etc.), and attending arts and entertainment events.
- Sports and Exercise: This category includes any time spent doing any sort of physical activity and watching sports events.
- Traveling: Any time spent traveling(regardless of where you’re going).
- Volunteering: Any volunteer work.
- Work: Time spent on any income-earning activity.
"""
            )
