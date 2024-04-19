from dash import html, dcc
from datetime import datetime as dt

from tabs.summary.components import SUMMARY_TAB
from tabs.activity.main import ACTIVITY_TAB
from tabs.workout.main import WORKOUT_TAB
from tabs.sleep.main import SLEEP_TAB
from tabs.insights.main import INSIGHTS_TAB

import colors, fonts

MAIN_HEADER = html.H1(
    children="Health Report",
    style={
        "text-align": "center",
        "font-family": fonts.FONT,
        "color": colors.CHART_TEXT_COLOR,
        "font-size": "48px",
    },
)

MAIN_HEADER = html.Div(
    children=[
        html.H1(
            children="Health Report",
            style={
                "text-align": "center",
                "font-family": "Helvetica, sans-serif",
                "color": "#333",
                "font-size": "48px",
            },
        ),
        html.H2(
            children="Created by Eric Collins",
            style={
                "text-align": "center",
                "font-family": "Roboto, sans-serif",
                "color": colors.GENERAL_TEXT_COLOR,
                "font-size": "18px",
            },
        ),
        html.Img(
            src="assets/logo_transparent.png",
            style={
                "height": "300px",
                "width": "300px",
                "position": "absolute",
                "top": "-100px",
                "left": "850px",
            },
        ),
    ],
    style={
        "position": "relative",
    },
)
# ---------------------------------------------------------
SETTINGS_BAR = html.Div(
    children=[
        dcc.DatePickerRange(
            id="DateRange",
            start_date=dt(2022, 7, 1).date(),
            end_date=dt(2024, 4, 18).date(),
            style={"font-family": fonts.FONT, "color": colors.GENERAL_TEXT_COLOR},
        ),
    ]
)
# ---------------------------------------------------------
TABS = dcc.Tabs(
    id="tabs",
    children=[
        dcc.Tab(label="Summary", children=SUMMARY_TAB, className='custom-tabs', selected_className='custom-tab--selected'),
        dcc.Tab(label="Activity", children=ACTIVITY_TAB, className='custom-tabs', selected_className='custom-tab--selected'),
        dcc.Tab(label="Workout", children=WORKOUT_TAB, className='custom-tabs', selected_className='custom-tab--selected'),
        dcc.Tab(label="Sleep", children=SLEEP_TAB, className='custom-tabs', selected_className='custom-tab--selected'),
        dcc.Tab(label="Insights", children=INSIGHTS_TAB, className='custom-tabs', selected_className='custom-tab--selected'),
    ],
)
