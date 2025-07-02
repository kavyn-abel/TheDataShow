import streamlit as st
import pandas as pd
import altair as alt

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
        st.write('Here\'s the url for the data we\'ll be using. Data is information. This data includes the number of births for each day of the year in the U.S. for the years 2000-2014. Click on the link below to see the raw data.')
        st.write('https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_2000-2014_SSA.csv')

        st.write('Let\'s bring in that data with Python code.')

        url = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_2000-2014_SSA.csv'
        birthday_df = pd.read_csv(url)

        st.write("Here\'s how that data looks when we've brought it into a pandas dataframe with Python code:")
        # A dataframe is like a table in excel, with rows and columns.
        # st.table(data = birthday_df.head())
        # Trying st.dataframe
        st.dataframe(data = birthday_df.head())

        # Expander for how we did that
        with st.expander("How did we bring that data into python?"):
            code = ''' # We used this python code to read in the csv file.
url = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_2000-2014_SSA.csv'
birthday_df = pd.read_csv(url)

# Then displayed the first 5 rows of the dataframe in the app.
st.dataframe(data = birthday_df.head())
    '''
            st.code(code, language="python")

        return birthday_df


    def calculate_births_by_year():
        divider_line()

        st.write('With this data we can find out things such as which year had the most births.')
        st.write('We can do this by summing the number of births within each year. We can look at the results in the chart below:')

        # Get the number of births per year
        years_df = birthday_df.groupby("year").sum().reset_index()
        # Filter the dataframe
        years_df1 = years_df[["year", "births"]]

        # Here's alook at the data
        # st.table(data = years_df1)

        births_year_chart = (alt.Chart(years_df1).mark_bar().encode(
            x = alt.X('year:Q', title = 'Year'),
            y = alt.Y('births', title = 'Total Births', scale=alt.Scale(domain=[3500000, 4500000]))
        ).properties(
            width = 900,
            height = 800
        )
                            )

        st.altair_chart(births_year_chart, theme = None)

        st.write('Here we can see, according to our data, that the most births were in the year 2007.')

        with st.expander("How did we get there?"):
            code = ''' # We aggregated the data to get the number of births per year.
years_df = birthday_df.groupby("year").sum().reset_index()

# We created the chart with the altair library.
births_year_chart = alt.Chart(years_df1).mark_bar().encode(
    x = alt.X('year', title = 'Year'),
    y = alt.Y('births', title = 'Total Births', scale=alt.Scale(domain=[3500000, 4500000]))
)

# We presented the chart in the app.
st.altair_chart(altair_chart = births_year_chart)
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
        input_date = st.date_input('What is your birthday?')

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
        st.dataframe(top_days_df2.head(10))

        return days_df1


    def least_common_birthdays(days_df:pd.DataFrame, month_dict:dict):
        divider_line()
        st.write('Next, let\'s take a look at the days with the lowest number of births. Do you see anything interesting?')
        # Lowest number of birth days
        low_days_df = days_df1.sort_values(by = 'births', ascending = True)

        # Map to the actual month names before displaying
        low_days_df1 = low_days_df.copy()
        low_days_df1['month'] = low_days_df1['month'].replace(month_dict)

        st.dataframe(low_days_df1.head(10))

        st.text_area('Write what you observe about this data:')

        # How we got there box
        with st.expander("How did we get to this lowest number of births view of the data?"):
            code = ''' # We sorted the data starting from the lowest number of births, going up.
low_days_df = days_df1.sort_values(by = 'births', ascending = True)

# We mapped the months as numbers to their actual names with an earlier 
# defined dictionary called month_dict.
low_days_df1 = low_days_df.copy()
low_days_df1['month'] = low_days_df1['month'].replace(month_dict)

