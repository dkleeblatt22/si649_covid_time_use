import pandas as pd
import streamlit as st
import altair as alt


@st.cache_data
def load_data():

    # bar chart of DIFFERENCE in average minutes spent on each activity between 2019 and 2021

    # reading in data I cleaned in R - AVERAGES HERE ARE WEIGHTED
    barchart_data = pd.read_csv(
        'data/avg_time_2019_2021.csv')

    # decided we want differences to be 2021-2019, so positive values reflect an increase in that activity in 2021
    barchart_data['DIFF'] = barchart_data['DIFF'] * -1

    return barchart_data

def bar_plotter(barchart_data):
    ages = list(barchart_data['AGE_GROUP'].unique())

    sexes = list(barchart_data['SEX'].unique())

    # interactive components
    selectSex = alt.selection_single(
        fields=['SEX'],
        init={'SEX': sexes[0]},
        bind=alt.binding_select(options=sexes, name='Select sex: ')
    )

    selectAge = alt.selection_single(
        fields=['AGE_GROUP'],
        init={'AGE_GROUP': ages[0]},
        bind=alt.binding_select(options=ages, name='Select age group: ')
    )

    # bar chart
    barchart = alt.Chart(barchart_data, title="Comparing Average Time Spent in 2021 and 2019").transform_filter(selectAge & selectSex).transform_window(
        sort=[alt.SortField("DIFF", order="descending")],
        diff_rank="rank(*)"
    ).mark_bar().encode(
        alt.Y('ACTIVITY:N', sort=alt.EncodingSortField(
            field="diff_rank", order="ascending"), axis=alt.Axis(title=None)),
        alt.X('DIFF:Q', axis=alt.Axis(title="Average Difference Between 2021 and 2019 in Minutes"),
            scale=alt.Scale(domain=[(barchart_data.DIFF.min() - 4), (barchart_data.DIFF.max() + 4)])),
        color=alt.condition(
            alt.datum.DIFF > 0,
            alt.value("#3cb371"),  # positive color
            alt.value("#ff6666")  # negative color
        )
    )

    # text labels
    text_right = barchart.mark_text(align="left", baseline="middle", dx=3).encode(
        text=alt.Text("DIFF:Q", format='.2f'),
        opacity=alt.condition(alt.datum.DIFF > 0, alt.value(1), alt.value(0)),
        color=alt.condition(alt.datum.significant == 'YES',
                            alt.value("#3cb371"), alt.value('lightgray'))
    )

    text_left = barchart.mark_text(align="right", baseline="middle", dx=-3).encode(
        text=alt.Text("DIFF:Q", format='.2f'),
        opacity=alt.condition((alt.datum.DIFF < 0), alt.value(1), alt.value(0)),
        color=alt.condition(alt.datum.significant == 'YES',
                            alt.value("#ff6666"), alt.value('lightgray'))
    )

    final_barchart = barchart.add_selection(selectAge, selectSex) + text_right + text_left
    return final_barchart


data = load_data()
plot = bar_plotter(data)

st.header("Comparing Pre-COVID & Post-COVID time uses")

st.altair_chart(plot, use_container_width=True, theme='streamlit')

st.markdown("Here, you can view the % change in minutes spend on a variety of activities for different demographic groups. Changes which are not statistitcally significant, ie those which fail a P-test, are shown with gray text.")



