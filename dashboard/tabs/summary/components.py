from dash import html, dcc

import colors, fonts

GRAPH_STYLE = {
    "margin": "30px",
    "borderRadius": "20px",
    "backgroundColor": colors.CHART_BACKGROUND_COLOR,
    "width": "400px",
    "height": "300px",
}

CALORIES_ROLLING_FIGURE = dcc.Graph(id="SummaryCaloriesFigure", style=GRAPH_STYLE)

EXERCISE_ROLLING_FIGURE = dcc.Graph(id="SummaryExerciseFigure", style=GRAPH_STYLE)

SLEEP_ROLLING_FIGURE = dcc.Graph(id="SummarySleepFigure", style=GRAPH_STYLE)

FAVORITE_WORKOUTS_FIGURE = dcc.Graph(
    id="SummaryFavoriteWorkoutsFigure", style=GRAPH_STYLE
)

WORKOUT_HEATMAP_FIGURE = dcc.Graph(id="SummaryWorkoutHeatmapFigure", style=GRAPH_STYLE)

HOURS_SLEPT_VARIABILITY_FIGURE = dcc.Graph(id="SummaryHoursSleptVariabilityFigure", style=GRAPH_STYLE)
WAKE_UP_TIME_VARIABILITY_FIGURE = dcc.Graph(id="SummaryWakeUpTimeVariabilityFigure", style=GRAPH_STYLE)
FALL_ASLEEP_TIME_VARIABILITY_FIGURE = dcc.Graph(id="SummaryFallAsleepTimeVariabilityFigure", style=GRAPH_STYLE)


TOTAL_CALORIES_BURNED = html.Div(
    id="SummaryCaloriesTotalCaloriesSection",
    children=[
        html.H2(
            "Total Calories Burned:",
            style={"margin-right": "10px", "color": colors.GENERAL_TEXT_COLOR},
        ),
        html.H2(
            id="SummaryCaloriesTotalCaloriesBurned",
            style={"color": colors.SUMMARY_CALORIES_COLOR},
        ),
    ],
    style={
        "display": "flex",
        "flex-direction": "row",
        "flex-wrap": "nowrap",
        "margin-left": "50px",  # 2x GRAPH_STYLE margin - margin-right
    },
)

TOTAL_MINUTES_EXERCISED = html.Div(
    id="SummaryExerciseTotalExerciseSection",
    children=[
        html.H2(
            "Total Exercise Minutes:",
            style={"margin-right": "10px", "color": colors.GENERAL_TEXT_COLOR},
        ),
        html.H2(
            id="SummaryExerciseTotalExercise",
            style={"color": colors.SUMMARY_EXERCISE_COLOR},
        ),
    ],
    style={
        "display": "flex",
        "flex-direction": "row",
        "flex-wrap": "nowrap",
        "margin-left": "50px",  # 2x GRAPH_STYLE margin - margin-right
    },
)

AVERAGE_SLEEP_PER_NIGHT = html.Div(
    id="SummaryAvgSleepSection",
    children=[
        html.H2(
            "Average Hours Slept:",
            style={"margin-right": "10px", "color": colors.GENERAL_TEXT_COLOR},
        ),
        html.H2(
            id="SummaryAvgSleep",
            style={"color": colors.SUMMARY_SLEEP_COLOR},
        ),
    ],
    style={
        "display": "flex",
        "flex-direction": "row",
        "flex-wrap": "nowrap",
        "margin-left": "50px",  # 2x GRAPH_STYLE margin - margin-right
    },
)

CALORIES_POWER_EQUIVALENT_DROPDOWN = html.Div(
    id="SummaryCaloriesPowerEquivalentSection",
    children=[
        html.H3(
            "Powered the average",
            style={"margin-right": "10px", "color": colors.GENERAL_TEXT_COLOR},
        ),
        dcc.Dropdown(
            id="SummaryCaloriesPowerEquivalentDropdown",
            style={"flex": "1", "margin-top": "6px"},
        ),
        html.H3(
            "for...", style={"margin-left": "10px", "color": colors.GENERAL_TEXT_COLOR}
        ),
    ],
    style={
        "display": "flex",
        "flex-direction": "row",
        "flex-wrap": "nowrap",
        "margin-left": "50px",  # 2x GRAPH_STYLE margin - margin-right
    },
)

