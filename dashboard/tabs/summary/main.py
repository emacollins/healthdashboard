from dash import html, dcc

from tabs.summary import components as c

SUMMARY_TAB = html.Div(
    id="SummaryTab",
    className="body",
    children=[
        html.Div(
            id="Columns",
            children=[
                html.Div(
                    id="SummaryCalories",
                    children=[
                        c.CALORIES_ROLLING_FIGURE,
                    ],
                    style={"flex": "1"}
                ),
                html.Div(
                    id="SummaryExercise",
                    children=[
                        c.EXERCISE_ROLLING_FIGURE,
                    ],
                    style={"flex": "1"}
                ),
                html.Div(
                    id="SummarySleep",
                    children=[
                        c.SLEEP_ROLLING_FIGURE,
                    ],
                    style={"flex": "1"}
                ),
            ],
            style={"display": "flex", "flex-direction": "row", "flex-wrap": "wrap"},
        ),
    ],
)
