import streamlit as st
import altair as alt
import pandas as pd

@st.cache_data
def load_data():
    models = pd.read_csv('data/models.csv')
    return models


def plotter(models):

    top = alt.Chart(models).transform_calculate(
        PERCENT_CHANGE_SIGN=alt.datum.PERCENT_CHANGE * alt.datum.SIGN_PERCENT_CHANGE
    ).transform_filter(
        alt.FieldOneOfPredicate(
            'VARIABLE', oneOf=['COVID Peak', 'Post-COVID Peak'])
    ).transform_filter(
        alt.FieldOneOfPredicate('ACTIVITY', oneOf=['Caring for Household', 'Caring for Non-Household', 'Education', 'Eating and Drinking',
                                                   'Household Activities', 'Household Services', 'Personal Care', 'Phone Calls'])
    ).mark_bar().encode(
        x=alt.X('VARIABLE:N', axis=alt.Axis(title=None, labelAngle=30)),
        y=alt.Y('PERCENT_CHANGE_SIGN:Q', axis=alt.Axis(
            title='Percent Change from Pre-COVID Peak Months')),
        color=alt.Color('VARIABLE:N', scale=alt.Scale(domain=[
                        'COVID Peak', 'Post-COVID Peak'], range=['#4b6be5', '#7f3eb0']), legend=None),
        column=alt.Column('ACTIVITY:N', title=None)
    ).properties(width=100)


    bottom = alt.Chart(models).transform_calculate(
        PERCENT_CHANGE_SIGN=alt.datum.PERCENT_CHANGE * alt.datum.SIGN_PERCENT_CHANGE
    ).transform_filter(
        alt.FieldOneOfPredicate(
            'VARIABLE', oneOf=['COVID Peak', 'Post-COVID Peak'])
    ).transform_filter(
        alt.FieldOneOfPredicate('ACTIVITY', oneOf=['Care Services', 'Consumer Purchasing', 'Religious/Spiritual Activities',
                                                'Socializing and Leisure', 'Sports and Exercise', 'Traveling',
                                                'Volunteering', 'Work'])
    ).mark_bar().encode(
        x=alt.X('VARIABLE:N', axis=alt.Axis(title=None, labelAngle=30)),
        y=alt.Y('PERCENT_CHANGE_SIGN:Q', axis=alt.Axis(
            title='Percent Change from Pre-COVID Peak Months')),
        color=alt.Color('VARIABLE:N', scale=alt.Scale(domain=[
                        'COVID Peak', 'Post-COVID Peak'], range=['#4b6be5', '#7f3eb0']), legend=None),
        column=alt.Column('ACTIVITY:N', title=None)
    ).properties(width=100)

    return top & bottom

models = load_data()
plots = plotter(models)

st.header("Comparing Pre-COVID time use with COVID and post-COVID time use")
st.markdown("We wanted to see how the effect sizes of each time period variable looked within each activity model. Remember the effect size of the COVID peak variable represents the average multiplicative effect on time spent between pre-COVID months and COVID peak months ( and likewise for the post-COVID peak variable). We converted these values into percent change values and plotted them below.")

st.altair_chart(plots, use_container_width=True, theme=None)

st.markdown(
    """
    Positive percent changes mean we saw an increase in that activity compared to pre-COVID months and negative percent changes mean we saw a decrease in that activity compare to post-COVID months, holding all other variables in the model constant.
    So what is this plot telling us?
    - For activities where the blue bar is higher than the purple bar, this means that the COVID peak months were more different than the post-COVID peak months. In other words, after the COVID pandemic started to become more controlled, time spent on these activities started shifting more toward where they were before COVID hit.
    - We see bidirectional bars for caring for household, caring for non-household, household services, and work. This means we saw an increase/decrease during COVID peak months compared to pre-COVID months, but then the opposite trend during post-COVID peak months.
    - The only activity where the percent changes are in the same direction and we see a bigger percent change in post-COVID peak months than in COVID peak months is eating and drinking. However, it’s important to note that the average time spent eating and drinking each month for these 3 years didn’t change all that much, as we saw in the bar plot of monthly averages earlier. So we’re not putting a lot of stock in this finding, although we recognize that it is an interesting trend.

    """
)
