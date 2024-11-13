import shiny
import plotly.express as px
import pandas as pd

# Sample data for demonstration
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Value': [4, 7, 1, 8]
})

# Create a Plotly bar chart
fig = px.bar(df, x='Category', y='Value', title="Simple Bar Chart")

# Define the Shiny UI layout
app_ui = shiny.ui.page_fluid(
    shiny.ui.output_plot("plot")
)

# Define the server function to render the plot
def server(input, output, session):
    output.plot = shiny.render.plot(fig)  # Updated to render.plot()

# Create the Shiny app
app = shiny.App(app_ui, server)

# Run the app
if __name__ == "__main__":
    app.run()