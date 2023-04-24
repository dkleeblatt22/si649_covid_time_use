import streamlit as st
import altair as alt
import pandas as pd


@st.cache_data
def load_data():
    # bar chart of DIFFERENCE in average minutes spent on each activity between 2019 and 2021

    # reading in data I cleaned in R - AVERAGES HERE ARE WEIGHTED
    waterfall_data = pd.read_csv('data/waterfall.csv')
    # plot was too crowded with this many time points, so only using Jun 2019 - Jun 2021
    month_list = ['Jan 2019', 'Feb 2019', 'Mar 2019', 'Apr 2019', 'May 2019',
                  'Jul 2021', 'Aug 2021', 'Sep 2021', 'Oct 2021', 'Nov 2021', 'Dec 2021']

    waterfall_data = waterfall_data[~waterfall_data['label'].isin(month_list)]
    # making Jun 2020 amount values equal to percent_nonzero
    waterfall_data[waterfall_data['label'] == 'Jun 2019']['amount']
    waterfall_data.loc[waterfall_data['label'] == 'Jun 2019',
                       'amount'] = waterfall_data[waterfall_data['label'] == 'Jun 2019']['percent_nonzero']
    # sorting label variable
    waterfall_data['label'] = pd.Categorical(waterfall_data['label'],
                                             categories=['Jun 2019', 'Jul 2019', 'Aug 2019', 'Sep 2019', 'Oct 2019', 'Nov 2019', 'Dec 2019',
                                                         'Jan 2020', 'Feb 2020', 'Mar 2020', 'May 2020', 'Jun 2020', 'Jul 2020', 'Aug 2020', 'Sep 2020', 'Oct 2020', 'Nov 2020', 'Dec 2020',
                                                         'Jan 2021', 'Feb 2021', 'Mar 2021', 'Apr 2021', 'May 2021', 'Jun 2021'],
                                             ordered=True)
    # data needs to be in order for each category
    waterfall_data = waterfall_data.sort_values(
        ['ACTIVITY', 'label'], ascending=True)
    return waterfall_data


