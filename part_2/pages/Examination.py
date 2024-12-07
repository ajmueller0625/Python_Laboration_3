import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Tab configuration
st.set_page_config(
    page_title='Student Examination Comparison',
    page_icon=':bar_chart:',
    layout='wide'
)


@st.cache_data  # Caches the dataframe
def load_data():
    df = pd.read_csv('part_2/StudentPerformanceFactors.csv')
    return df


# Puts the dataframe in a variable
df = load_data()

# Title of the page and a header for the page filter
st.title('Students examination scores comparison based on given factors')
st.sidebar.header('Filters')

# Dataframe that is going to be used for filters
filtered_data = df

# Creates a radio button filter for school type
school_types = ['All'] + list(df['School_Type'].unique())
school_types_radio = st.sidebar.radio(
    'Select a school type', school_types, horizontal=True)

# Applies the selected filter from school type as long the value is not all
if school_types_radio != 'All':
    filtered_data = filtered_data[(
        filtered_data['School_Type'] == school_types_radio)]

# Creates a dropdown filter for attendance
attendance = ['60 - 70', '71 - 80', '81 - 90', '91 - 100']
attendance_dropdown = st.sidebar.selectbox(
    'Attendance Percentage', attendance)

# Applies the selected filter from attendance
attendance_dropdown_input = attendance_dropdown.split(' - ')
filtered_data = filtered_data[(filtered_data['Attendance'] >= int(attendance_dropdown_input[0])) & (
    filtered_data['Attendance'] <= int(attendance_dropdown_input[1]))]

# Creates a dropdown filter for amount of hours stutied
hours_studied = ['1 - 10', '11 - 20', '21 - 30', '31 - 40', '41 - 44']
hours_studied_dropdown = st.sidebar.selectbox(
    'Amount of hours stutied', hours_studied)

# Applies the selected filter from amount of hours stutied
hours_studied_dropdown_input = hours_studied_dropdown.split(' - ')
filtered_data = filtered_data[(filtered_data['Hours_Studied'] >= int(hours_studied_dropdown_input[0])) & (
    filtered_data['Hours_Studied'] <= int(hours_studied_dropdown_input[1]))]

# Creates a dropdown filter for amount of sleep hours
sleep_hours = ['3 - 4', '5 - 6', '7 - 8', '9 - 10']
sleep_hours_dropdown = st.sidebar.selectbox(
    'Amount of sleep hours', sleep_hours)

# Applies the selected filter from amount of sleep hours
sleep_hours_dropdown_input = sleep_hours_dropdown.split(' - ')
filtered_data = filtered_data[(filtered_data['Sleep_Hours'] >= int(sleep_hours_dropdown_input[0])) & (
    filtered_data['Sleep_Hours'] <= int(sleep_hours_dropdown_input[1]))]

# Creates a radio button filter for motivation level
motivation_level = ['All'] + list(df['Motivation_Level'].unique())
motivation_level_radio = st.sidebar.radio(
    'Motivation level', motivation_level)

# Applies the selected filter from motivation level as long it is not all
if motivation_level_radio != 'All':
    filtered_data = filtered_data[(
        filtered_data['Motivation_Level'] == motivation_level_radio)]

# Creates a radio button filter for extracurricular activities
extracurricular_activities = ['All'] + \
    list(df['Extracurricular_Activities'].unique())
extracurricular_activities_radio = st.sidebar.radio(
    'Extracurricular activities', extracurricular_activities)

# Applies the selected filter from tracurricular activities as long it is not all
if extracurricular_activities_radio != 'All':
    filtered_data = filtered_data[(
        filtered_data['Extracurricular_Activities'] == extracurricular_activities_radio)]

# Header and columns configuration for filters used
st.header('Students examinations scores', divider=True)
factor_col1, factor_col2, factor_col3, factor_col4, factor_col5, factor_col6 = st.columns(
    6)

# Columns 1 - 6 show all the filters that has been used
with factor_col1:
    st.metric('School Type', school_types_radio)

with factor_col2:
    st.metric('Atendance Percentage', attendance_dropdown)

with factor_col3:
    st.metric('Hours Studied Per Week', hours_studied_dropdown)

with factor_col4:
    st.metric('Sleep Hours Per Night', sleep_hours_dropdown)

with factor_col5:
    st.metric('Motivation Level', motivation_level_radio)

with factor_col6:
    st.metric('Extracurricular Activities', extracurricular_activities_radio)

# Rename the filtered dataframe columns for better readability
filtered_data.rename({'Previous_Scores': 'Previous Scores',
                     'Exam_Score': 'Current Scores'}, axis=1, inplace=True)

# Takes the data from dataframe that is going to be used
scores_filtered_data = filtered_data[[
    'Previous Scores', 'Current Scores']]
scores_filtered_data.index.rename(name='Index', inplace=True)

# Shows the filtered dataframe in the page
st.dataframe(
    scores_filtered_data,
    use_container_width=True
)

# Header and columns cofiguration students examination scores comparison
st.header('Students Examination Scores Comparison', divider=True)
exams_description1, exams_description2 = st.columns(2)

# Takes the previous exam score from filtered dataframe and use aggregate method to get the count, mean, min, and max
with exams_description1:
    previous_score = filtered_data['Previous Scores'].agg(
        ['count', 'mean', 'min', 'max']).to_frame().transpose()
    previous_score.rename({'count': 'Amount of Student', 'mean': 'Mean Value',
                          'min': 'Min Value', 'max': 'Max Value'}, axis=1, inplace=True)
    previous_score.index.rename(name='Score', inplace=True)
    st.dataframe(previous_score, use_container_width=True)

# Takes the current exam score from filtered dataframe and use aggregate method to get the count, mean, min, and max
with exams_description2:
    current_score = filtered_data['Current Scores'].agg(
        ['count', 'mean', 'min', 'max']).to_frame().transpose()
    current_score.rename({'count': 'Amount of Student', 'mean': 'Mean Value',
                          'min': 'Min Value', 'max': 'Max Value'}, axis=1, inplace=True)
    current_score.index.rename(name='Score', inplace=True)
    st.dataframe(current_score, use_container_width=True)

# Header for students examination scores chart comparison
st.header('Students Examination Scores Chart Comparison', divider=True)

# Creates a bar chart for comparing previous and current exam scores of the students
if not filtered_data['Current Scores'].empty:
    exams_score_bar = go.Figure()

    # Creates a bar chart for previous exam scores
    previous_score_data = filtered_data['Previous Scores'].to_frame()
    previous_score_data.index.rename(name='Students Index', inplace=True)
    exams_score_bar.add_trace(go.Bar(
        x=previous_score_data.index,
        y=previous_score_data['Previous Scores'],
        name='Previous Scores',
        marker_color='crimson',
        text=previous_score_data['Previous Scores'],
        textposition='outside'
    ))

    # Creates a bar chart for current exam scores
    current_score_data = filtered_data['Current Scores'].to_frame()
    current_score_data.index.rename(name='Students Index', inplace=True)
    exams_score_bar.add_trace(go.Bar(
        x=current_score_data.index,
        y=current_score_data['Current Scores'],
        name='Current Scores',
        marker_color='cornflowerblue',
        text=current_score_data['Current Scores'],
        textposition='outside'
    ))

    # Combines the two exam scores bar chart
    exams_score_bar.update_layout(barmode='group', title='Students Overall Scores',
                                  xaxis_title='Student Index', yaxis_title='Examination Score')
    exams_score_bar.update_xaxes(type='category')

    st.plotly_chart(exams_score_bar, use_container_width=True)

else:

    # Shows if there is no data found based on all the filters
    st.write('No examination scores data found')
