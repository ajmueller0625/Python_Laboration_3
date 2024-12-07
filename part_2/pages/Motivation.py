import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Tab configuration
st.set_page_config(
    page_title='Student Motivation Level',
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
st.title('Students motivation level based on specific factors')
st.sidebar.header('Filters')

# Dataframe that is going to be used for filters
filtered_data = df

# Creates a radio button filter for school type
students_school_types = ['All'] + list(df['School_Type'].unique())
students_school_types_radio = st.sidebar.radio(
    'Select a school type', students_school_types, horizontal=True)

# Applies the selected filter from school type as long the value is not all
if students_school_types_radio != 'All':
    filtered_data = filtered_data[(
        filtered_data['School_Type'] == students_school_types_radio)]

# Creates a dropdown filter for teacher quality
teacher_quality = ['All', 'Low', 'Medium', 'High']
teacher_quality_dropdown = st.sidebar.selectbox(
    'Teacher Quality', teacher_quality)

# Applies the selected filter from teacher quality as long the value is not all
if teacher_quality_dropdown != 'All':
    filtered_data = filtered_data[(
        filtered_data['Teacher_Quality'] == teacher_quality_dropdown)]

# Creates a radio button filter for resource access
resourses_access = ['All', 'Low', 'Medium', 'High']
resourses_access_radio = st.sidebar.radio(
    'Select resource accessability', resourses_access)

# Applies the selected filter from resource access as long the value is not all
if resourses_access_radio != 'All':
    filtered_data = filtered_data[(
        filtered_data['Access_to_Resources'] == resourses_access_radio)]

# Creates a dropdown filter for family income
family_income = ['All'] + list(df['Family_Income'].unique())
family_income_dropdown = st.sidebar.selectbox(
    'Family Income', family_income)

# Applies the selected filter from family income as long the value is not all
if family_income_dropdown != 'All':
    filtered_data = filtered_data[(
        filtered_data['Family_Income'] == family_income_dropdown)]

# Creates a dropdown filter for physical activy
physical_activies = ['All', '0 - 2', '3 - 4', '5 - 6']
physical_activies_dropdown = st.sidebar.selectbox(
    'Physical Activity (hours/week)', physical_activies)

# Applies the selected filter from physical activy as long the value is not all
if physical_activies_dropdown != 'All':
    physical_activies_input = physical_activies_dropdown.split(' - ')
    filtered_data = filtered_data[(filtered_data['Physical_Activity'] >= int(physical_activies_input[0])) & (
        filtered_data['Physical_Activity'] <= int(physical_activies_input[1]))]

# Creates a radio button filter for peer influence
peer_influence = ['All'] + list(df['Peer_Influence'].unique())
peer_influence_radio = st.sidebar.radio(
    'Peer Influence', peer_influence)

# Applies the selected filter from peer influence as long the value is not all
if peer_influence_radio != 'All':
    filtered_data = filtered_data[(
        filtered_data['Peer_Influence'] == peer_influence_radio)]

# Header and columns configuration for used filters and minority/majority of students motivation level
st.header('Students Motivation Level', divider=True)
motivation_col1, motivation_col2, motivation_col3, motivation_col4, motivation_col5, motivation_col6, motivation_col7, motivation_col8 = st.columns(
    8)

# Columns 1 - 6 shows the filters that has been used
with motivation_col1:
    st.metric('School Type', students_school_types_radio)

with motivation_col2:
    st.metric('Teacher Quality', teacher_quality_dropdown)

with motivation_col3:
    st.metric('Resource Access', resourses_access_radio)

with motivation_col4:
    st.metric('Family Income', family_income_dropdown)

with motivation_col5:
    st.metric('Physical Activity', physical_activies_dropdown)

with motivation_col6:
    st.metric('Peer Influence', peer_influence_radio)

# Columns 7 and 8 shows the motivation level of students
with motivation_col7:
    # Shows the minority of students motivation level if there is data from all the filters
    if not filtered_data['Motivation_Level'].empty:
        motivation_min = filtered_data['Motivation_Level'].value_counts(
        ).idxmin()
        st.metric('Minority Motivation Level', motivation_min)
    else:
        st.metric('Minority Motivation Level', 'No data')

with motivation_col8:
    # Shows the majority of students motivation level if there is data from all the filters
    if not filtered_data['Motivation_Level'].empty:
        motivation_max = filtered_data['Motivation_Level'].value_counts(
        ).idxmax()
        st.metric('Majority Motivation Level', motivation_max)
    else:
        st.metric('Majority Motivation Level', 'No data')

# Columns cofiguration for students motivation level charts
motivation_fig1, motivation_fig2 = st.columns(2)

with motivation_fig1:
    # Creates a bar chart for students motivation level based from all the filters
    if not filtered_data['Motivation_Level'].empty:

        # Dataframe that is going to be used in the pie chart
        motivation_count_df = filtered_data.value_counts(
            'Motivation_Level').reset_index()
        motivation_count_df.rename({'Motivation_Level': 'Motivation Level',
                                    'count': 'Amount of Students'}, axis=1, inplace=True)

        motivation_bar = px.bar(
            motivation_count_df,
            title='Students motivation level bar chart',
            y=motivation_count_df['Motivation Level'],
            x=motivation_count_df['Amount of Students'],
            orientation='h',
            color=motivation_count_df['Motivation Level'],
            color_discrete_map={'Low': 'darksalmon',
                                'Medium': 'cornflowerblue', 'High': 'crimson'},
            text_auto=True
        )
        motivation_bar.update_traces(
            textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(motivation_bar, use_container_width=True)
    else:
        # Shows if there is no data found based from all the filters
        st.write('No data found')

with motivation_fig2:
    # Creates a pie chart for students motivation level based from all the filters
    if not filtered_data['Motivation_Level'].empty:

        # Series that is going to be used in the bar chart
        motivation_count_series = filtered_data['Motivation_Level'].value_counts(
        )

        motivation_pie = px.pie(
            motivation_count_series,
            title='Students motivation level pie chart',
            names=motivation_count_series.index,
            values=motivation_count_series.values,
            color=motivation_count_series.index,
            color_discrete_map={'Low': 'darksalmon',
                                'Medium': 'cornflowerblue', 'High': 'crimson'},
            hole=.3
        )
        motivation_pie.update_traces(
            textposition='inside', textinfo='percent+label')

        st.plotly_chart(motivation_pie, use_container_width=True)
    else:
        # Shows if there is no data found based from all the filters
        st.write('No data found')

# Header and bar chart for students motivation based on their gender
st.header('Students Motivation Level by Gender', divider=True)
if not filtered_data['Motivation_Level'].empty:

    # Dataframe that is going to be used in the bar chart
    motivation_by_gender = filtered_data.value_counts(
        ['Motivation_Level', 'Gender']).reset_index()
    motivation_by_gender.rename({'Motivation_Level': 'Motivation Level',
                                'count': 'Amount of Students'}, axis=1, inplace=True)

    motivation_by_gender_bar = go.Figure()

    # Creates a bar chart for male students
    motivation_by_gender_male = motivation_by_gender[(
        motivation_by_gender['Gender'] == 'Male')].reset_index(drop=True)
    motivation_by_gender_bar.add_trace(go.Bar(
        x=motivation_by_gender_male['Motivation Level'],
        y=motivation_by_gender_male['Amount of Students'],
        name='Male',
        marker_color='crimson',
        text=motivation_by_gender_male['Amount of Students'],
        textposition='outside'
    ))

    # Creates a bar chart for female students
    motivation_by_gender_female = motivation_by_gender[(
        motivation_by_gender['Gender'] == 'Female')].reset_index(drop=True)
    motivation_by_gender_bar.add_trace(go.Bar(
        x=motivation_by_gender_female['Motivation Level'],
        y=motivation_by_gender_female['Amount of Students'],
        name='Female',
        marker_color='cornflowerblue',
        text=motivation_by_gender_female['Amount of Students'],
        textposition='outside'
    ))

    # Combines the two bar charts into one
    motivation_by_gender_bar.update_layout(
        barmode='group', xaxis_title='Motivation Level', yaxis_title='Amount of Students')

    st.plotly_chart(motivation_by_gender_bar, use_container_width=True)
else:
    # Shows if there is no data found based from all the filters
    st.write('No data found')
