import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'dc': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    while True:
        city = input("\nWould you like to see data for Chicago, NYC, or DC? ").lower()
        if city not in ('chicago', 'nyc', 'dc'):
            print("Sorry, I didn't understand that. ")
        else:
            print("Looks like you want to hear about {}!  If this is not true, restart the program now! ".format(city.upper()))
            break

    # get user input for month (january, february..., june), day (monday, tuesday, ... sunday), both, or none at all
    while True:
        filter = input("\nWould you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter. ").lower()
        if filter not in ('month', 'day', 'both', 'none'):
            print("Sorry, I didn't understand that. ")
        else:
            if filter == 'month':
                day = 'all'
                # get user input for month
                month = get_month()
            elif filter == 'day':
                month = 'all'
                # get user input for day of week
                day = get_day()
            elif filter == 'both':
                # get user input for month and day of week
                month = get_month()
                day = get_day()
            else:
                # do not get user input for month or day of week
                month = 'all'
                day = 'all'
                print("We will not filter by month or day. ")
            break

    print('-'*40)
    return city, month, day


def get_month():
    """ Asks user to specify a month to analyze """

    while True:
        month = input("\nWhich month? January, February, March, April, May, or June? ").lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
            print("Sorry, I didn't understand that. ")
        else:
            print("We will make sure to filter by the month of {}! ".format(month.upper()))
            break
    return month


def get_day():
    """ Asks user to specify a day to analyze """

    while True:
        day = input("\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ").lower()
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print("Sorry, I didn't understand that. ")
        else:
            print("We will make sure to filter by the day of {}! ".format(day.upper()))
            break
    return day


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

    # load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new DataFrame
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month, if applicable based on user input
    if month == 'all':
        print('\nWhat is the most popular month for traveling?')
        popular_month = df['month'].mode()[0]
        print(popular_month)

    # display the most common day of week, if applicable based on user input
    if day == 'all':
        print('\nWhat is the most popular day for traveling?')
        popular_day = df['day_of_week'].mode()[0]
        print(popular_day)

    # display the most common start hour
    print('\nWhat is the most popular hour of the day to start your travels?')
    popular_hour = df['hour'].mode()[0]
    print(popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start and end stations
    print('\nBelow are the most popular start and end stations, respectively?')
    popular_start = df['Start Station'].mode()[0]
    popular_end = df['End Station'].mode()[0]
    print(np.array([popular_start, popular_end]))

    # display most frequent combination of start station and end station trip
    print('\nWhat was the most popular trip from start to end?')
    df['trip'] = df['Start Station'].map(str) + ' TO ' + df['End Station'].map(str)
    popular_trip = df['trip'].value_counts().idxmax()
    print(popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    print('\nWhat was the total traveling time? ')
    total_time = df['Trip Duration'].sum()
    print(pd.to_timedelta(total_time, unit='s'))

    # display mean travel time
    print('\nWhat was the average time spent on each trip? ')
    avg_time = df['Trip Duration'].mean()
    print(pd.to_timedelta(avg_time, unit='s'))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    print("\nWhat is the breakdown of users? ")
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    print("\nWhat is the breakdown of gender? ")
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender)
    else:
        print("No gender data to share. ")

    # Display earliest, most recent, and most common year of birth
    print("\nWhat is the oldest, youngest, and most popular year of birth, respectively? ")
    if 'Birth Year' in df.columns:
        oldest_birthyear = df['Birth Year'].min()
        print("Oldest = {}".format(int(oldest_birthyear)))

        youngest_birthyear = df['Birth Year'].max()
        print("Youngest = {}".format(int(youngest_birthyear)))

        common_birthyear = df['Birth Year'].value_counts().idxmax()
        print("Most Common = {}".format(int(common_birthyear)))
    else:
        print("No birth year data to share. ")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def get_raw_data(df):
    """Display raw data upon request by the user."""

    while True:
        raw_data = input("\nWould you like to view individual trip data?  Type 'yes' or 'no'. ").lower()
        if raw_data not in ('yes', 'no'):
            print("Sorry, I don't understand.")
        else:
            i = 0
            while raw_data == 'yes':
                print(df.iloc[i:i+5, 0:-4])
                i += 5
                while True:
                    raw_data = input("\nWould you like to view more data?  Type 'yes' or 'no'. ").lower()
                    if raw_data not in ('yes', 'no'):
                        print("Sorry, I don't understand.")
                    else:
                        break
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        get_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
