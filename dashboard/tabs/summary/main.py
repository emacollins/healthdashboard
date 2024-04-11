from dash import html, dcc

from tabs.summary import components as c

SUMMARY_TAB = html.Div(
    id="SummaryTab",
    className="body",
    children=[
        html.Div(
            id="SummaryCalories",
            children=[
                c.CALORIES_ROLLING_FIGURE,
            ],
            style={"display": "flex", "flex-direction": "row"},

        )
    ]
)