CALORIES_POWER_EQUIVALENT_VALUE = html.H2(
    id="SummaryCaloriesPowerEquivalentValue",
    style={"margin-left": "180px", "color": colors.SUMMARY_CALORIES_COLOR},
)

CALORIES_POWER_EQUIVALENT = html.Div(
    id="SummaryCaloriesEquivalent",
    children=[CALORIES_POWER_EQUIVALENT_DROPDOWN, CALORIES_POWER_EQUIVALENT_VALUE],
    style={
        "align-items": "center",
    },
)

BURGER_LINE = html.Div(
    id="SummaryBurger",
    children=[
        html.H3(
            id="BurgersValue",
            style={"color": colors.SUMMARY_CALORIES_COLOR},
        ),
        html.H3(
            "Burgers",
            style={"margin-left": "10px", "color": colors.GENERAL_TEXT_COLOR},
        ),
    ],
    style={
        "display": "flex",
        "flex-direction": "row",
        "flex-wrap": "nowrap",  # 2x GRAPH_STYLE margin - margin-right
    },
)

CHEEZEITS_LINE = html.Div(
    id="SummaryCheezeits",
    children=[
        html.H3(
            id="CheezeitsValue",
            style={"color": colors.SUMMARY_CALORIES_COLOR},
        ),
        html.H3(
            "Cheez-Its",
            style={"margin-left": "10px", "color": colors.GENERAL_TEXT_COLOR},
        ),
    ],
    style={
        "display": "flex",
        "flex-direction": "row",
        "flex-wrap": "nowrap",  # 2x GRAPH_STYLE margin - margin-right
    },
)

FOOD_EQUIVALENT_SUMMARY = html.Div(
    id="SummaryFoodEquivalent",
    children=[
        html.H3(
            "Burned the equivalent of...", style={"color": colors.GENERAL_TEXT_COLOR}
        ),
        BURGER_LINE,
        CHEEZEITS_LINE,
    ],
    style={
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
    },
)

FAVORITE_WORKOUTS = html.Div(
    id="SummaryFavoriteWorkouts",
    children=[
        html.H3("Recorded Workouts", style={"color": colors.GENERAL_TEXT_COLOR, "margin-bottom": "0px"}),
        FAVORITE_WORKOUTS_FIGURE,
    ],
    style={
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
    },
)

WORKOUT_HEATMAP = html.Div(
    id="SummaryWorkoutHeatmap",
    children=[
        WORKOUT_HEATMAP_FIGURE,
    ],
    style={
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
    },
)

SLEEP_VARIABILITY = html.Div(
    id="SummarySleepVariability",
    children=[
        html.Div(HOURS_SLEPT_VARIABILITY_FIGURE, style={"margin-bottom": "-40px"}),
        html.Div(WAKE_UP_TIME_VARIABILITY_FIGURE, style={"margin-bottom": "-40px"}),
        html.Div(FALL_ASLEEP_TIME_VARIABILITY_FIGURE)
    ],
    style={
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
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
                        html.Br(),
                        html.Br(),
                        CALORIES_POWER_EQUIVALENT,
                        html.Br(),
                        FOOD_EQUIVALENT_SUMMARY,
                    ],
                    style={"flex": "1"},
                ),
                html.Div(
                    id="SummaryExercise",
                    children=[
                        EXERCISE_ROLLING_FIGURE,
                        TOTAL_MINUTES_EXERCISED,
                        html.Br(),
                        WORKOUT_HEATMAP,
                        FAVORITE_WORKOUTS,
                    ],
                    style={"flex": "1"},
                ),
                html.Div(
                    id="SummarySleep",
                    children=[
                        SLEEP_ROLLING_FIGURE,
                        AVERAGE_SLEEP_PER_NIGHT,
                        SLEEP_VARIABILITY
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
    style={"font-family": fonts.FONT},
)
