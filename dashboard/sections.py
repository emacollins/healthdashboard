from dash import html, dcc
from datetime import datetime as dt

from tabs.summary.main import SUMMARY_TAB
from tabs.activity.main import ACTIVITY_TAB
from tabs.workout.main import WORKOUT_TAB
from tabs.sleep.main import SLEEP_TAB
from tabs.insights.main import INSIGHTS_TAB

MAIN_HEADER = html.H1(
    children="Health Dashboard"
)
#---------------------------------------------------------
SETTINGS_BAR = html.Div(
    children=[
        dcc.DatePickerRange(
            id="DateRange", start_date=dt(2022, 7, 1).date(), end_date=dt(2024, 4, 1).date()
        ),
    ]
)
#---------------------------------------------------------
TABS = dcc.Tabs(
    id="tabs",
    children=[
        dcc.Tab(label="Summary", children=SUMMARY_TAB),
        dcc.Tab(label="Activity", children=ACTIVITY_TAB),
        dcc.Tab(label="Workout", children=WORKOUT_TAB),
        dcc.Tab(label="Sleep", children=SLEEP_TAB),
        dcc.Tab(label="Insights", children=INSIGHTS_TAB),
    ],
)

