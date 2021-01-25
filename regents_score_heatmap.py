#imports
### Data
import pandas as pd
import pickle
### Graphing
import plotly.graph_objects as go

### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

#imports from MY program
import os
import dash_table
from six.moves.urllib.parse import quote

## Navbar, not necessary in this version
#from navbar import Navbar

#nav = Navbar()

# from jupyterlab_dash import AppViewer
# viewer = AppViewer()

#df = pd.read_csv('/Users/teacher/Desktop/DeWitt Data/HighestRegentsScoresCSV.csv', dtype={"Student Name": object, "Off Class": object})


def create_dashboard(server):
    clinton_url='https://raw.githubusercontent.com/angelojc/dewittclinton/master/HighestRegentsScoresCSV.csv'
    df = pd.read_csv(clinton_url,sep=",")

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    exam_list = ['Algebra 1', 'Algebra 2', 'Geometry', 'ELA', 'Spanish', 'Living Environment', 'Earth Science', 'Physics', 'Chemisty', 'US History', 'Global History']
    exam_codes = ['Algebra 1 Regents', 'Algebra 2 Regents', 'Geometry Regents', 'ELA Regents', 'Spanish Exam',  'Living Environment Regents', 'Earth Science Regents', 'Physics Regents', 'Chemistry Regents', 'US History Regents', 'Global Regents' ]

    education_list = ['All Students','General Education', 'Special Education/504', 'ENL/ESL']
    education_codes = [['1', '2', '3', '4', 'S', 'L', 'T', 'E', 'B'],['1', '2', '3', '4'],['S', 'L', 'T','E'],['B']]

    cohort_list = ['All Cohorts','Y (9th grade)', 'X (10th grade)', 'W (11th grade)', 'V (12th grade)', 'U (Over Age)']
    cohort_codes = [['Y', 'X', 'W', 'V', 'U'],['Y'], ['X'], ['W'], ['V'], ['U']]

    options_list = ['Who are within 5 points of passing an exam',
                   'Who have fulfilled all minimum regents requirements',
                   'Who have fulfilled an advance regents diploma requirements']

    #App Layout
    def RegentsScoreHeatMap():
        layout = html.Div([

            nav,

            html.Div([ html.Br()]),

            html.Div([
                 html.H1(children='TESTING TESTING')
            ], style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'95%', 'border':'3px solid crimson', 'padding': '10px', 'backgroundColor': 'white'}),

            html.Div([
                 html.H1(children='Student Regents Data: Regents Completion Heat Map')
            ], style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'95%', 'border':'3px solid crimson', 'padding': '10px', 'backgroundColor': 'white'}),

            html.Div([ html.Br()]),

             html.Div([
                html.H5(children='Description:'),

                dcc.Markdown('''
                    * This dashboard displays the scores of students regents examinations
                    * The checkboxes can be used to filter the display by exam title, student group, cohort, and custom optional parameters
                    * Users can view the student names and exam scores by hovering over the graph sections
                    * __This tool could be used to identify target students for regents completion/college readiness/diploma eligibility__
                    '''),
            ],style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'95%', 'border':'3px solid black', 'padding': '10px', 'backgroundColor': 'white'}
            ),

            html.Div([ html.Br()]),

            html.Div([
                html.Div([
                    html.Div([

                        html.H5(children='Show me these exam scores', style={'text-align':'center'}),

                        dcc.Checklist(
                            id = 'exam',
                            options=[{'label': exam_list[i], 'value': i} for i in range(len(exam_list))],
                            value = [0],
                            style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'90%', 'border':'3px solid black', 'padding': '10px'}
                        ),
                    ], style={'width':'22%'},
                    className="four columns"),

                    html.Div([

                        html.H5(children='For these students', style={'text-align':'center'}),

                        dcc.Checklist(
                            id = 'education',
                            options=[{'label': education_list[i], 'value': i} for i in range(len(education_list))],
                            value = [0],
                            style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'90%', 'border':'3px solid black', 'padding': '10px'}
                        )
                    ], style={'width':'16%'},
                    className="four columns"),

                    html.Div([

                        html.H5(children='In these cohorts', style={'text-align':'center'}),

                        dcc.Checklist(
                            id = 'cohort',
                            options=[{'label': cohort_list[i], 'value': i} for i in range(len(cohort_list))],
                            value = [0],
                            style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'90%', 'border':'3px solid black', 'padding': '10px'}
                        )
                    ], style={'width':'12%'},
                    className="four columns"),

                    html.Div([

                        html.H5(children='(Optional)', style={'text-align':'center'}),

                        dcc.Checklist(
                            id = 'options',
                            options=[{'label': options_list[i], 'value': i} for i in range(len(options_list))],
                            style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'90%', 'border':'3px solid black', 'padding': '10px'}
                        )
                    ], style={'width':'37%'},
                    className="four columns"),

                    #html.Button('Submit', id='button', style={'vertical-align':'middle'}),

                ], style={'display': 'block', 'margin-left':'auto', 'margin-right':'auto', 'width':'99%'},
                className="four columns"),

            ], style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'95%', 'border':'3px solid black', 'padding': '10px', 'backgroundColor': 'white'},
            className="row"),

            html.Div([ html.Br()]),

            html.Div([
                html.Div([
                    html.Div([ html.Br()]),

                    html.Div([
                        dcc.Graph(id='reg_heatmap')
                    ], style={'backgroundColor': 'white'})


                ])
           ],style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'95%', 'border':'3px solid black', 'padding': '10px', 'backgroundColor': 'white'}, className="row")

        ], style={'backgroundColor': 'whitesmoke'})

        return layout


    def update_reg_score_graph(exam, education, cohort, options):
        filter_df = df

        cohort_values = []

        #Value is a list even though I think it should be an index. I don't fully understand this
        for list_item in cohort:
            temp = (cohort_codes[list_item])
            for item in temp:
                cohort_values.append(item)

        cohort_conditions = filter_df['Off Class 3'].isin(cohort_values)

        education_values = []

        #"Value" is a list even though I think it should be an index. I don't fully understand this
        for list_item in education:
            temp = (education_codes[list_item])
            for item in temp:
                 education_values.append(item)

        education_conditions = filter_df['Off Class 2'].isin(education_values)

        exam_values = []

        for list_item in exam:
            exam_values.append(exam_list[list_item])

        graph_me = df[cohort_conditions & education_conditions]

        graph_me = graph_me.sort_values(['Total Pass Count']).reset_index(drop=True)

        all_frames = [graph_me['Algebra 1 Regents'], graph_me['Algebra 2 Regents'], graph_me['Chemistry Regents'], graph_me['Earth Science Regents'], graph_me['ELA Regents'],graph_me['Geometry Regents'], graph_me['Global Regents'], graph_me['US History Regents'], graph_me['Living Environment Regents'], graph_me['Physics Regents'], graph_me['Spanish Exam']]

        frames_for_z_axis = []

        for item in exam:
            frames_for_z_axis.append(all_frames[item])

        attendance_rates = []

        figure = go.Figure(
            data= [
                go.Heatmap(
                y=exam_values,
                #y=y_axis,
                x=graph_me['First Name'],
                #z=[graph_me['Algebra 1 Regents'], graph_me['Algebra 2 Regents'], graph_me['Chemistry Regents'], graph_me['Earth Science Regents'], graph_me['ELA Regents'],graph_me['Geometry Regents'], graph_me['Global Regents'], graph_me['US History Regents'], graph_me['Living Environment Regents'], graph_me['Physics Regents'], graph_me['Spanish Exam']],
                z=frames_for_z_axis,
                colorscale=[[0.00, 'red'],   [0.55, 'red'],
                            [0.55, 'orange'], [0.65, 'orange'],
                            [0.65, 'green'],  [0.80, 'green'],
                            [0.80, 'blue'], [1.00, 'skyblue']],
                #colorscale=["red", "orange", "yellow", "green"],
                hoverongaps = False)
            ],
            layout=
                go.Layout(
                xaxis=dict(ticks=''),
                yaxis=dict(ticks=''),
                font=dict(size=11),
                plot_bgcolor='whitesmoke',
                width=1300,
                height=600,
                autosize=False
                )
        )


        return figure

        #viewer.show(app)
