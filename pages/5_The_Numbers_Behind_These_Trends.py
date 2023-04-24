import streamlit as st
import altair as alt
import pandas as pd

@st.cache_data
def load_data():
    models = pd.read_csv('data/models.csv')
    return models


def plotter(models):

    # interactive component
    activities2 = list(models['ACTIVITY'].unique())

    selectActivity2 = alt.selection_single(
        fields=['ACTIVITY'],
        init={'ACTIVITY': activities2[0]},
        bind=alt.binding_select(options=activities2, name='Select activity: ')
    )

    colorCondition = alt.condition(
        alt.datum.ESTIMATE > 0, alt.value("#3cb371"), alt.value("#ff6666"))

    # point estimates
    points = alt.Chart(models, title='Generalized Linear Model Results for Selected Activity').mark_point(filled=True, color='black').transform_window(
        sort=[alt.SortField("ESTIMATE", order="descending")],
        est_rank="rank(*)"
    ).encode(
        alt.X('ESTIMATE:Q'),
        alt.Y('VARIABLE:N', sort=alt.EncodingSortField(field="est_rank",
            order="ascending"), axis=alt.Axis(title='Predictor Variable')),
        color=colorCondition,
        tooltip=alt.Tooltip(value=None)
    )

    # error bars
    error_bars = alt.Chart(models).mark_errorbar().transform_window(
        sort=[alt.SortField("ESTIMATE", order="descending")],
        est_rank="rank(*)"
    ).encode(
        alt.X('upperCI:Q', scale=alt.Scale(zero=False), axis=alt.Axis(
            title='Parameter Estimates and 95% Confidence Intervals')),
        alt.X2('lowerCI:Q'),
        alt.Y('VARIABLE:N', sort=alt.EncodingSortField(
            field="est_rank", order="ascending")),
        color=colorCondition,
        tooltip=alt.Tooltip(value=None)
    )

    forest_plot = (
        points + error_bars).add_selection(selectActivity2).transform_filter(selectActivity2)
    
    opacityCondition = alt.condition(
        alt.datum.SIGNIFICANT == 1, alt.value(.8), alt.value(0))

    bubble_chart = alt.Chart(models, title='Significant Effect Estimates from Generalized Linear Models').mark_circle(
        opacity=0.8, stroke='black', strokeWidth=.7
    ).encode(y=alt.Y('VARIABLE:N', sort=alt.EncodingSortField(field='VARIABLE:N', order='ascending')),
            x=alt.X('ACTIVITY:N'),
            size=alt.Size('EXP_EST:Q', legend=None,
                        scale=alt.Scale(range=[0, 1500])),
            color=colorCondition,
            tooltip=alt.Tooltip(['INTERP:N'], title='Interpretation'),
            opacity=opacityCondition
            ).transform_filter(alt.datum.VARIABLE != 'Intercept').transform_filter(alt.datum.ACTIVITY != 'Civic Duties')

    return bubble_chart | forest_plot

models = load_data()
plots = plotter(models)

st.header("Generalized Linear Model")
st.subheader("Enough with the hearsay. Let’s put some numbers behind these trends.")

st.altair_chart(plots, use_container_width=True, theme=None)

st.markdown(
    """
    Each model for each activity gives us numbers (we call these parameter estimates sometimes) for each predictor variable, which tell us how much the time spent on that activity, on average, changed within that variable. Let’s start with the plot on the left. Each column is one model that we ran. Each row is all the variables we used to model the time spent doing the activity listed at the bottom of each column. The size of each circle represents the size of the parameter estimate. Using the red and green colors you’ve seen before, green represents a positive estimate (this variable increased the time spent) and red represents a negative estimate (this variable decreased the time spent).

    """
)

tab1, tab2 = st.tabs(["Technical explanation", "Non-technical explanation"])

with tab1:
    st.header("How does our model work?")
    st.markdown(
        """
        - So what exactly are these models telling us? How we interpret each variable within each model depends on if that variable is a continuous numerical variable or if it's categories. For age (age is the only continuous variable we used), the parameter estimate represents the percent change in the average number of minutes spent on that activity for each year increase in age. For all the other variables, i.e. the categorical variables, there's a reference group that we defined. The parameter estimate represents the percent change in the average number of minutes spent on that activity from the reference group. For instance, we made “never married” the reference group for the marital status variable. This means that the parameter estimate for the “married” category is the percent change in the number of minutes married people spent compared to the number of minutes people who have never been married spent. We know this is a little confusing, so we put interpretations of each parameter estimate on each bubble. Just hover over the bubble to see it.
        - We’re only showing you the parameter estimates that were found to be significantly different than 0, so the blank spaces in the plot just mean that variable was not found to have a significant impact on the time spent in that activity. 
        - The plot on the left is an overview of every model. The plot on the right goes into more detail about one of the models. Choose which activity you want to display using the drop-down menu. When you choose an activity, the variable with the largest increase in time spent will move to the top and likewise, the variable with largest decrease in time spent will move to the bottom. Choose different activities to see how different variables impacted time spent on that activity. Those lines represent the range of values we are 99.4% confident the true value lies within. The confidence intervals are pretty small for a lot of variables because we have so much data (every statistician’s dream). 
        - If you’re familiar with confidence intervals, you might be wondering what the 99.4% confidence interval thing is about. We used a Bonferroni correction on each model and divided our 0.05 significance level by the number of predictors within each model. This means our confidence intervals got wider, decreasing the chance we find associations that aren't really significant to be significant. 

        """
    )

with tab2:
    st.subheader("Observed trends")
    st.markdown(
        """
        Let’s cut out the statistics mumbo jumbo. These are some trends we see:
        - For every activity except household services, we see significant differences in the average amount of time spent during pre-COVID months and COVID peak months. Moreover, for every activity, we see significant differences in the average amount of time spent during pre-COVID months and post-COVID peak months. We’re saying COVID changes the average amount of time we spent on activities. We knew it.
        - In addition to being in a post-COVID peak month, variables that were significant for all activities were:
        - Age: The relationship between time spent and age is significant for all activities, holding all other variables constant. In other words, how we spend our time changes with age.
        - Sex: For all activities, average time spent by females is significantly different than average time spent by males, holding all other variables constant.
        - Having less than a high school diploma: People who have less than a high school diploma spent significantly different amounts of time, on average, in all activities than people who have a high school diploma, holding all other variables constant.
        - Having a Bachelor’s degree or having a graduate degree: People who have a Bachelor's degree or a graduate degree spent significantly different amounts of time, on average, in all activities than people who have a high school diploma, holding all other variables constant.
        - Being a weekend day: This one we expected. People spend different amount of time, on average, on all activities during the weekend than they do during the weekday, holding all other variables constant. 
        - These are interesting things we found when looking at the 3 variables with the most impact on each activity.
        - The three variables that had the most impact on the time spent on caring for the household were being married, being previously married, and being female. We also noted that 2 of these are also in the top most impactful variables for time spent on household activities, namely being female and being married. These variables significantly increased the time spent on caring for the household and time spent on household activities. This made us wonder how COVID impacted these associations. We added interaction terms for time period x sex and for time period x marital status to the caring for household and household activities models. We’ll spare you the statistical details, but the interaction terms were significant except for one. This means the impact of sex and the impact of marital status on time spent on these activities were significantly different between time periods. 
        - Time period shows up in the top 3 most impactful variables for consumer purchasing and traveling.

        """
    )


