import time
import pandas as pd
import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Asks the user to specify a city and how they want to filter the data.

    Returns:
        city (str): The city to analyze.
        month (str): The month to filter by, or 'all'.
        day (str): The day of the week to filter by, or 'all'.
    """
    print("Hello! Let's explore some US bikeshare data!")

    # Get city input
    city = input(
        "Would you like to see data for Chicago, New York City, or Washington? "
    ).lower()
    while city not in ["chicago", "new york city", "washington"]:
        print("That’s not a valid city.")
        city = input("Please enter Chicago, New York City, or Washington: ").lower()

    # Ask how to filter the data
    filter_type = input(
        "Would you like to filter the data by month, day, both, or not at all? Type 'none' for no filter: "
    ).lower()
    while filter_type not in ["month", "day", "both", "none"]:
        print("That’s not a valid filter type.")
        filter_type = input("Please enter 'month', 'day', 'both', or 'none': ").lower()

    # Default values
    month = "all"
    day = "all"

    # Get month if needed
    if filter_type == "month" or filter_type == "both":
        month = input(
            "Which month? (January, February, March, April, May, or June): "
        ).lower()
        while month not in ["january", "february", "march", "april", "may", "june"]:
            print("Invalid month.")
            month = input("Please enter a month from January to June: ").lower()

    # Get day if needed
    if filter_type == "day" or filter_type == "both":
        day = input(
            "Which day? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): "
        ).lower()
        while day not in [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]:
            print("Invalid day.")
            day = input("Please enter a valid day of the week: ").lower()

    print("-" * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters it by month and day if requested.

    Args:
        city (str): City name
        month (str): Month name or 'all'
        day (str): Day name or 'all'

    Returns:
        df (DataFrame): The filtered DataFrame
    """
    # Load the CSV file for the selected city
    filename = city.replace(" ", "_") + ".csv"
    df = pd.read_csv(filename)

    # Convert Start Time to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Create new columns for month and day of week
    df["month"] = df["Start Time"].dt.month_name().str.lower()
    df["day_of_week"] = df["Start Time"].dt.day_name().str.lower()

    # Filter by month if needed
    if month != "all":
        df = df[df["month"] == month]

    # Filter by day if needed
    if day != "all":
        df = df[df["day_of_week"] == day]

    return df


# if __name__ == "__main__":
#     city, month, day = get_filters()
#     df = load_data(city, month, day)
#     print("\nHere’s what your filtered data looks like:")
#     print(df.head())
#     print(f"\nTotal rows after filtering: {len(df)}")


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """
    print("\nCalculating The Most Frequent Times of Travel...\n")

    # Most common month
    common_month = df["month"].mode()[0]
    print(f"Most common month: {common_month.title()}")

    # Most common day of week
    common_day = df["day_of_week"].mode()[0]
    print(f"Most common day of the week: {common_day.title()}")

    # Most common start hour
    df["hour"] = df["Start Time"].dt.hour
    common_hour = df["hour"].mode()[0]
    print(f"Most common start hour: {common_hour}:00")


# if __name__ == "__main__":
#     city, month, day = get_filters()
#     df = load_data(city, month, day)
#     time_stats(df)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip combinations.
    """
    print("\nCalculating The Most Popular Stations and Trip...\n")

    # Most common start station
    start_station = df["Start Station"].mode()[0]
    print(f"Most common start station: {start_station}")

    # Most common end station
    end_station = df["End Station"].mode()[0]
    print(f"Most common end station: {end_station}")

    # Most common trip (combination of start and end)
    df["trip"] = df["Start Station"] + " to " + df["End Station"]
    most_common_trip = df["trip"].mode()[0]
    print(f"Most common trip: {most_common_trip}")


# if __name__ == "__main__":
#     city, month, day = get_filters()
#     df = load_data(city, month, day)
#     time_stats(df)
#     station_stats(df)


def trip_duration_stats(df):
    """
    Displays statistics on total and average trip duration.
    """
    print("\nCalculating Trip Duration...\n")

    # Total travel time
    total_time = df["Trip Duration"].sum()
    print(f"Total travel time: {total_time:,} seconds ({total_time / 3600:.2f} hours)")

    # Average travel time
    average_time = df["Trip Duration"].mean()
    print(
        f"Average travel time: {average_time:.2f} seconds ({average_time / 60:.2f} minutes)"
    )


# if __name__ == "__main__":
#     city, month, day = get_filters()
#     df = load_data(city, month, day)
#     time_stats(df)
#     station_stats(df)
#     trip_duration_stats(df)


def user_stats(df):
    """
    Displays statistics on user types and, if available, gender and birth year.
    """
    print("\nCalculating User Stats...\n")

    # Count user types
    print("User Types:")
    print(df["User Type"].value_counts())

    # Gender counts (only if column exists)
    if "Gender" in df.columns:
        print("\nGender Counts:")
        print(df["Gender"].value_counts())
    else:
        print("\nGender data not available.")

    # Birth year stats (only if column exists)
    if "Birth Year" in df.columns:
        print("\nBirth Year Info:")
        print(f"Earliest birth year: {int(df['Birth Year'].min())}")
        print(f"Most recent birth year: {int(df['Birth Year'].max())}")
        print(f"Most common birth year: {int(df['Birth Year'].mode()[0])}")
    else:
        print("\nBirth year data not available.")


# if __name__ == "__main__":
#     city, month, day = get_filters()
#     df = load_data(city, month, day)
#     time_stats(df)
#     station_stats(df)
#     trip_duration_stats(df)
#     user_stats(df)


def display_raw_data(df):
    """
    Asks user if they want to see 5 rows of raw data, displays them if yes.
    """
    show_data = input(
        "\nWould you like to see 5 lines of raw data? (yes or no): "
    ).lower()
    start = 0

    while show_data == "yes":
        print(df.iloc[start : start + 5])
        start += 5

        if start >= len(df):
            print("You've reached the end of the data.")
            break

        show_data = input("Would you like to see 5 more rows? (yes or no): ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)  # ✅ This was missing

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            print("Thank you for exploring US bikeshare data. Goodbye!")
            break


if __name__ == "__main__":
    main()
