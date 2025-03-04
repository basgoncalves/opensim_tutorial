import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import SpanSelector
import io

def load_and_trim_csv(csv_data, time_column, value_column):
    """
    Loads a CSV, plots it, and allows trimming based on selected time points.

    Args:
        csv_data (str or io.StringIO): Path to CSV file or CSV data as string.
        time_column (str): Name of the time column.
        value_column (str): Name of the value column to plot.

    Returns:
        pandas.DataFrame: Trimmed DataFrame.
    """
    try:
        df = pd.read_csv(csv_data, parse_dates=[time_column])
    except FileNotFoundError:
        print(f"Error: CSV file not found.")
        return None
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

    if time_column not in df.columns or value_column not in df.columns:
        print(f"Error: Time column '{time_column}' or value column '{value_column}' not found.")
        return None

    fig, ax = plt.subplots()
    ax.plot(df[time_column], df[value_column])

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))  # Adjust date format as needed
    fig.autofmt_xdate()

    selected_times = []

    def onselect(xmin, xmax):
        selected_times.clear()
        selected_times.append(mdates.num2date(xmin))
        selected_times.append(mdates.num2date(xmax))
        print(f"Selected time range: {selected_times[0]} to {selected_times[1]}")

    span = SpanSelector(
        ax, onselect, 'horizontal', useblit=True,
        props=dict(alpha=0.5, facecolor='red')
    )

    plt.show()

    if len(selected_times) == 2:
        start_time = min(selected_times)
        end_time = max(selected_times)
        trimmed_df = df[(df[time_column] >= start_time) & (df[time_column] <= end_time)].copy() # use copy to prevent slice warnings
        return trimmed_df
    else:
        print("No time range selected, returning original DataFrame.")
        return df

# Example Usage (from a file):
# trimmed_df = load_and_trim_csv("your_data.csv", "timestamp", "value")

# Example usage (from a string, useful for testing):

csv_string = """timestamp,value
2023-10-26 10:00:00,10
2023-10-26 10:15:00,12
2023-10-26 10:30:00,15
2023-10-26 10:45:00,18
2023-10-26 11:00:00,20
2023-10-26 11:15:00,22
2023-10-26 11:30:00,25
2023-10-26 11:45:00,28
2023-10-26 12:00:00,30
"""

trimmed_df = load_and_trim_csv(io.StringIO(csv_string), "timestamp", "value")

if trimmed_df is not None:
    print("\nTrimmed DataFrame:")
    print(trimmed_df)