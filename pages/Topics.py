import streamlit as st
import pandas as pd
import altair as alt
import io
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Set the page wide to help with the squished dataframes.
# st.set_page_config(layout="wide")

# For the logo
# Create 3 columns
col1, col2, col3 = st.columns([1, 2, 1])

# Put the image in the center column
with col2:
    # st.image('The Data Show Logo1.png', use_column_width=True)
    # st.image('The Data Show Logo1.png', use_column_width=True) # Deprecated
    st.image('The Data Show Logo1.png', use_container_width=True)


# Classes and Functions

def divider_line():
            st.markdown(
    "<hr style='border: 2px solid #FFFFFF;'>",
    unsafe_allow_html=True
)

class Birthday:
    # Note - data is just information.
    def load_birthday_data():
        st.write('We\'re gonna talk about birthday data.')
        st.write('Here\'s the url for the data we\'ll be using. This data includes the number of births for each day of the year in the U.S. for the years 2000-2014. Click on the link below to see the raw data.')
        st.write('https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_2000-2014_SSA.csv')

        st.write('Let\'s bring in that data with Python code.')

        url = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_2000-2014_SSA.csv'
        birthday_df = pd.read_csv(url)

        st.write("Here\'s how that data looks when we've brought it into a pandas dataframe with Python code:")
        # A dataframe is like a table in excel, with rows and columns.
        st.dataframe(data = birthday_df.head(), hide_index=True)

        # Expander for how we did that
        with st.expander("How did we bring that data into python?"):
            code = '''# We used this python code to read in the csv file.
url = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_2000-2014_SSA.csv'
birthday_df = pd.read_csv(url)

# Then displayed the first 5 rows of the dataframe in the app.
st.dataframe(data = birthday_df.head(), hide_index=True)
    '''
            st.code(code, language="python")

        return birthday_df


    def calculate_births_by_year():
        divider_line()

        st.write('With this data we can find out things such as which year had the most births.')
        st.write('We can do this by summing the number of births within each year. We can look at the results in the chart below (If you hover over a bar in the chart, it will show you the number of births for that year):')

        # Get the number of births per year
        years_df = birthday_df.groupby("year").sum().reset_index()
        # Filter the dataframe
        years_df1 = years_df[["year", "births"]]

        # Here's alook at the data
        # st.table(data = years_df1)

        births_year_chart = (alt.Chart(years_df1).mark_bar().encode(
            x = alt.X('year:Q', title = 'Year'),
            y = alt.Y('births:Q', title = 'Total Births') # , scale=alt.Scale(domain=[3500000, 4500000]) This scale was breaking the chart in the live app.
        ))

        st.altair_chart(births_year_chart, theme = None)

        st.write('Here we can see, according to our data, that the most births were in the year 2007.')

        with st.expander("How did we get there?"):
            code = '''# We aggregated the data to get the number of births per year.
years_df = birthday_df.groupby("year").sum().reset_index()

# We created the chart with the altair library.
births_year_chart = alt.Chart(years_df1).mark_bar().encode(
    x = alt.X('year', title = 'Year'),
    y = alt.Y('births', title = 'Total Births')
)

# We presented the chart in the app.
st.altair_chart(altair_chart = births_year_chart, theme = None)
        '''
            st.code(code, language="python")


    def display_users_birthday_commonality(month_dict:dict):
        # Want user to be able to find out of the 365 days in a year how common there's is. 
        # ie it is the 103rd most common birthday.

        # Filtered the data to desired columns
        days_df = birthday_df[['month', 'date_of_month', 'births']]

        # Aggregated the data by each month and day of the year.
        days_df1 = days_df.groupby(["month", "date_of_month"]).sum().reset_index()

        # Sorted the data
        top_days_df = days_df1.sort_values(by = ['births'], ascending = False)

        # Added a numbering to the data
        top_days_df['row_number'] = range(1, len(top_days_df) + 1)
        # st.table(top_days_df.head())

        # Add a column for the last digit
        top_days_df['last_digit'] = top_days_df['row_number'] % 10

        # Conditionally set a suffix column based off the last_digit for the row_number
        def simple_suffix(d):
            if d == 1:
                return 'st'
            elif d == 2:
                return 'nd'
            elif d == 3:
                return 'rd'
            else:
                return 'th'

        top_days_df['suffix'] = top_days_df['last_digit'].apply(simple_suffix)

        divider_line()
        st.write('Want to find out how common your birthday is?')
        st.write('Enter your birthday below and we\'ll tell you how common it is out of the 366 days in a year.')

        # Collect an input date from the user
        input_date = st.date_input('What is your birthday? (Just get the right month and day, the year doesn\'t matter)')

        # st.write(input_date)

        # Extract the month and day entered by the user.
        input_month = input_date.month
        input_day = input_date.day

        # st.write(f"Month: {input_month}")
        # st.write(f"Day: {input_day}")

        # Filter the data to the input month and day
        user_birthday_df = top_days_df[top_days_df['month'] == input_month]
        user_birthday_df1 = user_birthday_df[user_birthday_df['date_of_month'] == input_day]
        # st.table(user_birthday_df1)

        # Set up the row_number/commonality concatenated with the suffix, ready for display
        user_birthday_df1['birthday_commonality'] = user_birthday_df1['row_number'].astype(str) + user_birthday_df1['suffix']

        # Pull the birthday_commonality field
        user_birthday_commonality = user_birthday_df1['birthday_commonality'].iloc[0]

        # Display back to the user.
        st.write(f'Your birthday is the {user_birthday_commonality} most common birthday.')

        # Explainer block
        with st.expander("How did we do this?"):
            code = '''
# We filtered the data to desired columns.
days_df = birthday_df[['month', 'date_of_month', 'births']]

# Aggregated the data by each month and day of the year.
days_df1 = days_df.groupby(["month", "date_of_month"]).sum().reset_index()

# Sorted the data from the most births down to the least.
top_days_df = days_df1.sort_values(by = ['births'], ascending = False)

# Added a row numbering to the data so that number 1 has the most births and 
# 366 has the least.
top_days_df['row_number'] = range(1, len(top_days_df) + 1)

# Added a column for the last digit.
top_days_df['last_digit'] = top_days_df['row_number'] % 10

# Conditionally set a suffix column based off the last_digit for the 
# row_number.
def simple_suffix(d):
    if d == 1:
        return 'st'
    elif d == 2:
        return 'nd'
    elif d == 3:
        return 'rd'
    else:
        return 'th'

top_days_df['suffix'] = top_days_df['last_digit'].apply(simple_suffix)

# Collected an input date from the user.
input_date = st.date_input('What is your birthday?')

# Extracted the month and day entered by the user.
input_month = input_date.month
input_day = input_date.day

# Filtered the data to the input month and day.
user_birthday_df = top_days_df[top_days_df['month'] == input_month]
user_birthday_df1 = user_birthday_df[user_birthday_df['date_of_month'] == input_day]

# Set up the row_number/commonality concatenated with the suffix, ready 
# for display.
user_birthday_df1['birthday_commonality'] = user_birthday_df1['row_number'].astype(str) + user_birthday_df1['suffix']

# Pulled the row_number field (that we created earlier) from the chosen date.
#(This will tell us how common of the 366 days this day is for births).
user_birthday_commonality = user_birthday_df1['birthday_commonality'].iloc[0]

# Displayed that number back to the user.
st.write(f'Your birthday is the {user_birthday_commonality} most common birthday.')
        '''
            st.code(code, language="python")

        # Convert to actual months instead of numbers before displaying the most common birthdays to the user.

        top_days_df1 = top_days_df.copy()
        top_days_df1['month'] = top_days_df1['month'].replace(month_dict)

        top_days_df2 = top_days_df1[['month', 'date_of_month', 'births']]

        st.text('')
        st.text('')
        st.write('Here\'s a look at the most common birthdays:')
        st.dataframe(top_days_df2.head(10), hide_index=True)

        return days_df1


    def least_common_birthdays(days_df:pd.DataFrame, month_dict:dict):
        divider_line()
        st.write('Next, let\'s take a look at the days with the lowest number of births. Do you see anything interesting?')
        # Lowest number of birth days
        low_days_df = days_df1.sort_values(by = 'births', ascending = True)

        # Map to the actual month names before displaying
        low_days_df1 = low_days_df.copy()
        low_days_df1['month'] = low_days_df1['month'].replace(month_dict)

        st.dataframe(low_days_df1.head(10), hide_index=True)

        st.text_area('Write what you observe about this data:')

        # How we got there box
        with st.expander("How did we get to this lowest number of births view of the data?"):
            code = '''# We sorted the data starting from the lowest number of births, going up.
low_days_df = days_df1.sort_values(by = 'births', ascending = True)

# We mapped the months as numbers to their actual names with an earlier 
# defined dictionary called month_dict.
low_days_df1 = low_days_df.copy()
low_days_df1['month'] = low_days_df1['month'].replace(month_dict)

# Displayed the data back to the user in the app.
st.dataframe(low_days_df1.head(10), hide_index=True)
        '''
            st.code(code, language="python")


