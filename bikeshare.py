import time
import pandas as pd
import numpy as np

# Mapping of city names to corresponding CSV filenames
CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}
VALID_CITIES = ["chicago", "new york city", "washington"]
VALID_MONTHS = ["january", "february", "march", "april", "may", "june"]
VALID_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
VALID_FILTERS = ["month", "day", "both", "none"]


def get_valid_input(prompt, valid_options):
    """Prompt user until a valid input is given."""
    response = input(prompt).lower()
    while response not in valid_options:
        print("Invalid input.")
        response = input(prompt).lower()
    return response


def get_filters():
    """
    Asks the user to specify a city and how they want to filter the data.

    Returns:
        city (str): The city to analyze
        month (str): The month to filter by, or 'all'
        day (str): The day of the week to filter by, or 'all'
    """
    print("Hello! Let's explore some US bikeshare data!")

    # Get valid city
    city = get_valid_input(
        "Would you like to see data for Chicago, New York City, or Washington? ",
        VALID_CITIES,
    )

    # Get valid filter type
    filter_type = get_valid_input(
        "Would you like to filter the data by month, day, both, or not at all? Type 'none' for no filter: ",
        VALID_FILTERS,
    )

    # Defaults
    month = "all"
    day = "all"

    # Get month if required
    if filter_type in ("month", "both"):
        month = get_valid_input(
            "Which month? (January, February, March, April, May, or June): ",
            VALID_MONTHS,
        )

    # Get day if required
    if filter_type in ("day", "both"):
        day = get_valid_input(
            "Which day? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ",
            VALID_DAYS,
        )

    print("-" * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and applies filters by month and day if requested.

    Args:
        city (str): City name
        month (str): Month name or 'all'
        day (str): Day name or 'all'

    Returns:
        df (DataFrame): The filtered DataFrame
    """
    # Load CSV data for the selected city
    filename = city.replace(" ", "_") + ".csv"
    df = pd.read_csv(filename)

    # Convert Start Time to datetime format
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Extract month and day of week from Start Time
    df["month"] = df["Start Time"].dt.month_name().str.lower()
    df["day_of_week"] = df["Start Time"].dt.day_name().str.lower()

    # Apply month filter if specified
    if month != "all":
        df = df[df["month"] == month]

    # Apply day filter if specified
    if day != "all":
        df = df[df["day_of_week"] == day]

    return df


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


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip combinations.
    """
    print("\nCalculating The Most Popular Stations and Trip...\n")

    # Most commonly used start station
    start_station = df["Start Station"].mode()[0]
    print(f"Most common start station: {start_station}")

    # Most commonly used end station
    end_station = df["End Station"].mode()[0]
    print(f"Most common end station: {end_station}")

    # Most frequent combination of start and end station
    df["trip"] = df["Start Station"] + " to " + df["End Station"]
    most_common_trip = df["trip"].mode()[0]
    print(f"Most common trip: {most_common_trip}")


def trip_duration_stats(df):
    """
    Displays statistics on total and average trip duration.
    """
    print("\nCalculating Trip Duration...\n")

    total_time = df["Trip Duration"].sum()
    avg_time = df["Trip Duration"].mean()

    total_hours = total_time / 3600
    avg_minutes = avg_time / 60

    print(f"Total travel time: {total_time:,} seconds ({total_hours:.2f} hours)")
    print(f"Average travel time: {avg_time:.2f} seconds ({avg_minutes:.2f} minutes)")


def user_stats(df):
    """
    Displays statistics on user types, gender, and birth year (if available).
    """
    print("\nCalculating User Stats...\n")

    # Display counts of user types
    print("User Types:")
    print(df["User Type"].value_counts())

    # Display counts of gender, if available
    if "Gender" in df.columns:
        print("\nGender Counts:")
        print(df["Gender"].value_counts())
    else:
        print("\nGender data not available.")

    # Display birth year statistics, if available
    if "Birth Year" in df.columns:
        print("\nBirth Year Info:")
        print(f"Earliest birth year: {int(df['Birth Year'].min())}")
        print(f"Most recent birth year: {int(df['Birth Year'].max())}")
        print(f"Most common birth year: {int(df['Birth Year'].mode()[0])}")
    else:
        print("\nBirth year data not available.")


def display_raw_data(df):
    """
    Asks the user if they want to view raw data and shows 5 rows at a time.
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
    """
    Main function to run the bikeshare interactive script.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            print("Thank you for exploring US bikeshare data. Goodbye!")
            break


if __name__ == "__main__":
    main()
