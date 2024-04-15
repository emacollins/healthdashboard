columns_and_titles = [
    ("active_energy_burned", "Active Energy Burned"),
    ("exercise_minutes", "Exercise Minutes"),
    ("stand_hours", "Stand Hours"),
]

CHART_BACKGROUND_COLOR = "black"

# X data column is always the index of the dataframe
summary_charts_config = {
    "ActiveEnergy": {
        "y_data_column": "active_energy_burned",
        "layout": {
            "title": {
                "text": "Calories Burned",
                "x": 0.5,
                "font": {"color": CHART_BACKGROUND_COLOR},
            },
            "colorway": ["#FA4A41"],
            "xaxis": {"title": "Date", "color": "black", "showgrid": False},
            "yaxis": {
                "title": "",
                "color": CHART_BACKGROUND_COLOR,
                "showgrid": False,
            },
            "plot_bgcolor": CHART_BACKGROUND_COLOR,
            "paper_bgcolor": "white",
        },
    },
    "ExerciseMinutes": {
        "y_data_column": "exercise_minutes",
        "layout": {
            "title": {"text": "Exercise Minutes", "x": 0.5, "font": {"color": "black"}},
            "colorway": ["#B2FA49"],
            "xaxis": {
                "title": "Date",
                "color": "black",
                "showgrid": False,
            },
            "yaxis": {
                "title": "Minutes Per Day",
                "color": "black",
                "showgrid": False,
            },
            "plot_bgcolor": CHART_BACKGROUND_COLOR,
            "paper_bgcolor": "white",
        },
    },
    "SleepHours": {
        "y_data_column": "hours_slept",
        "layout": {
            "title": {"text": "Sleep Hours", "x": 0.5, "font": {"color": "black"}},
            "colorway": ["#97EBFA"],
            "xaxis": {
                "title": "Date",
                "color": "black",
                "showgrid": False,
            },
            "yaxis": {
                "title": "Hours Per Day",
                "color": "black",
                "showgrid": False,
            },
            "plot_bgcolor": CHART_BACKGROUND_COLOR,
            "paper_bgcolor": "white",
        },
    },
}
