import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_options = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

day_options = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'satursday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop
    # to handle invalid inputs
    while True:
        try:
            city = input('\nEnter the name of the city you would like to explore: ').lower()
            if city not in CITY_DATA.keys():
                print('\nWe do not have data for that city, please enter a valid city')
            else:
                break
        except:
            print('\nThat is not a valid input')

    # get user input for month (all, january, february, ... , june)
    while True:
        print('\nYou can choose to see data for the months of January through June')
        try:
            month = input('\nIndicate if you want to see data for all months by entering "all", otherwise enter\
 the month (no abbreviation) you would like to explore: ').lower()
            if month not in month_options:
                print('\nWe cannot accept that input, please enter a valid month')
            else:
                break
        except:
            print('\nThat is not a valid input')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('\nYou can choose to see data filtered by day of week \n')
        try:
            day = input('\nIndicate if you want to see data for all days of the week by entering "all", otherwise\
 enter the day of the week (no abbreviation) you would like to explore: ').lower()
            if day not in day_options:
                print('\nWe cannot accept that input, please enter a valid month')
            else:
                break
        except:
            print('\nThat is not a valid input')

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
    df['day_of_week'] = df['Start Time'].dt.day_name(locale = 'English')

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month']== month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def show_raw(df):
    """
    Asks user whether they would like to see the raw data that has been filtered

    If 'yes' displays raw data 5 rows at a time
    """
    print('\nYou have the choice to review the raw data we have filtered for you')

    # get user input on whether they would like to see the raw data
    possible_ans = ['yes', 'no']
    while True:
        try:
            answer = input('\nWould you like to your raw data? 5 lines will be printed at a time. Answer "yes" or "no": ').lower()
            if answer not in possible_ans:
                print('\nThat is not a valid answer please try again')
            else:
                break
        except:
            print('\nThat is not a valid input')

    n = 5
    i = 0
    while answer == 'yes':
        if i < df.shape[0]:
            print(df.iloc[i:n , :])
        i += n
        n += n
        answer = input('\nWould you like to see 5 more lines of raw data? Answer "yes" or "no": ').lower()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_month = df['month'].mode()[0]
    print('\nThe most common month is: {}'.format(most_month))

    # display the most common day of week
    most_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of week is {}'.format(most_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_hour = df['hour'].mode()[0]
    print('\nThe most common start hour is {}'.format(most_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start = df['Start Station'].mode()[0]
    print('\nThe most common start station is: {}'.format(most_start))

    # display most commonly used end station
    most_end = df['End Station'].mode()[0]
    print('\nThe most common end station is: {}'.format(most_end))

    # display most frequent combination of start station and end station trip
    start_combo, end_combo = df.groupby('Start Station')['End Station'].value_counts().idxmax()
    print('\nThe most requent combination of start station and end station trip is\
 between the {} station and the {} station'.format(start_combo, end_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_traveltime_s = df['Trip Duration'].sum()
    print('\nThe total travel time for all the records is {} seconds'.format(total_traveltime_s))
    format_time = time.strftime('%H:%M:%S', time.gmtime(total_traveltime_s))
    print('Which is a total of {} when converted to hours:minutes:seconds'.format(format_time))

    # display mean travel time
    mean_traveltime_s = df['Trip Duration'].mean()
    print('\nThe mean travel time for is {} seconds'.format(mean_traveltime_s))
    format_meantime = time.strftime('%H:%M:%S', time.gmtime(mean_traveltime_s))
    print('Which is a total of {} when converted to hours:minutes:seconds'.format(format_meantime))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe total count of each user type category in the data: ')
    print(user_types)

    if city == 'washington':
        print('\nWe do not have user gender and birth year statistics for the Washington data')
    else:
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('\nThe total count of male and female users in the data: ')
        print(gender_count)

        # Display earliest, most recent, and most common year of birth
        most_early = int(df['Birth Year'].min())
        print('\nThe earliest birth year in the data is {}'.format(most_early))

        most_recent = int(df['Birth Year'].max())
        print('\nThe most recent birth year in the data is {}'.format(most_recent))

        most_common_year = int(df['Birth Year'].mode()[0])
        print('\nThe most common birth year in the data is {}'.format(most_common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        show_raw(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
