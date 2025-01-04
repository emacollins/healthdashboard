from dash import html, dcc


UPLOAD_TAB = html.Div(
    [
        dcc.Input(id="upload-username-input", type="text", required=True),
        dcc.Upload(
            id="upload-file",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "50%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=False,
        ),
        html.Div(id="output-message"),
    ]
)