class Movie:
    def load_movie_data():
        st.write('Let\'s talk movies!')
        st.write('In this section we are looking at data from movies released since 2022 until August 2023.')
        st.write('Here is the original dataset, if you\'re interested: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset')
        st.write('In this section we are working off of the movies_metadata.csv that is found there.')
        # The original kaggle movie dataset is in here: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset
    # I am working with the movies_metadata.csv

        # Open the CSV file in read mode
        with open("movies_since_2022_select_columns.csv", "r", encoding="utf-8") as f:
            csv_raw = f.read()  # Read the full content as a string

        # Split the raw CSV into lines
        lines = csv_raw.splitlines()

        # Limit to the first N lines (e.g., header + 5 rows)
        row_limit = 3
        limited_csv_raw = "\n".join(lines[:row_limit+1])  # +1 to include header

        # Display the limited content
        st.text_area(f"Here are the first {row_limit} rows of the raw data:", limited_csv_raw, height=200)

        st.write('Messy, right? We\'ll bring that data in with Python code.')

        # Read in the data
        recent_movies_df = pd.read_csv('movies_since_2022_select_columns.csv')

        # Filter the columns to what I want to work with
        # recent_movies_df1 = recent_movies_df[['title', 'vote_average', 'vote_count', 'release_date', 'revenue', 
        #                             'runtime', 'budget', 'genres']]
        recent_movies_df1 = recent_movies_df[['title', 'vote_average', 'vote_count', 'release_date', 'revenue', 
                                     'runtime', 'budget', 'genres']]
        
        st.write('Here\'s how that data looks brought into a dataframe with Python code:')
        st.dataframe(recent_movies_df1.head(), hide_index=True)

        with st.expander("How did we bring that data into Python?"):
            code = '''# We read in the data into a dataframe from a csv file.
recent_movies_df = pd.read_csv('movies_since_2022.csv')

# Next, we displayed the first 5 rows of data to you in the app.
st.dataframe(recent_movies_df1.head(), hide_index=True)
        '''
            st.code(code, language="python")


        return recent_movies_df1
    
        

    def movie_vote_averages(recent_movies_df1:pd.DataFrame):
        divider_line()
        st.write('Now, let\'s sort the data by the vote average and see what movies, on average, get the highest vote rating out of 10.')
        highest_vote_avg = recent_movies_df1.sort_values('vote_average', ascending = False)
        st.dataframe(highest_vote_avg.head(), hide_index=True)
        st.write('Notice anything? These movies have a 10 point average, but have you heard of them? Maybe not, because there is only 1 vote for each of these movies.')

        st.text('')
        st.write('So, let\'s also sort by the vote count as well and see how that looks.')
        highest_vote_avg_and_count = recent_movies_df1.sort_values(['vote_average', 'vote_count'], ascending = False)
        st.dataframe(highest_vote_avg_and_count.head(), hide_index=True)
        st.write('Ok, still very few votes.')

        st.text('')
        st.write('What if we take a look at movies that have at least 500 votes- still sorted by the vote average and vote count.')
        # Now what if we have to look at the data where there has to be at least 500 votes
        highest_vote_avg_and_count1 = highest_vote_avg_and_count[highest_vote_avg_and_count['vote_count'] > 500]
        st.dataframe(highest_vote_avg_and_count1.head(), hide_index=True)
        st.write('See the difference between this and our first output in this section?')

        
        with st.expander("How did we do this?"):
            code = '''# We sorted the data by the vote average.
highest_vote_avg = recent_movies_df1.sort_values('vote_average', ascending = False)

# Next, we additionally sorted by the vote count.
highest_vote_avg_and_count = recent_movies_df1.sort_values(['vote_average', 'vote_count'], ascending = False)

# Finally, we took this sorted data and filtered to movies that had 
# at least 500 votes.
highest_vote_avg_and_count1 = highest_vote_avg_and_count[highest_vote_avg_and_count['vote_count'] > 500]
        '''
            st.code(code, language="python")

        # popular_movie_data = highest_vote_avg_and_count1.head()

        # popular_movie_chart = (alt.Chart(popular_movie_data).mark_bar().encode(
        #     x = alt.X('title', title = 'Movie Title'),
        #     y = alt.Y('vote_average', title = 'Vote Average') #  , scale=alt.Scale(domain=[8, 9])
        # ))

        # st.altair_chart(popular_movie_chart, theme = None)

    def most_profitable_movies(recent_movies_df1:pd.DataFrame):
        # Feature engineering
        divider_line()
        st.write('Let\'s make a column called Box Office Margin. We calculate this by subtracting the budget from the revenue.')
        bom_df = recent_movies_df1.copy()
        bom_df['Box Office Margin'] = bom_df['revenue'] - bom_df['budget']

        st.text('')
        st.write('Let\'s take a look at it (scroll all the way to the right ):')
        st.dataframe(bom_df.head(1), hide_index=True)

        st.text('')
        st.write('We\'ll sort the data now by the Box Office Margin, and look at movies with at least 100 votes.')
        # Where there are at least 100 votes
        bom_df1 = bom_df[bom_df['vote_count'] > 100]

        # And sort by Box Office Margin
        bom_df2 = bom_df1.sort_values('Box Office Margin', ascending = False)
        # st.table(bom_df2.head(10))

        st.write('Here is a chart showing the top 5 movies with that criteria. (You can hover over a bar to get the exact Box Office Margin for that movie)')

        # Chart for most profitable movies
        bom_movie_data = bom_df2.head(5)
        bom_movie_chart = (alt.Chart(bom_movie_data).mark_bar().encode(
            x = alt.X('title', title = 'Movie Title'),
            y = alt.Y('Box Office Margin', title = 'Box Office Margin ($)') #  , scale=alt.Scale(domain=[8, 9])
        ))

        st.altair_chart(bom_movie_chart, theme = None)

        with st.expander("How did we do this?"):
            code = '''# We created a new column from ones that we already had (That's called 
# feauture engineering).
# We made a column that calculates the difference between revenue and budget.
bom_df = recent_movies_df1.copy()
bom_df['Box Office Margin'] = bom_df['revenue'] - bom_df['budget']

# We filtered the data to show us records where there are more than 100 votes.
bom_df1 = bom_df[bom_df['vote_count'] > 100]

# Then we sorted by Box Office Margin. Highest to lowest.
bom_df2 = bom_df1.sort_values('Box Office Margin', ascending = False)

# Lastly we created a chart to show the top 5 movies according to their Box 
# Office Margin.
bom_movie_data = bom_df2.head(5)
bom_movie_chart = (alt.Chart(bom_movie_data).mark_bar().encode(
    x = alt.X('title', title = 'Movie Title'),
    y = alt.Y('Box Office Margin', title = 'Box Office Margin')
))

# And displayed the chart in the app.
st.altair_chart(bom_movie_chart, theme = None)
        '''
            st.code(code, language="python")

        return bom_df2



    def stats_by_genre(bom_df2:pd.DataFrame):
        divider_line()
        st.write('Lastly, here\'s an interactive piece working with movie genres.')
        # Define list of common genre's (according to the data set)
        genre_list = ['Drama', 'Comedy', 'Horror', 'Animation', 'Music', 'Thriller', 'Action', 'Romance', 'Science Fiction','Crime'] # 'Documentary'

        # Allow the user to select from this list
        user_genre = st.selectbox('Please select a genre:', genre_list)

        # st.write(f'You selected {user_genre}.')

        # Filter the bom_df to the chosen genre
        # genre_profit_df = profit_df2[profit_df2['genres'] == user_genre]
        # Instead filter to movies that include the chosen genre- not to those that are only, singly, that genre.
        genre_bom_df = bom_df2[bom_df2['genres'].str.contains(rf'\b{user_genre}\b', case=False, na=False)]
        # This is so much better, plus I can introduces regex!

        # Title of the most profitable movie of that genre
        genre_title_df = genre_bom_df['title'].iloc[0]
        # Budget
        genre_budget_df = genre_bom_df['budget'].iloc[0]
        # Revenue
        genre_rev_df = genre_bom_df['revenue'].iloc[0]
        # Box Office Margin
        genre_bom_df1 = genre_bom_df['Box Office Margin'].iloc[0]
        # Vote average
        genre_vote_avg_df = genre_bom_df['vote_average'].iloc[0]
        # Number of votes
        genre_vote_count = genre_bom_df['vote_count'].iloc[0]

        # Display to the user these items of the top movie in the chosen genre
        st.write(f'The title of the top movie in {user_genre} is {genre_title_df}.')
        # st.write(f'The budget of the top movie in {user_genre} is {genre_budget_df}')
        # st.write(f'The revenue of the top movie in {user_genre} is {genre_rev_df}')
        # st.write(f'The profit of the top movie in {user_genre} is {genre_profit_df1}')
        st.write(f'The vote average is {genre_vote_avg_df}, with a total number of {genre_vote_count:,} votes.')

        col1, col2, col3 = st.columns(3)
        col1.metric("Revenue", f"{genre_rev_df:,}")
        col2.metric("Budget", f"{genre_budget_df:,}")
        col3.metric("Box Office Margin", f"{genre_bom_df1:,}")

        with st.expander("How did we do this?"):
            code = '''# We defined a list of genres.
genre_list = ['Drama', 'Comedy', 'Horror', 'Animation', 'Music', 'Thriller', 'Action', 'Romance', 'Science Fiction','Crime']
        
# We allowed the user to select from that list.
user_genre = st.selectbox('Choose a genre', genre_list)

# Next, we filtered our Box Office Margin dataframe to any movies that 
# have that genre included in their list of genres.
# This is done with what is called regular expressions, or regex. This 
# allows us to search through textual data.
genre_bom_df = bom_df2[bom_df2['genres'].str.contains(rf'\\b{user_genre}\\b', case=False, na=False)]

# As the dataframe is already sorted from highest to least Box 
# Office Margin we need to extract the details from the first 
# record which will have the highest margin movie in that genre.

# Extract the title of the top Box Office Margin movie of that genre and 
# save it to a variable.
genre_title_df = genre_bom_df['title'].iloc[0]
# Do the same with budget
genre_budget_df = genre_bom_df['budget'].iloc[0]
# And revenue
genre_rev_df = genre_bom_df['revenue'].iloc[0]
# Box Office Margin
genre_bom_df1 = genre_bom_df['profit'].iloc[0]
# Vote average
genre_vote_avg_df = genre_bom_df['vote_average'].iloc[0]
# Number of votes
genre_vote_count = genre_bom_df['vote_count'].iloc[0]

# After saving these items into variables, we displayed them to the user.
st.write(f'The title of the top movie in {user_genre} is {genre_title_df}.')
st.write(f'The vote average is {genre_vote_avg_df}, with a total number of {genre_vote_count:,} votes.')

# This code here shows us those metrics in the app and adds a comma separator 
# to the large number values.
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", f"{genre_rev_df:,}")
col2.metric("Budget", f"{genre_budget_df:,}")
col3.metric("Box Office Margin", f"{genre_bom_df1:,}")
        '''
            st.code(code, language="python")


