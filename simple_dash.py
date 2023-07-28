from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv("data/sales_data.csv", parse_dates=["date"])

# fig = px.line(data_frame=df, x="date", y="sales", color="region")

app.layout = html.Div(children=[
    html.H1(children='My mini Dash web-dashboard'),

    html.Div(children='''
        Sales plot.
    '''),

    dcc.Checklist(options=df["region"].unique(), value=df["region"].unique(), id="check-list"),


    dcc.Graph(
        id='line-chart',
    )
])


@callback(
    Output("line-chart", "figure"),
    Input("check-list", "value")
)
def update_line_chart(selected_regions):
    
    filtered_df = df[df["region"].isin(selected_regions)]

    fig = px.line(data_frame=filtered_df, x="date", y="sales", color="region")

    fig.update_layout(transition_duration=100)

    return fig


if __name__ == '__main__':
    app.run(debug=True)