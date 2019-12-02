import time
import pandas as pd
import numpy as np
import calendar
import math
import statistics

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
city=''
month=''
day=''

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!\nType exit at anytime to stop')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nEnter name of the city to analyze from the list: chicago, new york city, washington\n')
    while city.lower() not in ['chicago', 'new york city', 'washington']:
        if city.lower() == 'exit':
            print ('\nRecieved exit command! Good Bye!!')
            break
        else:
            city = input('\nInvalid City "{}"!!! Enter name of the city to analyze from the list: chicago, new york city, washington\n'.format(city))

    # TO DO: get user input for month (all, january, february, ... , june)
    if city.lower() != 'exit':
        month = input('\nInput the month to anlyze from the list: all (for all the months), january,february, ... , june\n')
        while month.lower() not in ['all', 'january', 'february','march','april','may','june']:
            if month.lower() == 'exit':
                print ('\nRecieved exit command! Good Bye!!')
                break
            else:
                month = input('\nInvalid Month "{}"!!! input the month to anlyze from the list: all (for all the months), january,february, ... , june\n'.format(month))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if city.lower() != 'exit' and month.lower() != 'exit':
        day = input('\nInput the day of week to analyze from the list: all (for whole week), monday, tuesday,..sunday\n')
        while day.lower() not in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
            if day.lower() == 'exit':
                print ('\nRecieved exit command! Good Bye!!')
                break
            else:
                day = input('\nInvalid day "{}"!!! input the day of week to analyze from the list: all (for whole week), monday, tuesday,..sunday\n'.format(day))

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    """This function displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    mon = calendar.month_name[(df['Start Time'].dt.month).mode()[0]]
    print('\nMost common Month: {}'.format(mon))

    # TO DO: display the most common day of week
    print('\nMost common day of the week: {}'.format(df['Start Time'].dt.weekday_name.mode()[0]))

    # TO DO: display the most common start hour
    print('\nMost common start hour: {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """This function displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('\nMost commonly used start station: {}'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('\nMost commonly used end station: {}'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print('\nMost frequent used start & end station trip is: {}'.format((df['Start Station']+df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    print('\nTotal travel time: {}'.format(total_duration))

    # TO DO: display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('\nMean travel time: {}'.format(mean_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_count = df['User Type'].value_counts()
    print('\nCount of user Type:\n{}'.format(user_count))

    # TO DO: Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nCount of Gender:\n{}'.format(gender_count))
    except Exception as e:
        print('\nException: Unable to generate gender counts as Gender details not available')
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_yr = int(df['Birth Year'].min())
        most_recent_birth_yr = int(df['Birth Year'].max())
        most_common_birth_yr = int(df['Birth Year'].mode()[0])
        print('\nEarliest Birth Year:{}\nMost recent Birth Year: {}\nMost Common Birth Year: {}'.format(earliest_birth_yr,most_recent_birth_yr,most_common_birth_yr))
    except Exception as f:
        print('\nException: Unable to generate birth stats as birth details not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data upon user requst."""
    start_time = time.time()
    lcount = 0
    while True:
        if lcount == 0:
            display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        else:
            display_data = input('\nWould you like to see 5 more lines of raw data? Enter yes or no.\n')

        if display_data.lower() != 'yes':
            break
        else:
            print(df.iloc[lcount:lcount+5])
            lcount += 5

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        if(city != 'exit' and month != 'exit' and day != 'exit' ):
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