class Titanic:
    def load_titanic_data():
        st.write('Alright, the Titanic!')
        st.write('In this section we are looking at passenger data from the Titanic, which sank in the North Atlantic Ocean on April 15, 1912.')
        st.write('Here is the original dataset, if you\'re interested: https://www.kaggle.com/datasets/yasserh/titanic-dataset/data?select=Titanic-Dataset.csv')

        # Here is a link to the titanic kaggle dataset: https://www.kaggle.com/datasets/yasserh/titanic-dataset/data?select=Titanic-Dataset.csv
        # Open the CSV file in read mode
        with open("titanic_dataset.csv", "r", encoding="utf-8") as f:
            csv_raw = f.read()  # Read the full content as a string

        # Split the raw CSV into lines
        lines = csv_raw.splitlines()

        # Limit to the first N lines (e.g., header + 5 rows)
        row_limit = 3
        limited_csv_raw = "\n".join(lines[:row_limit+1])  # +1 to include header

        # Display the limited content
        st.text_area(f"Here are the first {row_limit} rows of the raw data:", limited_csv_raw, height=150)

        st.write('Kind of hard to follow, right? We\'ll bring that data in with Python code.')

        st.write('Here\'s how that data looks brought into a dataframe with Python code:')

        titanic_df = pd.read_csv('titanic_dataset.csv')
        st.dataframe(titanic_df.head(), hide_index=True)

        with st.expander("How did we bring that data into Python?"):
            code = '''# We read in the data into a dataframe from a csv file.
titanic_df = pd.read_csv('titanic_dataset.csv')

# Then, we displayed the first 5 rows of data to you in the app.
st.dataframe(titanic_df.head(), hide_index=True)
        '''
            st.code(code, language="python")

        divider_line()

        st.write('Let\'s take a look at the dataset info to understand what we are working with.')
        st.write('When working with a new dataset it can be helpful to understand the data overall. This info below shows us how many columns there are, the names of those columns, and how many non-null (or empty) values there are. It appears there are only a few columns that have missing data. That last piece is the type of data that the column contains.')
        # Capture the df.info() output
        buffer = io.StringIO()
        titanic_df.info(buf=buffer)
        titanic_df_info = buffer.getvalue()

        # Display in Streamlit
        st.text(titanic_df_info)

        with st.expander("How do we see the info of a dataset in Python?"):
            code = '''# We use the .info() command like this on our dataframe.
titanic_df.info()
        '''
            st.code(code, language="python")

        # Rename Sex to Gender
        titanic_df.rename(columns={'Sex':'Gender'}, inplace = True)

        return titanic_df
        
    def pie_charts(titanic_df:pd.DataFrame):
        divider_line()

        st.write('Data can be visualized to help us gain more understanding and insight than we can from the individual rows of data. Here are some pie charts that help us learn more about the gender and class distributions of the Titanic passengers. (You can hover over each section in the charts for more info.)')
        st.write('Here we can see that there are more males than females aboard the titanic:')
        
        # Look at gender data in a pie chart
        gender_chart = alt.Chart(titanic_df).mark_arc().encode(
            theta=alt.Theta(field='Gender', type='nominal', aggregate='count'),
            color=alt.Color('Gender:N'),
            tooltip=[alt.Tooltip('Gender:N'), alt.Tooltip('count():Q')]
        ).properties(title = 'Gender Distribution')

        st.altair_chart(gender_chart, theme = None)

        st.write('This chart below shows us that there are much more third class passengers than first and second class:')

        # Pclass pie chart
        pclass_chart = alt.Chart(titanic_df).mark_arc().encode(
            theta=alt.Theta(field='Pclass', type='nominal', aggregate='count'),
            color=alt.Color('Pclass:N'),
            tooltip=[alt.Tooltip('Pclass:N'), alt.Tooltip('count():Q')]
        ).properties(title = 'Pclass Counts')

        st.altair_chart(pclass_chart, theme = None)

        with st.expander("How did we make these charts from the data?"):
            code = '''# We used this alt.Chart function to create the chart. The .mark_arc() piece 
# tells the function that we want a pie chart.
gender_chart = alt.Chart(titanic_df).mark_arc().encode(
    theta=alt.Theta(field='Gender', type='nominal', aggregate='count'),
    color=alt.Color('Gender:N'),
    tooltip=[alt.Tooltip('Gender:N'), alt.Tooltip('count():Q')] # This tooltip allows you to hover the actual chart and see some information.
).properties(title = 'Gender Distribution') # This title property allows us to choose the title for the chart.

# Next, we display the chart in the app.
st.altair_chart(gender_chart, theme = None)

# Pclass pie chart.
pclass_chart = alt.Chart(titanic_df).mark_arc().encode(
    theta=alt.Theta(field='Pclass', type='nominal', aggregate='count'),
    color=alt.Color('Pclass:N'),
    tooltip=[alt.Tooltip('Pclass:N'), alt.Tooltip('count():Q')]
).properties(title = 'Pclass Counts')

# Display the chart in the app.
st.altair_chart(pclass_chart, theme = None)
        '''
            st.code(code, language="python")


    def class_data(titanic_df:pd.DataFrame):
        divider_line()

        # Was a certain class more likely to survive?
        st.write('As we saw in the pie chart there are three classes of passengers. First class, Second class, and Third class. Were passengers of a certain class more likely to survive?')
        st.write('Let\'s find out.')

        st.write('Here are the number of passengers in each class.')
        pclass_df = titanic_df.copy()

        # Get the count of passengers for each class
        class_count_df = pclass_df.groupby('Pclass').agg(Passenger_Count = ('Survived', 'count'))
        st.dataframe(class_count_df)

        st.write('Here are the number of passengers that survived in each class.')
        # Let's sum survived by pclass
        pclass_df1 = pclass_df[['Pclass', 'Survived']]
        pclass_df2 = pclass_df1.groupby('Pclass').agg(Number_Survived = ('Survived', 'sum'))
        st.dataframe(pclass_df2)

        # Join the dataframes
        survival_rate_df = pd.merge(left = class_count_df, right = pclass_df2, on = 'Pclass', how = 'left')

        # Create a calculated column for the survival rate
        survival_rate_df['Survival_Rate'] = survival_rate_df['Number_Survived'] / survival_rate_df['Passenger_Count']

        # survival_rate_df = pclass_df2 / class_count_df

        # Combine into a DataFrame
        # class_survival_df = pd.DataFrame({
        #     'Total': class_count_df,
        #     'Survived': pclass_df2,
        #     'SurvivalRate': survival_rate_df
        # }).reset_index()

        st.write('Here\'s the data together also containing the survival rates calculated.')
        st.dataframe(survival_rate_df.head())

        st.write('From this information we can conclude that first class passengers were 38% more likely to survive than the third class passengers.')

        with st.expander("How did we get these values?"):
            code = '''# We got the count of passengers for each class.
class_count_df = pclass_df.groupby('Pclass').agg(Passenger_Count = ('Survived', 'count'))

# We summed the number of passengers who survived by pclass.
pclass_df1 = pclass_df[['Pclass', 'Survived']]
pclass_df2 = pclass_df1.groupby('Pclass').agg(Number_Survived = ('Survived', 'sum'))

# Joined the dataframes together.
survival_rate_df = pd.merge(left = class_count_df, right = pclass_df2, on = 'Pclass', how = 'left')

# Created a calculated column for the survival rate.
survival_rate_df['Survival_Rate'] = survival_rate_df['Number_Survived'] / survival_rate_df['Passenger_Count']
# And displayed the data.
st.dataframe(survival_rate_df.head())

        '''
            st.code(code, language="python")

    def pre_processing(titanic_df:pd.DataFrame):
        divider_line()
        titanic_df1 = titanic_df.copy()

        st.write('Another facet of data science is machine learning. I will explain what this is later. For now, here are some important details regarding the preparation of data before the machine learning happens.')

        st.write('Machine learning models rely heavily on mathematical algorithms. So, we need to ensure that we are working with only numerical data, and make sure there are no null (or empty) values in our dataset.')
        st.write('For that reason we will encode the gender column to values of 1 and 0. 1 representing a female passenger, and 0 for male.')

        # Encode gender to female: 1, male: 0
        titanic_df1['Gender'] = titanic_df1['Gender'].map({'male': 0, 'female': 1})

        st.write('We will also fill the blank age values with the median age.')
        # This is a data cleaning technique as don't want to have null values for machine learning.
        # Fill missing age with median
        titanic_df1['Age'] = titanic_df1['Age'].fillna(titanic_df1['Age'].median())

        with st.expander("How did we do this?"):
            code = '''# We encoded the gender column to female: 1, male: 0 like this:
titanic_df1['Gender'] = titanic_df1['Gender'].map({'male': 0, 'female': 1})

# Then we filled in the blank age values with the median age.
titanic_df1['Age'] = titanic_df1['Age'].fillna(titanic_df1['Age'].median())
        '''
            st.code(code, language="python")

        return titanic_df1

    def machine_learning(titanic_df1:pd.DataFrame):
        divider_line()

        st.write('The basic idea of machine learning is that you give the computer data, you let it practice with the data- allowing it to learn and identify patterns. Then have the computer make predictions or decisions without being told the answer.')
        st.write('We select data to be used by the computer to predict whether a passenger will survive the Titanic or not. The features we\'re using are: \'Pclass\', \'Gender\', \'Age\', \'SibSp\', \'Parch\', and \'Fare\'.')
        # Select features and target (not using cabin or embarked which had null values)
        features = ['Pclass', 'Gender', 'Age', 'SibSp', 'Parch', 'Fare']
        X = titanic_df1[features]
        y = titanic_df1['Survived']

        # Split into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        with st.expander("Here is the code for the machine learning process."):
            code = '''# Selected features and target (not using cabin or embarked which had null values).
features = ['Pclass', 'Gender', 'Age', 'SibSp', 'Parch', 'Fare']
X = titanic_df1[features]
y = titanic_df1['Survived']

# Split into training and validation sets.
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model.
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
        '''
            st.code(code, language="python")

        st.write('After the computer is trained (it has learned and practiced), we can use it to predict whether passengers will survive the Titanic on its own (without the answers).')

        # Predict and evaluate
        y_pred = model.predict(X_val)
        accuracy = round(accuracy_score(y_val, y_pred) * 100, 2)

        # st.write('Here is the level of accuracy that our model got when we ran through some data that didn\'t have the answers of whether they had survived or not. We compared the prediceted results versus the actual survival result column of data.')
        st.write(f'Here is the accuracy of the machine learning model: {accuracy}%.')
        st.write('That\'s pretty good! 81% of the time the computer predicted correctly whether a passenger survived or not.')

        coefficients = pd.DataFrame({
            'Feature': features,
            'Coefficient': model.coef_[0]
        })

        st.write('Shown below are coefficients. Coefficients are numbers that show how important each column of data is to the computer\'s prediction.')
        st.write('A positive number shows that a column was more likely to contribute to survival, a negative number is less likely to contribute to survival. The larger the number (in magnitude- not positive or negative), the more it contributed.') 
        st.dataframe(coefficients)
        st.write('Gender has a high positive coefficient meaning a passenger is more likely to survive based on their gender- female in this case.')
        st.write('Class is negative, based on a passengers class (third class) they are less likely to survive.')
        st.write('We saw this before when we looked at the class data we saw that the first class passengers survived more than third class passengers. But what about gender? What about the women surviving more than the men? Why might that be? Well in this event, there was a woman and children first policy. Lifeboat access was prioritized for women and children. First class and second class women passengers would also have been closer to the lifeboats than the third class passengers. These factors contributed to the Titanic passengers survivability.')

        with st.expander("Here is the code for the computers accuracy and coefficients."):
            code = '''# Predict and evaluate.
y_pred = model.predict(X_val)
accuracy = round(accuracy_score(y_val, y_pred) * 100, 2)

st.write(f'The accuracy of the model is: {accuracy}%.')

coefficients = pd.DataFrame({
    'Feature': features,
    'Coefficient': model.coef_[0]
})
st.dataframe(coefficients)    
        '''
            st.code(code, language="python")


