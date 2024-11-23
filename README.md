# Cintel-05-Cintel: Continuous Intelligence - Live Data Stream & User Interaction

## Overview

The **Continuous Intelligence** project is a web application built using **PyShiny** to display live data streams. This application allows users to interact with real-time data and visualize trends as data is processed in motion. The primary focus of this project is to demonstrate the power of **continuous intelligence (CI)** by utilizing live data feeds and enabling user interactions.

The application processes data streams, such as real-time metrics or sensor readings, and updates the visualizations dynamically. Users can interact with the data through a simple, user-friendly interface and adjust parameters in real-time.

## Features

- **Real-Time Data Streams**: Displays live data updates as they are received, simulating real-world streaming data scenarios.
- **User Interaction**: Interactive elements allow users to modify the data or parameters and see the effects immediately.
- **Live Data Visualization**: Graphical plots that update continuously with incoming data, showing trends, averages, and other statistical metrics.
- **Statistical Insights**: Displays key statistics, such as averages, maximums, and minimums, to enhance data understanding.
- **Deque Management**: Uses Python’s **deque** data structure to handle and process recent data efficiently.
## Required Packages

This project requires the following Python packages:

- **faicons**: Used for Font Awesome free icons, providing scalable vector icons for your web app interface.
- **pandas**: A powerful library for data manipulation and analysis, particularly used for working with tabular data in Python.
- **pyarrow**: A dependency required by the latest version of `pandas`, used for efficient data serialization and deserialization.
- **plotly**: A graphing library for creating interactive visualizations and charts.
- **scipy**: A Python library used for scientific and technical computing. Specifically, it's used here for the `stats.linregress` function to build a trend line for charts.
- **shiny**: A Python web application framework used to build interactive web applications, the core tool for creating this app.
- **shinylive**: A tool to help build the app and deploy it to GitHub Pages by exporting it to the `docs` folder.
- **shinywidgets**: A wrapper for integrating complex widgets, such as interactive `plotly` charts, into the Shiny app.

## Installation

1. **Clone the repository**:
```bash
   git clone https://github.com/Elen-tesfai/cintel-05-cintel.git
   cd cintel-05-cintel
   ```
2. **Create and activate a virtual environment (optional but recommended)**:
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install the required packages**:
```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
```bash
   python dashboard/app.py
   ```