from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv("data/sales_data.csv", parse_dates=["date"])

fig = px.line(data_frame=df, x="date", y="sales", color="region")

app.layout = html.Div(children=[
    html.H1(children='My mini Dash web-dashboard'),

    html.Div(children='''
        Sales plot.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)