topic = st.selectbox(
    "Pick a Topic",
    ("Select a topic", "Level 1 - 📅 Birthdays", "Level 2 - 🍿 Movies", "Level 3 - ⚓ The Titanic"),
    index=0
)
# Testing, adding levels to each section.

# Main
if topic == 'Level 1 - 📅 Birthdays':
    birthday_df = Birthday.load_birthday_data()

    Birthday.calculate_births_by_year()

    # Define the months name dictionary
    month_names_dict = {
    1:'January',
    2:'February',
    3:'March',
    4:'April',
    5:'May',
    6:'June',
    7:'July',
    8:'August',
    9:'September',
    10:'October',
    11:'November',
    12:'December',
    }

    days_df1 = Birthday.display_users_birthday_commonality(month_names_dict)

    Birthday.least_common_birthdays(days_df1, month_names_dict)

    # ----------------------------------------------------------------------------------------
    # Look at just months like how I did one with just years.
    # st.write('Look at just months like how I did one with just years?')

    # # Get the total number of births per month
    # months_df = birthday_df.groupby("month").sum().reset_index()
    # # Filter the dataframe
    # months_df1 = months_df[["month", "births"]]

    # births_month_chart = alt.Chart(months_df1).mark_bar().encode(
    #     x = alt.X('month', title = 'Month'),
    #     y = alt.Y('births', title = 'Number of Births')
    # )

    # st.altair_chart(altair_chart = births_month_chart)

    # # Can divide them all by 15 to get the avg number of births for that month over the 15 years.
    # months_avg_df = months_df1.copy()
    # months_avg_df['births'] = (months_avg_df['births']/15)

    # births_month_avg_chart = alt.Chart(months_avg_df).mark_bar().encode(
    #     x = alt.X('month', title = 'Month'),
    #     y = alt.Y('births', title = 'Number of Births')
    # )

    # st.altair_chart(altair_chart = births_month_avg_chart)

        # What we've learned
    divider_line()
    st.write('By going through this birthday data we\'ve seen how data scientists use Python code to study data and gain valuable insights. We\'ve seen the usefulness of aggregating, visualizing, sorting, filtering, and observing.')

    if st.button('Finished? Click Here.'):
        st.success("Nice job exploring data! 🎉 Want to try another path? Just pick another topic at the top.")
        st.balloons()

        # Can I have it appear down here for the to choose the next one?



