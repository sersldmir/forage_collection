from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(name=__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv("data/sales_data.csv", parse_dates=["date"])

app.layout = html.Div(
    children=[
        html.H1(
            children="My mini Dash web-dashboard",
            style={"text-align": "center", "font-weight": "bold"},
        ),
        html.H3(
            children="Sales plot",
            style={"text-align": "center"},
        ),
        html.Div(
            children=[
                html.H4(children="Region Filter"),
                dbc.Checklist(options=df["region"].unique(), value=["south"], id="check-list"),
            ],
            style={"position": "absolute", "left": "45.7%"},
        ),
        dcc.Graph(id="line-chart", style={"padding-top": "10%"}),
    ],
    style={
        "background-image": "url(https://source.unsplash.com/nN1HSDtKdlw)",
        "background-repeat": "no-repeat",
        "background-position": "right top",
        "background-size": "1920px 1080px",
        "position": "absolute",
        "top": "0",
        "left": "0",
        "height": "100%",
        "width": "100%",
        "overflow": "hidden",
        "padding": "0px"
    },
)


@callback(Output("line-chart", "figure"), Input("check-list", "value"))
def update_line_chart(selected_regions):
    filtered_df = df[df["region"].isin(selected_regions)]

    fig = px.line(data_frame=filtered_df, x="date", y="sales", color="region")

    fig.update_layout(
        transition_duration=100,
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        xaxis_title="<b>Date</b>",
        yaxis_title="<b>Sales</b>",
        legend_title="<b>Regions</b>"
    )

    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b>")
    fig.update_yaxes(tickprefix="<b>",ticksuffix ="</b>")

    return fig


if __name__ == "__main__":
    app.run(debug=False)
