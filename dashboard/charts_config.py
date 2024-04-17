columns_and_titles = [
    ("active_energy_burned", "Active Energy Burned"),
    ("exercise_minutes", "Exercise Minutes"),
    ("stand_hours", "Stand Hours"),
]

CHART_BACKGROUND_COLOR = "#F5F5F5"
CHART_TEXT_COLOR = "#636363"

# X data column is always the index of the dataframe
summary_charts_config = {
    "ActiveEnergy": {
        "y_data_column": "active_energy_burned",
        "layout": {
            "title": {
                "text": "Calories Burned",
                "x": 0.5,
                "font": {"color": CHART_TEXT_COLOR},
            },
            "colorway": ["#EA491D"],
            "xaxis": {"title": "Date", "color": CHART_TEXT_COLOR, "showgrid": False},
            "yaxis": {
                "title": "",
                "color": CHART_TEXT_COLOR,
                "showgrid": False,
            },
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
        },
    },
    "ExerciseMinutes": {
        "y_data_column": "exercise_minutes",
        "layout": {
            "title": {"text": "Exercise Minutes", "x": 0.5, "font": {"color": CHART_TEXT_COLOR}},
            "colorway": ["#8EEB26"],
            "xaxis": {
                "title": "Date",
                "color": CHART_TEXT_COLOR,
                "showgrid": False,
            },
            "yaxis": {
                "title": "Minutes Per Day",
                "color": CHART_TEXT_COLOR,
                "showgrid": False,
            },
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
        },
    },
    "SleepHours": {
        "y_data_column": "hours_slept",
        "layout": {
            "title": {"text": "Sleep Hours", "x": 0.5, "font": {"color": CHART_TEXT_COLOR}},
            "colorway": ["#2651EB"],
            "xaxis": {
                "title": CHART_TEXT_COLOR,
                "color": CHART_TEXT_COLOR,
                "showgrid": False,
            },
            "yaxis": {
                "title": "Hours Per Day",
                "color": CHART_TEXT_COLOR,
                "showgrid": False,
            },
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
        },
    },
}