def fall_plotter(water_data):
    # interactive component
    activities2 = list(water_data['ACTIVITY'].unique())

    selectActivity2 = alt.selection_single(
        fields=['ACTIVITY'],
        init={'ACTIVITY': activities2[0]},
        bind=alt.binding_select(options=activities2, name='Select activity: ')
    )

    # code from https://altair-viz.github.io/gallery/waterfall_chart.html

    base_chart = alt.Chart(water_data).transform_window(
        window_sum_amount="sum(amount)",
        window_lead_label="lead(label)",
    ).transform_calculate(
        calc_lead="datum.window_lead_label === null ? datum.label : datum.window_lead_label",
        calc_prev_sum="datum.label === 'End' ? 0 : datum.window_sum_amount - datum.amount",
        calc_amount="datum.label === 'End' ? datum.window_sum_amount : datum.amount",
        calc_text_amount="(datum.label !== 'Begin' && datum.label !== 'End' && datum.calc_amount > 0 ? '+' : '') + datum.calc_amount",
        calc_center="(datum.window_sum_amount + datum.calc_prev_sum) / 2",
        calc_sum_dec="datum.window_sum_amount < datum.calc_prev_sum ? datum.window_sum_amount : ''",
        calc_sum_inc="datum.window_sum_amount > datum.calc_prev_sum ? datum.window_sum_amount : ''",
    ).encode(
        x=alt.X(
            "label:O",
            axis=alt.Axis(title="Months", labelAngle=30),
            sort=None
        ))

    # alt.condition does not support multiple if else conditions which is why
    # we use a dictionary instead. See https://stackoverflow.com/a/66109641
    # for more information
    color_coding = {
        "condition": [
            {"test": "datum.label === 'Begin' || datum.label === 'End'",
                "value": "#878d96"},
            {"test": "datum.calc_amount < 0", "value": "#ff6666"},
        ],
        "value": "#3cb371",
    }

    bar = base_chart.mark_bar(size=35).encode(
        y=alt.Y("calc_prev_sum:Q", title="Percent of People Who Reported Doing Activity",
                axis=alt.Axis(format="%")),
        y2=alt.Y2("window_sum_amount:Q"),
        color=color_coding,
    )

    # The "rule" chart is for the horizontal lines that connect the bars
    rule = base_chart.mark_rule(
        xOffset=-17.5,
        x2Offset=17.5,
    ).encode(
        y=alt.Y("window_sum_amount:Q"),
        x2=alt.X2("calc_lead"),
    )

    # Add values as text
    text_pos_values_top_of_bar = base_chart.mark_text(
        baseline="bottom",
        dy=-4
    ).encode(
        text=alt.Text("calc_sum_inc:N", format='.2%'),
        y=alt.Y("calc_sum_inc:Q"),
    ).transform_filter(
        alt.datum.calc_sum_inc > 0.00
    )
    text_neg_values_bot_of_bar = base_chart.mark_text(
        baseline="top",
        dy=4
    ).encode(
        text=alt.Text("calc_sum_dec:N", format='.2%'),
        y="calc_sum_dec:Q",
    ).transform_filter(
        alt.datum.calc_sum_dec > 0.00
    )
    text_bar_values_mid_of_bar = base_chart.mark_text(baseline="middle").encode(
        text=alt.Text("calc_text_amount:N", format='.2%'),
        y="calc_center:Q",
        color=alt.value("white"),
    )

    # we need a line between Feb 2020 and March 2020
    covid_begins = base_chart.mark_rule(xOffset=-19, strokeWidth=2.5, strokeDash=[1, 1]).encode(
        x=alt.X('label:O', sort=None),
        color=alt.value("darkgrey"),
        opacity=alt.condition(alt.datum.label == 'Mar 2020',
                              alt.value(1), alt.value(0))
    )

    covid_ends = base_chart.mark_rule(xOffset=-19, strokeWidth=2.5, strokeDash=[1, 1]).encode(
        x=alt.X('label:O', sort=None),
        color=alt.value("darkgrey"),
        opacity=alt.condition(alt.datum.label == 'Feb 2021',
                              alt.value(1), alt.value(0))
    )

    waterfall_plot = alt.layer(
        bar,
        rule,
        text_pos_values_top_of_bar,
        text_neg_values_bot_of_bar,
        text_bar_values_mid_of_bar,
        covid_begins,
        covid_ends
    ).add_selection(selectActivity2).transform_filter(selectActivity2).properties(height=300, width=1000)

    return waterfall_plot


waterfall_data = load_data()
waterfall_plot = fall_plotter(waterfall_data)

st.header("Waterfall Visualization")
st.subheader(
    "Averages are influenced by outlier values, so we wanted to take a deeper look.")

st.markdown(
    """
    You just saw the weighted averages of the amount of time spent in each month on each activity. But the thing about averages is that they're highly influenced by extreme values, like values of 0. People that reported a time of 0 minutes on activity did not perform that activity at all that day. We wanted to know how the number of people who reported they did NOT do a certain activity changed throughout time. But to make things easier to understand, we plotted the number of people who DID report they spent any amount of time (> 0 minutes) on an activity over time. 
    """
)

st.altair_chart(waterfall_plot, use_container_width=True, theme='streamlit')

st.markdown(
    """
    - You know the drill - select whatever activity you want to see using the drop-down menu. 
    - If you're seeing a green bar, that means there was an increase in the number of people who did that activity that month, compared with the previous month. If you're seeing a red bar, that means there was a decrease in the number of people who did that activity that month, compared with the previous month. In other words, red bars mean there was an increase in the number of people who didn't do that activity at all, compared with the previous month. You can think about it whatever way makes sense to you - we don't really care.

    """
)
