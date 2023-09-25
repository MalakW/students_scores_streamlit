#import the required libraries 
from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px  
import plotly.graph_objects as go
import streamlit.components.v1 as components

#setting wide screen page for streamlite
st.set_page_config(layout = 'wide')

#loading the data set
path = "StudentsPerformance.csv"
df = pd.read_csv(path)    

#create age and total columns 
df['total'] = df['math score'] + df['reading score'] + df['writing score']
df['age'] = np.random.randint(11,17, size = len(df))

# Define custom color palette
custom_colors = ['#0C356A', '#279EFF', '#40F8FF', '#D5FFD0']

# Menu bar
selected = option_menu(
    menu_title=None,
    options=["Home", "Gender", "Scores"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "nav-link-selected": {
            "background-color": "#279EFF",  # Color for the selected option
            "color": "white",  # Text color for the selected option
        },
        "nav": {
            "background-color": "#0C356A",  # Background color for the menu
            "padding": "10px",
            "border-radius": "10px",
        },
        "nav-link": {
            "color": "white",  # Text color for the menu options (switched to white)
            "font-size": "16px",  # Font size for the menu options
            "margin": "5px",
        },
    },
)

#Gender Page
if selected == "Gender":
    # Center the charts using custom CSS
    st.markdown(
        """
        <style>
            .css-1aumxhk {
                display: flex;
                justify-content: center;
            }
        </style>
        """,
        unsafe_allow_html=True)
    
    # Title
    st.header("Gender Distribution of Students")

    # Histogram
    fig = px.histogram(df, x='gender', 
                       color='gender', 
                       labels={'gender':'Gender'},
                       color_discrete_sequence=['#0C356A', '#279EFF', '#40F8FF', '#D5FFD0'])
    
    fig.update_xaxes(showgrid=False)  # Remove x-axis grid lines
    fig.update_yaxes(showgrid=False)  # Remove y-axis grid lines
    
    st.plotly_chart(fig, use_container_width=True)
    st.text('The female distribution of students is higher than that of male.')
    
    # Dropdown for team selection
    selected_option = st.selectbox("Select Team", sorted(df['team'].unique()))

    # Display gender distribution based on selection
    st.header(f"Gender Distribution for Team {selected_option}")
    st.text(f'The pie plot shows the gender distribution of each group in the class.')

    if selected_option == "Overall Gender Distribution":
        gender_counts = df['gender'].value_counts()
    else:
        team_data = df[df['team'] == selected_option]
        gender_counts = team_data['gender'].value_counts()

    if not gender_counts.empty:
        pie_fig = px.pie(gender_counts, 
                         values=gender_counts.values, 
                         names=gender_counts.index,
                         color_discrete_sequence=['#0C356A', '#279EFF', '#40F8FF', '#D5FFD0'])
        
        # Centering the pie chart using CSS
        c = f"""
            <style>
                .chart-container {{
                    display: flex;
                    justify-content: center;
                }}
            </style>
        """
        
        st.markdown(c, unsafe_allow_html=True)
        
        components.html(pie_fig.to_html(full_html=False), height=500)
    else:
        st.warning(f"No data available for Team {selected_option}")
        
# Displaying text analysis for the pie chart
    if selected_option == "group A":
        st.text("The female gender is higher than male for group A.")
    elif selected_option == "group B":
        st.text("The female gender is higher than male for group B.")
    elif selected_option == "group C":
        st.text("The female gender is higher than male for group C.")
    elif selected_option == "group D":
        st.text("The female gender is higher than male for group D.")
    else:
        st.text(f"The female gender is higher than male for group E.")

#Scores Page
if selected == "Scores":
    st.markdown(
        """
        <style>
            .css-3mmywe {
                display: flex;
                justify-content: center;
            }
        </style>
        """,
        unsafe_allow_html=True)
    
    st.subheader("Total Scores by Group and Subject")

    # Group by 'team' and sum the scores
    scores_by_group = df.groupby('team')[['math score', 'reading score', 'writing score']].sum()

    # Create an interactive bar chart
    fig = px.bar(scores_by_group, barmode='group', color_discrete_sequence=['#0C356A', '#279EFF', '#40F8FF', '#D5FFD0'])
    fig.update_layout(
                      xaxis_title="Group",
                      yaxis_title="Total Score",
                      legend_title="Subject",
                      xaxis={'categoryorder':'array', 'categoryarray':['group A', 'group B', 'group C', 'group D', 'group E']})

    fig.update_xaxes(showgrid=False)  # Remove x-axis grid lines
    fig.update_yaxes(showgrid=False)  # Remove y-axis grid lines
    st.plotly_chart(fig)
    st.text('Group C has the hightest score compared to other groups.')
    
    df = df[~df['parental level of education'].isin(['some college', 'some high school'])]
    
    #selected_education = st.sidebar.selectbox("Select Parental Level of Education", df['parental level of education'].unique())
    selected_score = st.selectbox("Select Subject", ['math score', 'reading score', 'writing score'])
    filtered_df = df[selected_score]
    
    st.subheader(f"The effect of Parental education level on the student's {selected_score}")

