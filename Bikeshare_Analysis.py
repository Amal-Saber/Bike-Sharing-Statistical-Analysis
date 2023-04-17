import time
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', "all"]
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',"all"]

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
    city = input("enter a city from (chicago, new york city, washington):  ").lower().strip()
    while city not in  CITY_DATA:
        city = input("This city is not listed choose from those(chicago, new york city, washington):  ").lower().strip()
    

    # get user input for month (all, january, february, ... , june)
    month = input("enter month from [january: june] or all for all months: ").lower().strip()
    while month not in months:
        month = input(" invaled input enter a month name for examble 'march': ").lower().strip()
    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("enter a day name or all for all days : ").lower().strip()
    while day not in days:
        day = input("invaled input enter a day name for examble 'monday' : ").lower().strip()

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
    df = pd.DataFrame(df)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.strftime("%B")
    df['day'] = df['Start Time'].dt.strftime("%A")
    df['trip'] = df['Start Station'] +  " >>> "  + df['End Station']

    # filter my month
    if month != 'all':
        df = df[df['month'] == month.title()]

    #filter by day
    if day != "all" :
        df = df[df['day'] == day.title()]
    return df




def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    start_time = time.time()
    
    common_month = None
    common_day = None
    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    
    if month == 'all':
        # display the most common month
        common_month = df['month'].mode()[0]
        
    if day == 'all':    
        # display the most common day of week
        common_day = df['day'].mode()[0]


    print("\nThis took %s seconds." % np.round(time.time() - start_time))
    print('-'*40)
    return common_hour,common_month, common_day




def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    start_time = time.time()


    # display most commonly used start station
    common_ss = df['Start Station'].mode()[0]

    # display most commonly used end station
    common_es = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    common_t = df['trip'].mode()[0]
    

    print("\nThis took %s seconds." % np.round(time.time() - start_time))
    print('-'*40)
    return common_ss, common_es, common_t




def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    start_time = time.time()


    # display total travel time
    total_travel = np.sum(df['Trip Duration'])

    # display average travel time
    avg_travel = np.mean(df['Trip Duration'])

    # display statistics about travel time
    stat_travel = df['Trip Duration'].describe()
    

    print("\nThis took %s seconds." % np.round(time.time() - start_time))
    print('-'*40)
    return total_travel, avg_travel, stat_travel




def user_stats(df):
    """Displays statistics on bikeshare users."""

    start_time = time.time()

    earliest_birth = None
    count_gender = None
    recent_birth = None
    common_birth = None
    stat_birth = None
    # Display counts of user types
    count_user_type = df['User Type'].value_counts()

    try:
        # Display counts of gender
        count_gender = df['Gender'].value_counts()

        # Display earliest, most recent, and most common year of birth
        earliest_birth = int(np.min(df['Birth Year']))
        recent_birth = int(np.max(df['Birth Year']))
        common_birth = int(df['Birth Year'].mode()[0])

        # Display statistics about birth year
        stat_birth = df['Birth Year'].describe()

    except:
        print("")
        
    print("\nThis took %s seconds." % np.round(time.time() - start_time))
    print('-'*40)
    return count_user_type, count_gender, earliest_birth, recent_birth, common_birth, stat_birth




def count_visual(df,col):
    """Create a count plot to know categories iterations in the data."""
    print("\nCreate count plot for {} column".format(col))
    
    #plot results 
    sns.set_style("darkgrid")
    plt.figure(figsize=(7,5))
    ax = sns.countplot(y=col, data= df, order=df[col].value_counts().index[:10],palette='Greens')
    ax.set_facecolor("#D9E4DD")
    plt.show()

    




def hist_visual(df, col):
    """Create a histogram  graph to show the distribution of data."""
    print("\nCreate histogram to know the distribution of {}".format(col))

    plt.figure(figsize=(7,5))
    ax = sns.histplot(data =df ,x= col, color='#56b567')
    ax.set_facecolor("#D9E4DD")
    plt.show()




def pie_visual(df,col):
    """Create a pie chart to present percent of every category in the data."""
    print("\nCreate pie chart to know persent of every category in {} column".format(col))

    data = df[col].value_counts()
    plt.figure(figsize=(3,3))
    plt.pie(data, labels=data.index, autopct='%.0f%%',colors=['#bce4b5', '#56b567'])
    plt.show()





