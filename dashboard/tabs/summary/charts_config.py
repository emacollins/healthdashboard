import colors
import fonts

TITLE_X = 0.5
TITLE_Y = 0.9

SUMMARY_MARGIN = {"l": 5, "r": 50, "t": 80, "b": 60, "pad": 0}

workout_heatmap_chart_config = {
    "layout": {
        "autosize": True,
        "xaxis": {"title_text": None, "side": "top"},
        "yaxis": {"title_text": None},
        "coloraxis": {"showscale": False},
    },
}
favorite_workout_chart_config = {
    "y_data_column": "activity_name",
    "x_data_column": "count",
    "layout": {
        "colorway": [colors.SUMMARY_EXERCISE_COLOR],
        "xaxis": {
            "title": "",
            "color": colors.CHART_TEXT_COLOR,
            "showgrid": False,
            "showticklabels": False,
        },
        "yaxis": {
            "title": "",
            "color": colors.CHART_TEXT_COLOR,
            "showgrid": False,
            "tickfont": {"size": 14},
            "automargin": True,
        },
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "margin": {"l": 0, "r": 20, "t": 10, "b": 5, "pad": 0},
        "font": {"family": fonts.FONT},
        "bargap": 0.5,
    },
}


# X data column is always the index of the dataframe
summary_charts_config = {
    "ActiveEnergy": {
        "y_data_column": "total_calories",
        "layout": {
            "title": {
                "text": "Calories Burned Per Day",
                "x": TITLE_X,
                "y": TITLE_Y,
                "font": {"color": colors.CHART_TEXT_COLOR, "size": 20},
            },
            "colorway": [colors.SUMMARY_CALORIES_COLOR],
            "xaxis": {"title": "", "color": colors.CHART_TEXT_COLOR, "showgrid": False},
            "yaxis": {
                "title": "",
                "color": colors.CHART_TEXT_COLOR,
                "showgrid": False,
            },
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "margin": SUMMARY_MARGIN,
            "font": {"family": fonts.FONT},
        },
    },
    "ExerciseMinutes": {
        "y_data_column": "exercise_minutes",
        "layout": {
            "title": {
                "text": "Exercise Minutes Per Day",
                "x": TITLE_X,
                "y": TITLE_Y,
                "font": {"color": colors.CHART_TEXT_COLOR, "size": 20},
            },
            "colorway": [colors.SUMMARY_EXERCISE_COLOR],
            "xaxis": {
                "title": "",
                "color": colors.CHART_TEXT_COLOR,
                "showgrid": False,
            },
            "yaxis": {
                "title": "",
                "color": colors.CHART_TEXT_COLOR,
                "showgrid": False,
            },
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "margin": SUMMARY_MARGIN,
            "font": {"family": fonts.FONT},
        },
    },
    "SleepHours": {
        "y_data_column": "hours_slept",
        "layout": {
            "title": {
                "text": "Sleep Hours Per Night",
                "x": TITLE_X,
                "y": TITLE_Y,
                "font": {"color": colors.CHART_TEXT_COLOR, "size": 20},
            },
            "colorway": [colors.SUMMARY_SLEEP_COLOR],
            "xaxis": {
                "title": "",
                "color": colors.CHART_TEXT_COLOR,
                "showgrid": False,
            },
            "yaxis": {
                "title": "",
                "color": colors.CHART_TEXT_COLOR,
                "showgrid": False,
            },
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "margin": SUMMARY_MARGIN,
            "font": {"family": fonts.FONT},
        },
    },
}