elif topic == 'Level 2 - 🍿 Movies':
    # The original kaggle movie dataset is in here: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset
    # I am working with the movies_metadata.csv
    recent_movies_df1 = Movie.load_movie_data()

    Movie.movie_vote_averages(recent_movies_df1)

    bom_df2 = Movie.most_profitable_movies(recent_movies_df1)

    Movie.stats_by_genre(bom_df2)

    # What we've learned
    divider_line()
    st.write('By going through this movie data we\'ve seen how data scientists use Python code to massage the data to something useable. We\'ve seen the usefulness of sorting, filtering, feature engineering, visualizing, and regular expressions.')

    if st.button('Finished? Click Here.'):
        st.success("Nice job exploring data! 🎊 Want to try another path? Just pick another topic at the top.")
        st.balloons()

    # Could show images of movies in some places too

elif topic == 'Level 3 - ⚓ The Titanic':
    titanic_df = Titanic.load_titanic_data()

    Titanic.pie_charts(titanic_df)

    Titanic.class_data(titanic_df)

    titanic_df1 = Titanic.pre_processing(titanic_df)

    Titanic.machine_learning(titanic_df1)

     # What we've learned
    divider_line()
    st.write('By going through this Titanic data we\'ve seen how data scientists use Python code to look at a datasets info, visualize data in pie charts, and use machine learning to make predictions.')

    if st.button('Finished? Click Here.'):
        st.success("Nice job exploring data! 🙌 Want to try another path? Just pick another topic at the top.")
        st.snow()







































































