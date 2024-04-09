columns_and_titles = [
    ("active_energy_burned", "Active Energy Burned"),
    ("exercise_minutes", "Exercise Minutes"),
    ("stand_hours", "Stand Hours"),
]

# X data column is always the index of the dataframe
summary_charts_config = {
    "ActiveEnergy": {
        "y_data_column": "active_energy_burned",
        "layout": {
            "title": {
                "text": "Active Energy Burned",
                "x": 0.5,
                "font": {"color": "white"},
            },
            "colorway": ["#FA4A41"],
            "xaxis": {"title": "Date", "color": "white", "showgrid": False},
            "yaxis": {
                "title": "Calories Burned Per Day",
                "color": "white",
                "showgrid": False,
            },
            "plot_bgcolor": "black",
            "paper_bgcolor": "black",
        },
    },
    "ExerciseMinutes": {
        "y_data_column": "exercise_minutes",
        "layout": {
            "title": {"text": "Exercise Minutes", "x": 0.5, "font": {"color": "white"}},
            "colorway": ["#B2FA49"],
            "xaxis": {
                "title": "Date",
                "color": "white",
                "showgrid": False,
            },
            "yaxis": {
                "title": "Minutes Per Day",
                "color": "white",
                "showgrid": False,
            },
            "plot_bgcolor": "black",
            "paper_bgcolor": "black",
        },
    },
    "StandHours": {
        "y_data_column": "stand_hours",
        "layout": {
            "title": {"text": "Stand Hours", "x": 0.5, "font": {"color": "white"}},
            "colorway": ["#435EFA"],
            "xaxis": {
                "title": "Date",
                "color": "white",
                "showgrid": False,
            },
            "yaxis": {
                "title": "Hours Per Day",
                "color": "white",
                "showgrid": False,
            },
            "plot_bgcolor": "black",
            "paper_bgcolor": "black",
        },
    },
}
