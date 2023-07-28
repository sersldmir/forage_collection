from dash.testing.application_runners import import_app
# from dash import Dash, html, dcc, Input, Output, callback
# import dash_bootstrap_components as dbc
# import plotly.express as px
# import pandas as pd

def test_app(dash_duo):
    """Simple test to check if the app works. Checks header, graph and filter"""

    app = import_app("simple_dash")
    dash_duo.start_server(app)

    dash_duo.wait_for_text_to_equal("h1", "My mini Dash web-dashboard", 5)

    assert dash_duo.find_element("h3").text == "Sales plot"

    assert dash_duo.find_element("#line-chart") != None

    assert dash_duo.find_element("#check-list") != None

    assert dash_duo.get_logs() == [], "Browser console should contain no error"
    ...