from dash import html, dcc

BACKGROUND_COLOR = "#F6F6F6"

GRAPH_STYLE = style = {
    "margin": "50px",
    "borderRadius": "20px",
    "backgroundColor": "white",
}

CALORIES_ROLLING_FIGURE = dcc.Graph(id="SummaryCaloriesFigure", style=GRAPH_STYLE)

EXERCISE_ROLLING_FIGURE = dcc.Graph(id="SummaryExerciseFigure", style=GRAPH_STYLE)

SLEEP_ROLLING_FIGURE = dcc.Graph(id="SummarySleepFigure", style=GRAPH_STYLE)

SUMMARY_TAB = html.Div(
    id="SummaryTab",
    children=[
        html.Div(
            id="Columns",
            children=[
                html.Div(
                    id="SummaryCalories",
                    children=[
                        CALORIES_ROLLING_FIGURE,
                    ],
                    style={
                        "flex": "1",
                    },
                ),
                html.Div(
                    id="SummaryExercise",
                    children=[
                        EXERCISE_ROLLING_FIGURE,
                    ],
                    style={"flex": "1"},
                ),
                html.Div(
                    id="SummarySleep",
                    children=[
                        SLEEP_ROLLING_FIGURE,
                    ],
                    style={"flex": "1"},
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
                "flex-wrap": "wrap",
                "backgroundColor": BACKGROUND_COLOR,
            },
        ),
    ],
)
