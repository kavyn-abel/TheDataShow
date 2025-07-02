import streamlit as st

#------------------------------------------------------------------------------
# For the logo
# Create 3 columns
col1, col2, col3 = st.columns([1, 2, 1])

# Put the image in the center column
with col2:
    # st.image('The Data Show Logo1.png', use_column_width=True)
    # st.image('TheDataShowAnimatedLogo.gif', use_column_width=True) # Deprecated
    st.image('TheDataShowAnimatedLogo.gif', use_container_width=True)
#------------------------------------------------------------------------------
# Intro to data science
st.write()
st.write()
st.write('Welcome to The Data Show!')
st.write('I am excited to introduce you to the field of data science. Data scientists work with data to find insights that help people in all kinds of fields make informed decisions. The abilities of a data scientist are needed by businesses, sports teams, in medicine, government, and much more. These skills include programming and statistics, along with data storage, manipulation, analysis, and visualization.')
st.write('This app is designed to give you examples of ways data scientists work with data. They use dataframes as a way to organize data in rows and columns:')
st.image('dataframe.png')
st.write('Image source: *https://www.geeksforgeeks.org/pandas/python-pandas-dataframe/*')
st.write('Data scientists make charts to visualize data and help others understand patterns, trends, and other insights that may be helpful:')
st.image('chart_types.png')
st.write('Image source: *https://www.datamation.com/big-data/data-visualization-use-cases/*')
st.write('Additionally, this app will show you how data scientists work with data in code to create new columns, sort data, filter it, and work with textual data. The image below shows some logos of tools that data scientists may use:')
st.image('data_science_tools.png')
st.write('Image source: *https://www.linkedin.com/pulse/data-science-full-stack-roadmap-2022-himanshu-ramchandani/*')

# Use the data_science image I've saved here?

st.write('')
st.write('Let\'s dive in.')
st.write('Please select \'Topics\' in the sidebar at the left, and then choose a topic to explore.')
    
