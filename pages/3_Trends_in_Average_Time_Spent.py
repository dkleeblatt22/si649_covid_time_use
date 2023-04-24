import pandas as pd
import streamlit as st
import altair as alt

# @st.cache_data
def load_data():
    monthly_combined = pd.read_csv('data/monthly_combined.csv')

    monthly_combined['DATE'] = pd.to_datetime(
        monthly_combined[['YEAR', 'MONTH']].assign(DAY=1))

    # adding pre covid, covid peak, and post covid variable to monthly_combined
    monthly_combined['time_period'] = 'Post-COVID Peak'
    monthly_combined.loc[monthly_combined['DATE'] <=
                        '2021-01-01', 'time_period'] = 'COVID Peak'
    monthly_combined.loc[monthly_combined['DATE'] <=
                        '2020-02-01', 'time_period'] = 'Pre-COVID Peak'

    monthly_combined['time_period'] = pd.Categorical(monthly_combined.time_period, categories=[
                                                    'Pre-COVID Peak', 'COVID Peak', 'Post-COVID Peak'], ordered=True)

    monthly_combined['month_label'] = (monthly_combined['DATE'].dt.strftime(
        '%b') + ' ' + monthly_combined['DATE'].dt.strftime('%Y'))
    monthly_combined['month_label'] = monthly_combined.month_label.astype(
        'category')

    # ordering month_label column
    my_order = ['Jan 2019', 'Feb 2019', 'Mar 2019', 'Apr 2019', 'May 2019', 'Jun 2019', 'Jul 2019', 'Aug 2019', 'Sep 2019', 'Oct 2019', 'Nov 2019', 'Dec 2019',
                'Jan 2020', 'Feb 2020', 'Mar 2020', 'May 2020', 'Jun 2020', 'Jul 2020', 'Aug 2020', 'Sep 2020', 'Oct 2020', 'Nov 2020', 'Dec 2020',
                'Jan 2021', 'Feb 2021', 'Mar 2021', 'Apr 2021', 'May 2021', 'Jun 2021', 'Jul 2021', 'Aug 2021', 'Sep 2021', 'Oct 2021', 'Nov 2021', 'Dec 2021']

    monthly_combined['month_label'] = pd.Categorical(monthly_combined.month_label, categories=my_order, ordered=True)

    return monthly_combined


def monthly_plotter(monthly_combined):
    activities = list(monthly_combined['ACTIVITY'].unique())

    selectActivity = alt.selection_single(
        fields=['ACTIVITY'],
        init={'ACTIVITY': activities[0]},
        bind=alt.binding_select(options=activities, name='Select activity: ')
    )

    my_order = ['Jan 2019', 'Feb 2019', 'Mar 2019', 'Apr 2019', 'May 2019', 'Jun 2019', 'Jul 2019', 'Aug 2019', 'Sep 2019', 'Oct 2019', 'Nov 2019', 'Dec 2019',
                'Jan 2020', 'Feb 2020', 'Mar 2020', 'May 2020', 'Jun 2020', 'Jul 2020', 'Aug 2020', 'Sep 2020', 'Oct 2020', 'Nov 2020', 'Dec 2020',
                'Jan 2021', 'Feb 2021', 'Mar 2021', 'Apr 2021', 'May 2021', 'Jun 2021', 'Jul 2021', 'Aug 2021', 'Sep 2021', 'Oct 2021', 'Nov 2021', 'Dec 2021']

    year2019 = alt.Chart(monthly_combined[monthly_combined.time_period == 'Pre-COVID Peak']).mark_bar().encode(
        x=alt.X('month_label:N', sort=my_order, axis=alt.Axis(title=None)),
        y=alt.Y('mean:Q', axis=alt.Axis(title="Average Minutes Spent")),
        color=alt.Color('time_period:N', sort=['Pre-COVID Peak', 'COVID Peak', 'Post-COVID Peak'], title=None,
                        scale=alt.Scale(domain=['Pre-COVID Peak', 'COVID Peak', 'Post-COVID Peak'],
                                        range=['#f58a42', '#4b6be5', '#7f3eb0'])),
        tooltip=alt.Tooltip(['mean:Q'], format='.2f',
                            title='Average Number of Minutes')
    ).transform_filter(selectActivity).properties(width=800, height=100)

    year2020 = alt.Chart(monthly_combined[monthly_combined.time_period == 'COVID Peak']).mark_bar().encode(
        x=alt.X('month_label:N', sort=my_order, axis=alt.Axis(title=None)),
        y=alt.Y('mean:Q', axis=alt.Axis(title="Average Minutes Spent")),
        color=alt.Color('time_period:N', sort=['Pre-COVID Peak', 'COVID Peak', 'Post-COVID Peak'], title=None,
                        scale=alt.Scale(domain=['Pre-COVID Peak', 'COVID Peak', 'Post-COVID Peak'],
                                        range=['#f58a42', '#4b6be5', '#7f3eb0'])),
        tooltip=alt.Tooltip(['mean:Q'], format='.2f',
                            title='Average Number of Minutes')
    ).transform_filter(selectActivity).properties(width=800, height=100)

    year2021 = alt.Chart(monthly_combined[monthly_combined.time_period == 'Post-COVID Peak']).mark_bar().encode(
        x=alt.X('month_label:N', sort=my_order, axis=alt.Axis(title=None)),
        y=alt.Y('mean:Q', axis=alt.Axis(title="Average Minutes Spent")),
        color=alt.Color('time_period:N', sort=['Pre-COVID Peak', 'COVID Peak', 'Post-COVID Peak'], title=None,
                        scale=alt.Scale(domain=['Pre-COVID Peak', 'COVID Peak', 'Post-COVID Peak'],
                                        range=['#f58a42', '#4b6be5', '#7f3eb0'])),
        tooltip=alt.Tooltip(['mean:Q'], format='.2f',
                            title='Average Number of Minutes')
    ).transform_filter(selectActivity).properties(width=800, height=100)


    monthly_plot = (year2019+year2020+year2021).add_selection(selectActivity).resolve_scale(x='shared',
                                                                                y='shared').configure_legend(labelFontSize=14)

    # maybe add horizontal lines for mean of each time period?

    return monthly_plot

monthly_data = load_data()

montly_plot = monthly_plotter(monthly_data)

st.header("Monthly Average Time Use Trends")

st.altair_chart(montly_plot, use_container_width=True, theme='streamlit')

st.markdown(
    """
    Select whatever activity you want to see using the drop-down menu. Hover over each bar to see exact average values.
    Our two favorite data points: First, the average American didn't let COVID affect the time they spent on personal care and we're here for it.
    Second, the average time spent on socializing and leisure during COVID peak months was 30 minutes higher than that of pre-COVID peak months. And better yet, this average stayed higher(although only 6 minutes higher) in post-COVID peak months. Did COVID teach us to prioritize hanging out with other people and taking time to relax?
    """
)
