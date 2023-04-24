import pandas as pd
import streamlit as st
import altair as alt


@st.cache_data
def load_data():
    # decided we want differences to be 2021-2019, so positive values reflect an increase in that activity in 2021
    tsne = pd.read_csv('data/tsne.csv')
    tsne['time_period'] = pd.Categorical(tsne.time_period, categories=[
                                         'Pre-COVID Peak', 'COVID Peak', 'Post-COVID Peak'], ordered=True)

    return tsne


def tsne_plotter(tsne):
    # based on avg_time_2019_2021_bymonth.csv, the activities with significantly different means in 2019 and 2021 are:
    # Eating and Drinking, Civic Duties, Household Activities, Personal Care, Phone Calls, Consumer Purchasing, Religious/Spiritual Activities,
    # Socializing and Leisure, Traveling, Volunteering

    base = alt.Chart(tsne).encode(
        x=alt.X('tsne1:Q', sort={'field': 'date'}, axis=alt.Axis(title='tSNE Dimension 1'),
                scale=alt.Scale(domain=[(tsne.tsne1.min() - 4), (tsne.tsne1.max() + 6)])),
        y=alt.Y('tsne2:Q', sort={'field': 'date'}, axis=alt.Axis(title='tSNE Dimension 2'),
                scale=alt.Scale(domain=[(tsne.tsne2.min() - 2), (tsne.tsne2.max() + 2)])),
        color=alt.Color('time_period:N', legend=alt.Legend(title=None), sort=['Pre-COVID Peak', 'COVID Peak', 'Post-COVID Peak'],
                        scale=alt.Scale(domain=['Pre-COVID Peak', 'COVID Peak', 'Post-COVID Peak'],
                                        range=['#fa8775', '#4b6be5', '#67009b'])),
        # tooltip = alt.Tooltip(['Caring for Household','Household Activities', 'Phone Calls', 'Socializing and Leisure', 'Traveling'], format='.2f')
    )

    points = base.mark_circle()
    line = base.mark_line().encode(opacity=alt.value(.3))
    text = base.mark_text(dy=-10).encode(
        text='date_label'
    )

    # I want a barchart of the 10 significantly different activities to pop up when each point on this scatterplot is clicked

    # allowing for user to select one month
    selectMonth = alt.selection_single(on='mouseover', nearest=True)

    month_barchart = base.transform_fold(['Eating and Drinking', 'Civic Duties', 'Household Activities', 'Personal Care',
                                          'Phone Calls', 'Consumer Purchasing', 'Religious/Spiritual Activities',
                                          'Socializing and Leisure', 'Traveling', 'Volunteering'], as_=['ACTIVITY', 'value']
                                         ).mark_bar().transform_filter(
        alt.FieldOneOfPredicate("ACTIVITY", oneOf=['Eating and Drinking', 'Civic Duties', 'Household Activities', 'Personal Care',
                                                   'Phone Calls', 'Consumer Purchasing', 'Religious/Spiritual Activities',
                                                   'Socializing and Leisure', 'Traveling', 'Volunteering'])
    ).transform_window(sort=[alt.SortField("value", order="descending")], val_rank="rank(*)"
                       ).encode(
        x=alt.X('value:Q', axis=alt.Axis(
            title='Weighted Average Minutes Spent')),
        y=alt.Y('ACTIVITY:N', sort=alt.EncodingSortField(
            field="val_rank", order="ascending"), axis=alt.Axis(title=None))
    ).transform_filter(selectMonth)

    tsneplot = (points + line + text).add_selection(selectMonth).properties(
        title='Trends in Time Usage by Month via tSNE Dimension Reduction') | month_barchart.properties(title='Average Minutes Spent on Each Activity')

    return tsneplot


tsne_data = load_data()
tsneplot = tsne_plotter(tsne_data)

st.header("Visualizing monthly time use trends with dimensionality reduction")

st.altair_chart(tsneplot, use_container_width=True, theme='streamlit')

st.subheader(
    " We used tSNE to plot each month in 2019, 2020, and 2021 in a 2-dimensional space. ")
st.markdown(
    """
- T-distributed stochastic neighbor embedding (tSNE) is a fancy way to say we don't think you (or we) could read a 17-dimensional plot. Instead, we took all 17 activities the ATUS records and reduced them to 2-dimensions, which you see here. Months that have similar distributions of activity times are closer together. We connected months by their order in time. 
- Take note of the colors here - you’ll see them again. We grouped our data into three sections: pre-COVID peak (January 2019 to February 2020), COVID peak (March 2020 to January 2021), and post-COVID peak (February 2021 to December 2021).
- If you read nothing else on this page: Notice the orange points (months before the COVID peak hit us like a bus) have no overlap with the blue points (the peak COVID months). This means the time we spent on the 17 activity categories weren’t very similar before COVID and during the COVID peak. We see the purple months (the months after we got COVID hospitalizations under control) overlap with both the orange and blue points. So, post-COVID months are somewhere in between pre-COVID months and peak COVID months in terms of similarity of time spent in the 17 activity categories.
- Hover over points in the plot on the left to see the average number of minutes spent in the 10 categories we found to have significantly different averages in 2019 and 2020 (using a two-sample t-test with non-equal variances at the 𝛂 = 0.05 significance level). The bars will move with each activity. The activity with the highest amount of time spent will always shift to the top. 
    
"""
)
