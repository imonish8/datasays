import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_uploader as du
import plotly.express as px
import pandas as pd
import os
import streamlit as st
import pandas as pd
import plotly.express as px
app = dash.Dash(__name__)
server = app.server  # For deployment

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
du.configure_upload(app, UPLOAD_FOLDER)


app.layout = html.Div([
    html.H1("CSV Data Visualization"),
    du.Upload(
        id='upload-data',
        text='Drag and Drop or Select Files',
        max_file_size=1800,  # 1.8 MB
        filetypes=['csv'],
        upload_id='csv-upload'  # Unique session id
    ),
    html.Div(id='output-data-upload'),
    html.Div(id='graph-output')
])

@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'isCompleted'),
    State('upload-data', 'fileNames'),
    prevent_initial_call=True
)
def update_output(isCompleted, filenames):
    if isCompleted:
        if filenames is not None:
            file_path = os.path.join(UPLOAD_FOLDER, filenames[0])
            df = pd.read_csv(file_path)
            os.remove(file_path)  # Clean up the uploaded file

            return html.Div([
                html.H5("Select Columns for Visualization"),
                html.Label("X-axis"),
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    value=df.columns[0]
                ),
                html.Label("Y-axis"),
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    value=df.columns[1]
                ),
                html.Label("Select Plot Type"),
                dcc.Dropdown(
                    id='plot-type',
                    options=[
                        {'label': 'Line Plot', 'value': 'line'},
                        {'label': 'Bar Plot', 'value': 'bar'},
                        {'label': 'Scatter Plot', 'value': 'scatter'}
                    ],
                    value='line'
                ),
                html.Button('Generate Plot', id='generate-plot', n_clicks=0)
            ])
    return html.Div()

@app.callback(
    Output('graph-output', 'children'),
    Input('generate-plot', 'n_clicks'),
    State('xaxis-column', 'value'),
    State('yaxis-column', 'value'),
    State('plot-type', 'value'),
    State('upload-data', 'fileNames'),
    prevent_initial_call=True
)
def update_graph(n_clicks, x_column, y_column, plot_type, filenames):
    if n_clicks > 0:
        file_path = os.path.join(UPLOAD_FOLDER, filenames[0])
        df = pd.read_csv(file_path)

        if plot_type == 'line':
            fig = px.line(df, x=x_column, y=y_column)
        elif plot_type == 'bar':
            fig = px.bar(df, x=x_column, y=y_column)
        elif plot_type == 'scatter':
            fig = px.scatter(df, x=x_column, y=y_column)
        else:
            return html.Div("Invalid plot type selected.")

        return dcc.Graph(figure=fig)
    return html.Div()

st.title("CSV Data Visualization")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(df.head())

    # Select columns
    x_column = st.selectbox("Select X-axis column", df.columns)
    y_column = st.selectbox("Select Y-axis column", df.columns)

    # Select plot type
    plot_type = st.selectbox(
        "Select Plot Type",
        ("Line Plot", "Bar Plot", "Scatter Plot")
    )

    # Generate plot
    if st.button("Generate Plot"):
        if plot_type == "Line Plot":
            fig = px.line(df, x=x_column, y=y_column)
        elif plot_type == "Bar Plot":
            fig = px.bar(df, x=x_column, y=y_column)
        elif plot_type == "Scatter Plot":
            fig = px.scatter(df, x=x_column, y=y_column)
        else:
            st.error("Invalid plot type selected.")

        st.plotly_chart(fig)


if __name__ == '__main__':
    app.run_server(debug=True)