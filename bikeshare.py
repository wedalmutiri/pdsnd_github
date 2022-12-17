import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_input(input_str,input_type):
    """
    Check the validity of the user's input
     Args:
        (str) input_str - the input from the user
        (int) input_type - is the type of the input: 1 = city, 2 = month, 3 = day
    Returns:
        input_read - the valid input from the user
    """
    while True:
        input_read=input(input_str).lower()
        try:
            if input_read in ['chicago','new york city','washington'] and input_type == 1:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june','all'] and input_type == 2:
                break
            elif input_read in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print("Sorry, your input should be: chicago, new york city, or washington\n")
                if input_type == 2:
                    print("Sorry, your input should be: all, january, february, march, april, may, or june\n")
                if input_type == 3:
                    print("Sorry, your input should be: all, sunday, monday, tuesday, wednesday, thursday, friday, or saturday?\n")
        except ValueError:
            print("Sorry, your input is wrong\n")
    return input_read


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
   
# TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    
    city = check_input("Would you like to see data for Chicago, New York city, or Washington?\n", 1)
    
    # TO DO: get user input for month (all, january, february, ... , june)

    month = check_input("Which month - all, january, february, march, april, may, or june?\n(Hint: write all if you don't want to filter based on month)\n", 2)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = check_input("Which day - all, monday, tuesday, wednesday, thursday, friday, saturday, or sunday?\n",3)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is :", most_common_month)

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("The most common day of week is :", most_common_day_of_week)

    # display the most common start hour
    
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is :", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station :", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station :", most_common_end_station)

    # display most frequent combination of start station and end station trip
    df['Start & End'] = df['Start Station'].str.cat(df['End Station'], sep=' --> ')
        
    print('\nMost frequent combination of start station and end station trip is: ',df['Start & End'].mode()[0])

    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}".format(most_common_start_end_station[0], most_common_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel)

    # display mean travel time
    max_travel = df['Trip Duration'].max()
    print("Max travel time :", max_travel)

    print("Travel time for each user type:\n")
    # display the total trip duration for each user type
    group_by_user_trip = df.groupby(['User Type']).sum()['Trip Duration']
    for index, user_trip in enumerate(group_by_user_trip):
        print("  {}: {}".format(group_by_user_trip.index[index], user_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n")
    user_counts = df['User Type'].value_counts()
    # iteratively print out the total numbers of user types 
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))
    

    if 'Gender' in df.columns:
        user_stats_gender(df)

    if 'Birth Year' in df.columns:
        user_stats_birth(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats_gender(df):
    """Displays statistics of analysis based on the gender of bikeshare users."""

    # Display counts of gender
    print("Counts of gender:\n")
    gender_counts = df['Gender'].value_counts()
    # iteratively print out the total numbers of genders 
    for index,gender_count   in enumerate(gender_counts):
        print("  {}: {}".format(gender_counts.index[index], gender_count))

def user_stats_birth(df):
    """Displays statistics of analysis based on the birth years of bikeshare users."""

    # Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']
    # the most common birth year
    most_common_year = birth_year.value_counts().idxmax()
    print("The most common birth year:", most_common_year)
    # the most recent birth year
    most_recent = birth_year.max()
    print("The most recent birth year:", most_recent)
    # the most earliest birth year
    earliest_year = birth_year.min()
    print("The most earliest birth year:", earliest_year)

def table_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating Dataset Stats...\n')
    

    number_of_missing_values = np.count_nonzero(df.isnull())
    print("The number of missing values in the {} dataset : {}".format(city, number_of_missing_values))

    
    number_of_nonzero = np.count_nonzero(df['User Type'].isnull())
    print("The number of missing values in the \'User Type\' column: {}".format(number_of_missing_values))

    
def display_raw_data(df):
    """Displays 5 rwos of raw data at a time, on user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nWould you like to view next five row of raw data? Enter yes or no.\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            view_raw_data = input('\nWould you like to view first five row of raw data? Enter yes or no.\n')
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
       
if __name__ == "__main__":
    main()