# Group by parental level of education and calculate the mean score
mean_scores = df.groupby('parental level of education')[selected_score].mean().reset_index()


st.subheader(f"The effect of Parental education level on the student's {selected_score}")

# Group by parental level of education and calculate the mean score
mean_scores = df.groupby('parental level of education')[selected_score].mean().reset_index()

# Apply the color palette directly to the DataFrame
mean_scores[selected_score] = mean_scores[selected_score].astype(str)  # Convert to string for color assignment
mean_scores['color'] = mean_scores[selected_score].map({
    '0C356A': '#0C356A',
    '279EFF': '#279EFF',
    '40F8FF': '#40F8FF',
    'D5FFD0': '#D5FFD0'
})

# Create an interactive bar chart
fig = px.bar(mean_scores, x='parental level of education', y=selected_score, color='color')

# Update the layout for better visualization
fig.update_layout(
    xaxis_title="Parental Level of Education",
    yaxis_title=f"Mean {selected_score.capitalize()} Score"
)
fig.update_xaxes(showgrid=False)  # Remove x-axis grid lines
fig.update_yaxes(showgrid=False)  # Remove y-axis grid lines

  # Centering the chart using HTML and CSS
        st.write(
        f"""
        <div style="display: flex; justify-content: center;">
            {fig.to_html(full_html=False)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if selected_score == "math score":
        st.text(f"The students that their parent are of master's degree have the highest score for {selected_score}. ")
    elif selected_score == "reading score":
        st.text(f"The students that their parent are of master's degree have the highest score for {selected_score}. ")
    elif selected_score == "writing score":
       st.text(f"The students that their parent are of master's degree have the highest score for {selected_score}. ")
    
    st.subheader(f"Interaction between Test Preparation Course and Scores")
    
    # Group by 'test preparation course' and calculate the mean score for each subject
    mean_scores = df.groupby('test preparation course')[['math score', 'reading score', 'writing score']].mean().reset_index()
    colors = ['#0C356A', '#279EFF', '#40F8FF']
    
    # Create a grouped bar chart
    fig = go.Figure()
    
    subjects = ['math score', 'reading score', 'writing score']
    
    for i, subject in enumerate(subjects):
        subject_data = mean_scores[['test preparation course', subject]]
        fig.add_trace(go.Bar(
            x=subject_data['test preparation course'],
            y=subject_data[subject],
            name=subject,
            marker_color=colors[i]
        ))
    
    # Update the layout for better visualization
    fig.update_layout(
                      xaxis_title="Test Preparation Course",
                      yaxis_title="Mean Score")
    
    # Display the bar chart
    st.plotly_chart(fig)

    st.text('The graph shows that the students who took the test preparation course got higher score than those who didn\'t.')  

#Home Page
if selected == 'Home':
    st.title('Rising Stars: Test Prep Unlocks Potential')

    story = """
In a bustling academic arena, students are on a quest for knowledge and excellence. Among them, a group of young scholars stands out, each armed with their own unique potential.

Our story begins in a diverse cohort, where students are faced with the choice of embarking on a test preparation course. The path they choose will shape their academic journey.

As the data unveils, a revelation emerges. Those who dared to seize the opportunity presented by the test preparation course soared to new heights. Their scores in math, reading, and writing blossomed, painting a vivid picture of the power of preparation.

This data-driven tale reminds us that with the right tools and a spark of determination, every student has the potential to shine. The choice to embark on the journey of preparation is a step towards unlocking one's true academic prowess.

In this dynamic academic landscape, we witness the birth of rising stars, leaving a trail of inspiration for generations to come.
"""

    # Display the story with some styling
    st.markdown(
        f"""
        <div style="padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
            <p style="font-size: 18px; line-height: 1.6;">{story}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
