import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = ""
    while city not in CITY_DATA.keys():
        city = input("Enter the name of one city - Chicago, New York City, or Washington: ").lower()
    if city in CITY_DATA.keys():
        print("Thank you. We'll analyze the data for this city.")
    
    month = ""
    while month not in MONTH_DATA:
        month = input("Enter the name of one month between January and June, or \"all\": ").lower()
    if month in MONTH_DATA:
        print("Great. Moving on...")
    
    day = ""
    while day not in DAY_DATA:
        day = input("Enter a day of the week, or \"all\": ").lower()
    if day in DAY_DATA:
        print("Okay. Thank you.")
    
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
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != "all":
        month = MONTH_DATA.index(month) + 1
        df = df[df.month == month]
    else:
        df = df
        
    if day != "all":
        df = df[df.day_of_week == day.title()]
    else:
        df = df

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("The most common month is {}".format(MONTH_DATA[df.month.mode()[0] - 1].title()))
    print("The most common day of the week is {}".format(df.day_of_week.mode()[0]))
    print("The most common starting hour is {}".format(df['Start Time'].dt.hour.mode().iloc[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("The most commonly used start station is at {}".format(df['Start Station'].mode()[0]))

    print("The most commonly used end station is at {}".format(df['End Station'].mode()[0]))

    print("The most common trip goes between \n{}".format(df[['Start Station', 'End Station']].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Total Travel Time'] = df['Start Time'] - df['End Time']

    print("The mean travel time is {}".format(df['Total Travel Time'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The user type counts are: \n{}".format(df['User Type'].value_counts()))

    if "Gender" in df.columns:
        print("The gender counts are: \n{}".format(df['Gender'].value_counts()))
    else:
        print("Gender is not a column in this dataframe. Moving on...")

    if "Birth Year" in df.columns:
        print("The earliest year of birth is {}".format(int(df['Birth Year'].min())))
        print("The most recent year of birth is {}".format(int(df['Birth Year'].max())))
        print("The most common year of birth is {}".format(int(df['Birth Year'].mode()[0])))
    else:
        print("Birth year is not a column in this dataframe. Moving on...")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