# Displayed the data back to the user in the app.
st.dataframe(low_days_df1.head(10))
        '''
            st.code(code, language="python")


class Movie:
    def load_movie_data():
        st.write('Let\'s talk movies!')
        st.write('In this section we are looking at data from movies released since 2022 until August 2023.')

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
        recent_movies_df1 = pd.read_csv('movies_since_2022_select_columns.csv')

        # Filter the columns to what I want to work with
        # recent_movies_df1 = recent_movies_df[['title', 'vote_average', 'vote_count', 'release_date', 'revenue', 
        #                             'runtime', 'budget', 'genres']]
        
        st.write('Here\'s how that data looks brought into a dataframe with Python code:')
        # st.table(recent_movies_df1.head())
        st.dataframe(recent_movies_df1.head())

        with st.expander("How did we bring that data into Python?"):
            code = ''' # We read in the data into a dataframe from a csv file.
recent_movies_df = pd.read_csv('movies_since_2022.csv')

# Next, we displayed the first 5 rows of data to you in the app.
st.dataframe(recent_movies_df1.head())
        '''
            st.code(code, language="python")


        return recent_movies_df1
    
        

    def movie_vote_averages(recent_movies_df1:pd.DataFrame):
        divider_line()
        st.write('Now, let\'s sort the data by the vote average and see what movies, on average, get the highest vote rating out of 10.')
        highest_vote_avg = recent_movies_df1.sort_values('vote_average', ascending = False)
        st.dataframe(highest_vote_avg.head())
        st.write('Notice anything? These movies have a 10 point average, but there is only 1 vote on each of these movies.')

        st.text('')
        st.write('So, let\'s also sort by the vote count as well and see how that looks.')
        highest_vote_avg_and_count = recent_movies_df1.sort_values(['vote_average', 'vote_count'], ascending = False)
        st.dataframe(highest_vote_avg_and_count.head())
        st.write('Ok, still very few votes.')

        st.text('')
        st.write('What if we take a look at movies that have at least 500 votes- still sorted by the vote average and vote count.')
        # Now what if we have to look at the data where there has to be at least 500 votes
        highest_vote_avg_and_count1 = highest_vote_avg_and_count[highest_vote_avg_and_count['vote_count'] > 500]
        st.dataframe(highest_vote_avg_and_count1.head())
        st.write('See the difference between this and our first output in this section?')

        
        with st.expander("How did we do this?"):
            code = ''' # We sorted the data by the vote average.
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
        st.write('Let\'s take a look at it:')
        st.dataframe(bom_df.head(1))

        st.text('')
        st.write('We\'ll sort the data now by the Box Office Margin, and look at movies with at least 100 votes.')
        # Where there are at least 100 votes
        bom_df1 = bom_df[bom_df['vote_count'] > 100]

        # And sort by Box Office Margin
        bom_df2 = bom_df1.sort_values('Box Office Margin', ascending = False)
        # st.table(bom_df2.head(10))

        st.write('Here is a chart showing the top 5 movies with that criteria.')

        # Chart for most profitable movies
        bom_movie_data = bom_df2.head(5)
        bom_movie_chart = (alt.Chart(bom_movie_data).mark_bar().encode(
            x = alt.X('title', title = 'Movie Title'),
            y = alt.Y('Box Office Margin', title = 'Box Office Margin ($)') #  , scale=alt.Scale(domain=[8, 9])
        ))

        st.altair_chart(bom_movie_chart, theme = None)

        with st.expander("How did we do this?"):
            code = ''' # We created a new column from ones that we already had (That's called 
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
            code = ''' # We defined a list of genres.
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



topic = st.selectbox(
    "Pick a Topic",
    ("Select a topic", "📅 Birthdays", "🍿 Movies"), # , "🎵 Music", "☀️ Climate"
    index=0
)

# Main
if topic == '📅 Birthdays':
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



elif topic == '🍿 Movies':
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
        st.success("Nice job exploring data! 🎉 Want to try another path? Just pick another topic at the top.")
        st.balloons()

    # Could show images of movies in some places too
