import pandas as pd
import streamlit as st
import plotly.express as px

# Tab configuration
st.set_page_config(
    page_title='Student Performance',
    page_icon=':bar_chart:',
    layout='wide'
)


@st.cache_data  # Caches the dataframe
def load_data():
    df = pd.read_csv('part_2/StudentPerformanceFactors.csv')
    return df


# Puts the dataframe in a variable
df = load_data()

# Title and description of the page
st.title('Student Performance Factors')
st.write('''
         The dataset that is used in this dashboard provides a comprehensive 
         overview of various factors affecting student performance in exams.
         ''')

# Header and columns configuration for amount of student
st.header('Amount of Students', divider=True)
amount_col1, amount_col2, amount_col3 = st.columns(3)

with amount_col1:
    public_students = int(df[df['School_Type'].str.contains(
        'Public')]['School_Type'].value_counts())
    st.metric('Public School Students', f'{public_students}')

with amount_col2:
    private_students = int(df[df['School_Type'].str.contains(
        'Private')]['School_Type'].value_counts())
    st.metric('Private School Students', f'{private_students}')

with amount_col3:
    st.metric('Total Amount of Students', f'{len(df)}')

# Header and columns configuration for amount of students by gender chart
st.header('Amount of Students by Gender', divider=True)
gender_col1, gender_col2 = st.columns(2)

with gender_col1:
    gender_grp = df.groupby('Gender')
    gender_amount_pie = px.pie(
        gender_grp,
        values=gender_grp['Gender'].value_counts().values,
        names=gender_grp['Gender'].value_counts().index
    )
    gender_amount_pie.update_traces(
        textposition='inside', textinfo='percent+label')
    st.plotly_chart(gender_amount_pie, use_container_width=True)

with gender_col2:
    gender_per_school_type = df.value_counts(
        ['School_Type', 'Gender']).reset_index()
    gender_per_school_type.rename(
        {'School_Type': 'School Type', 'count': 'Amount of Students'}, axis=1, inplace=True)
    gender_amount_bar = px.bar(
        gender_per_school_type,
        x=gender_per_school_type['Gender'],
        y=gender_per_school_type['Amount of Students'],
        color=gender_per_school_type['School Type'],
        barmode='group'
    )
    st.plotly_chart(gender_amount_bar, use_container_width=True)
