from collections import deque
from shiny import reactive, render
from shiny.express import ui, input
import random
from datetime import datetime
from faicons import icon_svg
import pandas as pd
import plotly.express as px
from shinywidgets import render_plotly
from scipy import stats

# Constants
DEQUE_SIZE: int = 60
UPDATE_INTERVAL_SECS: int = 2  # Default interval for updates

# Reactive value wrapper
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

# Reactive calculation for combined data
@reactive.calc()
def reactive_calc_combined():
    # Invalidate every update interval
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Random temperature generation between -21 and -16 degrees Celsius
    temp = round(random.uniform(-21, -16), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    latest_dictionary_entry = {"temp": temp, "timestamp": timestamp}

    # Append the new entry to the deque
    reactive_value_wrapper.get().append(latest_dictionary_entry)

    # Snapshot and dataframe creation
    deque_snapshot = reactive_value_wrapper.get()
    df = pd.DataFrame(deque_snapshot)
    
    return deque_snapshot, df, latest_dictionary_entry

# Define UI
ui.page_opts(title="Penguin Air Temperature Live Tracker", fillable=False)  # Updated app title

# Sidebar UI
with ui.sidebar(open="open"):
    ui.input_dark_mode(mode="light")  # Dark mode toggle
    ui.h2("Explore the Penguins' Flight Data", class_="text-center")  # Updated sidebar title
    ui.p(
        "Track the temperatures of the penguins soaring through the icy skies. Real-time data from our flight crew.",
        class_="text-left",  # Updated description text
    )
    ui.hr()

    # Correct penguin image section using the provided URL
    ui.img(
        src="https://media.istockphoto.com/id/147290529/photo/emperors.jpg?s=612x612&w=0&k=20&c=ZApZFJtKoXGKYYJsgNcNPTMHqqSbbAx9CBg2AF2qyJk=",  # Penguin image source
        alt="Emperor Penguins",
        class_="center-img",  # CSS class for styling
    )

    # Updated text for tracking penguin temperature trends
    ui.p(
        ui.tags.i(class_="fas fa-thermometer-half", style="font-size: 1.5em; color: red;"),  # Thermometer icon
        " Track real-time penguin temperature variations and trends."
    )

    ui.hr()

    # Slider for limiting the number of data points displayed
    ui.input_slider("chart_limit", "Number of data points:", min=1, max=60, value=15)

    # Slider for controlling the update interval in seconds
    ui.input_slider("update_interval", "Update Interval (seconds):", min=1, max=30, value=2)

    ui.hr()

    # Update footer with GitHub and PyShiny links
    ui.p(
        ui.a(
            ui.tags.i(class_="fa-brands fa-github", style="font-size: 1.5em; color: black;"),
            "GitHub Source",
            href="https://github.com/Elen-tesfai/cintel-05-cintel/blob/main/",
            target="_blank",
        ),
        class_="text-left"
    )
    ui.p(
        ui.a(
            ui.tags.i(class_="fa-brands fa-github", style="font-size: 1.5em; color: black;"),
            "GitHub App",
            href="https://github.com/Elen-tesfai/cintel-05-cintel/blob/main/dashboard/app.py",
            target="_blank",
        ),
        class_="text-left"
    )
    ui.p(
        ui.a(
            ui.tags.i(class_="fa-brands fa-github", style="font-size: 1.5em; color: black;"),
            "PyShiny",
            href="https://shiny.posit.co/py/",
            target="_blank",
        ),
        class_="text-left"
    )

# Main content layout
with ui.layout_columns():
    # Value Box for current temperature
    with ui.value_box(
        showcase=icon_svg("thermometer"),  # Thermometer icon
        theme="bg-gradient-lightblue",      # Light blue gradient background
    ):
        "Current Temperature"
        
        @render.text
        def display_temp():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['temp']} °C"
        
        "Too cold for me!"

    # Value Box for current date and time
    with ui.value_box(
        showcase=icon_svg("clock"),  # Clock icon
        theme="bg-gradient-lightblue",  # Light blue gradient background
    ):
        "Current Date and Time"
        
        @render.text
        def display_time():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"

# New row for displaying recent readings in a table
with ui.layout_columns():
    with ui.card(height="250px", theme="bg-lightblue"):  # Light blue card background
        ui.card_header("Most Recent Readings")
        
        @render.data_frame
        def display_df():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            pd.set_option('display.width', None)  # Use maximum width for the dataframe
            return render.DataGrid(df, width="100%")

# New row for displaying chart and trend
with ui.layout_columns():
    with ui.card(height="600px", theme="bg-lightblue"):  # Light blue card background
        ui.card_header("Chart and Current Trend")
        
        @render_plotly
        def display_plot():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()

            if not df.empty:
                df_limited = df.tail(input.chart_limit())  # Limit the number of data points to display based on input
                df_limited["timestamp"] = pd.to_datetime(df_limited["timestamp"])

                # Scatter plot for temperature readings over time
                fig = px.scatter(df_limited,
                                 x="timestamp",
                                 y="temp",
                                 title="Temperature Readings with Regression Line",
                                 labels={"temp": "Temperature (°C)", "timestamp": "Time (local)"},
                                 color_discrete_sequence=["#007bff"])  # Blue color for the scatter points

                # Set y-axis range
                fig.update_yaxes(range=[-22, 0])

                # Regression line calculation
                sequence = range(len(df_limited))
                x_vals = list(sequence)
                y_vals = df_limited["temp"]

                slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
                df_limited['best_fit_line'] = [slope * x + intercept for x in x_vals]

                # Add regression line to the plot
                fig.add_scatter(x=df_limited["timestamp"], y=df_limited['best_fit_line'], mode='lines', name='Regression Line')

                # Update layout for the plot
                fig.update_layout(
                    xaxis_title="Time (local)", 
                    yaxis_title="Temperature (°C)"
                )

            return fig