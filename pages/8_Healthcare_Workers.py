import streamlit as st
import altair as alt
import pandas as pd


@st.cache_data
def load_data():
    occ = pd.read_csv('data/avg_time_all_years_bymonth_occ.csv')
    occ['MONTH_YEAR'] = pd.Categorical(occ['MONTH_YEAR'],
                                       categories=['Jan 2019', 'Feb 2019', 'Mar 2019', 'Apr 2019', 'May 2019', 'Jun 2019', 'Jul 2019', 'Aug 2019', 'Sep 2019', 'Oct 2019', 'Nov 2019', 'Dec 2019',
                                                   'Jan 2020', 'Feb 2020', 'Mar 2020', 'May 2020', 'Jun 2020', 'Jul 2020', 'Aug 2020', 'Sep 2020', 'Oct 2020', 'Nov 2020', 'Dec 2020',
                                                   'Jan 2021', 'Feb 2021', 'Mar 2021', 'Apr 2021', 'May 2021', 'Jun 2021', 'Jul 2021', 'Aug 2021', 'Sep 2021', 'Oct 2021', 'Nov 2021', 'Dec 2021'],
                                       ordered=True)
    # removing Civic Duties
    occ = occ[occ.ACTIVITY != 'Civic Duties']

    return occ


def healthcare_plotter(occ):
    activities3 = list(occ['ACTIVITY'].unique())
    selectActivity3 = alt.selection_single(
        fields=['ACTIVITY'],
        init={'ACTIVITY': activities3[0]},
        bind=alt.binding_select(options=activities3, name='Select activity: ')
    )

    linechart = alt.Chart(occ).mark_line(point=True).encode(
        x=alt.X('MONTH_YEAR:O', sort=['Jan 2019', 'Feb 2019', 'Mar 2019', 'Apr 2019', 'May 2019', 'Jun 2019', 'Jul 2019', 'Aug 2019', 'Sep 2019', 'Oct 2019', 'Nov 2019', 'Dec 2019',
                                      'Jan 2020', 'Feb 2020', 'Mar 2020', 'May 2020', 'Jun 2020', 'Jul 2020', 'Aug 2020', 'Sep 2020', 'Oct 2020', 'Nov 2020', 'Dec 2020',
                                      'Jan 2021', 'Feb 2021', 'Mar 2021', 'Apr 2021', 'May 2021', 'Jun 2021', 'Jul 2021', 'Aug 2021', 'Sep 2021', 'Oct 2021', 'Nov 2021', 'Dec 2021'],
                title=None),
        y=alt.Y('mean:Q', title='Average Number of Minutes Spent'),
        color=alt.Color('OCC_GROUP:N', title='Occupation Group', scale=alt.Scale(domain=[
                        'Healthcare Worker', 'Non-Healthcare Worker'], range=['#ed68ce', '#e8bc56'])),
        tooltip=alt.Tooltip(['mean:Q'], format='.2f',
                            title='Average Number of Minutes')
    ).add_selection(selectActivity3).transform_filter(selectActivity3)

    # we need a line between Feb 2020 and March 2020
    covid_begins2 = alt.Chart(occ).mark_rule(xOffset=0, strokeWidth=2.5, strokeDash=[1, 1]).encode(
        x=alt.X('MONTH_YEAR:O', sort=['Jan 2019', 'Feb 2019', 'Mar 2019', 'Apr 2019', 'May 2019', 'Jun 2019', 'Jul 2019', 'Aug 2019', 'Sep 2019', 'Oct 2019', 'Nov 2019', 'Dec 2019',
                                      'Jan 2020', 'Feb 2020', 'Mar 2020', 'May 2020', 'Jun 2020', 'Jul 2020', 'Aug 2020', 'Sep 2020', 'Oct 2020', 'Nov 2020', 'Dec 2020',
                                      'Jan 2021', 'Feb 2021', 'Mar 2021', 'Apr 2021', 'May 2021', 'Jun 2021', 'Jul 2021', 'Aug 2021', 'Sep 2021', 'Oct 2021', 'Nov 2021', 'Dec 2021']),
        color=alt.value("darkgrey"),
        opacity=alt.condition(alt.datum.MONTH_YEAR ==
                              'Mar 2020', alt.value(1), alt.value(0))
    )

    covid_ends2 = alt.Chart(occ).mark_rule(xOffset=0, strokeWidth=2.5, strokeDash=[1, 1]).encode(
        x=alt.X('MONTH_YEAR:O', sort=['Jan 2019', 'Feb 2019', 'Mar 2019', 'Apr 2019', 'May 2019', 'Jun 2019', 'Jul 2019', 'Aug 2019', 'Sep 2019', 'Oct 2019', 'Nov 2019', 'Dec 2019',
                                      'Jan 2020', 'Feb 2020', 'Mar 2020', 'May 2020', 'Jun 2020', 'Jul 2020', 'Aug 2020', 'Sep 2020', 'Oct 2020', 'Nov 2020', 'Dec 2020',
                                      'Jan 2021', 'Feb 2021', 'Mar 2021', 'Apr 2021', 'May 2021', 'Jun 2021', 'Jul 2021', 'Aug 2021', 'Sep 2021', 'Oct 2021', 'Nov 2021', 'Dec 2021']),
        color=alt.value("darkgrey"),
        opacity=alt.condition(alt.datum.MONTH_YEAR ==
                              'Feb 2021', alt.value(1), alt.value(0))
    )

    health_plot = alt.layer(linechart, covid_begins2, covid_ends2).properties(
        title='Comparing Trends in Time Use Among Healthcare Workers and Non-Healthcare Workers')

    return health_plot


occ = load_data()
plots = healthcare_plotter(occ)

st.header("Healthcare Worker Time Use")

st.altair_chart(plots, use_container_width=True, theme=None)

st.markdown("This interactive chart allows for comparison between healthcare worker and non-healthcare worker time use from 2019-2021. ")