def print_time_stats(df,month, day, common_hour, common_month, common_day ):
    print('\nCalculating The Most Frequent Times of Travel...\n\n')
    start_time = time.time()

    # print the most common start hour
    print("most common start hour is: {}\n".format(common_hour))

    if common_month != None:
        # print the most common month
        print("most common month is: {}\n".format(common_month))

    if common_day != None:    
        # print the most common day of week
        print("most common day is: {}\n".format(common_day))

    print("~"*20) 

    count_visual(df,'hour')
    if month == 'all':
        count_visual(df, 'month')
    if day == 'all' :
        count_visual(df, 'day')

    print("\nThis took %s seconds." % np.round(time.time() - start_time))
    print('-'*40)




def print_station_stats(df, common_ss, common_es, common_t):
    print('\nCalculating The Most Popular Stations and Trip...\n\n')
    start_time = time.time()

    # print most commonly used start station
    print("most commonly used start station is: {}\n".format(common_ss))

    #print most commonly used end station
    print("most commonly used end station is: {}\n".format(common_es))

    #print most frequent combination of start station and end station trip
    print("most frequent trip is: {}\n".format(common_t))

    print("~"*20)

    station_col = ['Start Station', 'End Station', 'trip']
    for col in station_col:
        count_visual(df, col)

    print("\nThis took %s seconds." % np.round(time.time() - start_time))
    print('-'*40)




def print_trip_duration_stats(total_travel, avg_travel, stat_travel):
    print('\nCalculating Trip Duration...\n\n')
    start_time = time.time()


    # print total travel time
    print("total travel time is: {} mins\n".format(total_travel))

    # print average travel time
    print("average travel time is: {} mins\n".format(avg_travel))

    # print statistics about travel time
    print("some statistics about travel time in mins:\n", stat_travel)


    print("\nThis took %s seconds." % np.round(time.time() - start_time))
    print('-'*40)




def print_user_stat(df, city, count_user_type, count_gender, earliest_birth, recent_birth, common_birth, stat_birth):
    print('\nCalculating User Stats...\n\n')
    start_time = time.time()


    # print counts of user types
    print("counts of user types is:\n", count_user_type)
    
    if earliest_birth != None :
        # print counts of gender
        print("\ncounts of gender is:\n", count_gender )

        # print earliest, most recent, and most common year of birth
        print("\nthe oldest person birth day is:  {}\n".format(earliest_birth))
        print("the smallest person birth day is: {}\n".format(recent_birth))
        print("most common year of birth is: {}\n".format(common_birth))

        # print statistics about birth year
        print("some statistics about Birth Year:\n", stat_birth)

    if earliest_birth  == None :
        print("\nNo data for gender and birth day in Washington")  

    print("~"*20)

    pie_visual(df,'User Type')
    if city != "washington" :
        pie_visual(df,'Gender')
        hist_visual(df, 'Birth Year')

    print("\nThis took %s seconds." % np.round(time.time() - start_time))
    print('-'*40)




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        

        common_hour,common_month, common_day = time_stats(df,month, day)
        print_time_stats(df, month, day, common_hour, common_month, common_day )

        
        common_ss, common_es, common_t = station_stats(df)
        print_station_stats(df, common_ss, common_es, common_t)

        total_travel, avg_travel, stat_travel = trip_duration_stats(df)
        print_trip_duration_stats(total_travel, avg_travel, stat_travel)

        count_user_type, count_gender, earliest_birth, recent_birth, common_birth, stat_birth = user_stats(df)
        print_user_stat(df, city, count_user_type, count_gender, earliest_birth, recent_birth, common_birth, stat_birth)
        

        list_valid_input = ["yes", "no"]
        def valid_input(input_val):
            while input_val not in list_valid_input:
                input_val = input("\ninvalid input enter (Yes/No): ").lower().strip()
            return input_val


        rows_count = len(df)
        start = 0
        while start < rows_count:            
            show_data = input("\nshow some data? enter (Yes/No): ").lower().strip()
            show_data = valid_input(show_data)
            end = start + 5

            if show_data == "yes":
                if rows_count - start < 5:
                    pd.set_option('display.max_columns',200)
                    print(df.iloc[start:(rows_count - start)])
                else:
                    pd.set_option('display.max_columns',200)
                    print(df.iloc[start:end]) 
            else :
                break

            start += 5


        restart = input('\nWould you like to restart? Enter yes or no: ')
        restart = valid_input(restart)
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()