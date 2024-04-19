from dash import html, dcc

import colors, fonts

GRAPH_STYLE = {
    "margin": "30px",
    "borderRadius": "20px",
    "backgroundColor": colors.CHART_BACKGROUND_COLOR,
}

CALORIES_ROLLING_FIGURE = dcc.Graph(id="SummaryCaloriesFigure", style=GRAPH_STYLE)

EXERCISE_ROLLING_FIGURE = dcc.Graph(id="SummaryExerciseFigure", style=GRAPH_STYLE)

SLEEP_ROLLING_FIGURE = dcc.Graph(id="SummarySleepFigure", style=GRAPH_STYLE)

TOTAL_CALORIES_BURNED = html.Div(
    id="SummaryCaloriesTotalCaloriesSection",
    children=[
        html.H2("Total Calories Burned:", style={"margin-right": "10px", "color": colors.GENERAL_TEXT_COLOR}),
        html.H2(id="SummaryCaloriesTotalCaloriesBurned", style={"color": colors.SUMMARY_CALORIES_COLOR}),
    ],
    style={
                "display": "flex",
                "flex-direction": "row",
                "flex-wrap": "nowrap",
                "margin-left": "50px", #2x GRAPH_STYLE margin - margin-right
            },
)

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
                        TOTAL_CALORIES_BURNED,
                    ],
                    style={
                        "flex": "1"
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
                "flex-wrap": "nowrap",
                "backgroundColor": colors.BACKGROUND_COLOR,
            },
        ),
    ],
    style={"font-family": fonts.FONT}
)
