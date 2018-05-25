import serial
import plotly.plotly as py
from plotly.graph_objs import *
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import State, Input, Output


app = dash.Dash(__name__)

server = app.server
app.scripts.config.serve_locally = True


# CSS Imports
external_css = ["https://codepen.io/chriddyp/pen/bWLwgP.css",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]


for css in external_css:
    app.css.append_css({"external_url": css})

app.layout = html.Div(
   [
        html.Div(
            id="container",
            style={"background-color": ""},
            children=[
                html.H2(
                    "Stepper Motor Control Panel",
                ),
                html.Img(
                    src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"
                )
            ],
            className="banner"
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Serial Monitor",
                                    style={"textAlign": "Center"},
                                    className="seven columns"
                                ),
                                daq.StopButton(
                                    id="start-stop",
                                    label="",
                                    className="five columns",
                                    n_clicks=0,
                                    style={"paddingTop": "3%",
                                           "display": "flex",
                                           "justify-content": "center",
                                           "align-items": "center"}
                                )
                            ],
                            className="row"
                        ),
                        html.Div(
                            [
                                dcc.Textarea(
                                    id="serial-response",
                                    placeholder='',
                                    value='',
                                    style={'width': '90%',
                                           'height': '500%'},
                                    disabled=True,
                                    rows=15,
                                ),
                            ],
                            style={"display": "flex",
                                   "justify-content": "center",
                                   "align-items": "center"}
                        ),
                        html.Br(),
                        html.Div(
                            id="mode-set",
                            children=[
                                html.H5(id='word',
                                        style={"textAlign": "center"})
                            ]
                        ),
                        html.Div(
                            [
                                daq.Knob(
                                    id="stepper-velocity",
                                    label="Velocity (Steps)",
                                    color="default",
                                    max=10000,
                                    min=0,
                                    value=0,
                                    size=75,
                                    scale={"interval": 2500},
                                    className="three columns",
                                    style={"marginLeft": "17%",
                                           "textAlign": "center"}
                                ),
                                daq.Knob(
                                    id="stepper-position",
                                    label="Position (Degree)",
                                    color="default",
                                    max=360,
                                    min=0,
                                    value=0,
                                    size=75,
                                    scale={"interval": 90},
                                    className="three columns",
                                    style={"marginLeft": "15%",
                                           "textAlign": "center"}
                                ),

                                daq.BooleanSwitch(
                                    id='switch-position',
                                    on=False,
                                    label="Position",
                                    vertical=True,
                                    labelPosition="top",
                                    disabled=True,
                                    color="default",
                                    className='two columns',
                                    style={"textAlign": "center"}
                                ),

                                daq.BooleanSwitch(
                                    id='switch-velocity',
                                    on=False,
                                    label="Velocity",
                                    vertical=True,
                                    color="default",
                                    labelPosition="top",
                                    disabled=True,
                                    className='two columns',
                                    style={"textAlign": "center",
                                           "paddingTop": "10%"}
                                )
                            ],
                            className="row"
                        )
                    ],
                    className="four columns",
                    style={"border-radius": "5px",
                           "border-width": "5px",
                           "border": "1px solid rgb(216, 216, 216)"
                           }
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Gauges",
                                    style={"textAlign": "center"}),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="position-gauge",
                                            className="six columns",
                                            style={"marginLeft": "13%", "display": "flex",
                                                   "justify-content": "right",
                                                   "align-items": "right"}
                                        )
                                    ],
                                    className="row",
                                    style={"border-radius": "1px",
                                           "border-width": "5px",
                                           "border-top": "1px solid rgb(216, 216, 216)",
                                           "marginBottom": "20%"
                                           }
                                ),
                                html.Div(
                                    [
                                        daq.Gauge(
                                            id="speed-gauge",
                                            showCurrentValue=True,
                                            units="Microsteps/Seconds",
                                            scale={"0": "Low",
                                                   "5": "Medium", "10": "High"},
                                            value=0,
                                            size=175,
                                            color="#FF5E5E",
                                            label="Speed",
                                            className="twelve columns",
                                            style={"marginTop": "10%",
                                                   "color": "#222"}
                                        )
                                    ],
                                    className="row",
                                    style={"border-radius": "1px",
                                           "border-width": "5px",
                                           "border-top": "1px solid rgb(216, 216, 216)"
                                           }
                                )
                            ],
                            style={"border-radius": "5px",
                                   "border-width": "5px",
                                   "border": "1px solid rgb(216, 216, 216)"
                                   }
                        ),
                    ],
                    className="four columns"
                ),
                html.Div(
                    [
                        html.H3(
                            "Start Settings",
                            style={"textAlign": "Center", "paddingBottom": "4.5%", "border-radius": "1px",
                                   "border-width": "5px",
                                   "border-bottom": "1px solid rgb(216, 216, 216)"
                                   }
                        ),
                        daq.ToggleSwitch(
                            id="pre-settings",
                            label=["Not Set", "Set"],
                            color="#FF5E5E",
                            size=32,
                            value=False,
                            style={"marginBottom": "1%",
                                   "paddingTop": "2%"}
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id='acceleration-set',
                                    placeholder='Acceleration',
                                    type='text',
                                    value='',
                                    className='six columns',
                                    style={"width": "35%",
                                           "marginLeft": "13.87%", "marginTop": "3%"}
                                ),
                                dcc.Input(
                                    id='address-set',
                                    placeholder='Address',
                                    type='text',
                                    value='',
                                    className='six columns',
                                    maxlength="1",
                                    style={"width": "35%",
                                           "marginTop": "3%"}
                                ),
                            ],
                            className="row"
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id='baudrate',
                                    placeholder='Baudrate',
                                    type='text',
                                    value='',
                                    className='six columns',
                                    style={"width": "35%",
                                           "marginLeft": "13.87%", "marginTop": "3%"}
                                ),
                                dcc.Input(
                                    id='com-port',
                                    placeholder='Port',
                                    type='text',
                                    value='',
                                    className='six columns',
                                    style={"width": "35%",
                                           "marginTop": "3%"}
                                ),
                            ],
                            className="row"
                        ),
                        html.H5("Motor Current",
                                style={"textAlign": "Center",
                                       "paddingTop": "2.5%", "marginBottom": "12%", "marginTop": "5%"}
                                ),
                        html.Div(
                            [
                                daq.Slider(
                                    id='motor-current',
                                    value=30,
                                    color="default",
                                    min=0,
                                    max=100,
                                    size=250,
                                    step=None,
                                    handleLabel={
                                        "showCurrentValue": 'True', "label": "VALUE"},
                                    marks={"0": "0", "10": '', "20": '', "30": "", "40": "",
                                           "50": "50", "60": "", "70": "", "80": "", "90": "", "100": "100"},
                                    targets={"80": {"showCurrentValue": "False",
                                                    "label": "WARNING", "color": "#685"}, "100": ""}
                                )
                            ],
                            style={"display": "flex",
                                   "justify-content": "center",
                                   "align-items": "center", "marginBottom": "12%"}
                        ),
                        html.H5(
                            "Hold Current",
                            style={"textAlign": "center",
                                   "marginBottom": "12%"}
                        ),
                        html.Div(
                            [
                                daq.Slider(
                                    id='hold-current',
                                    color="default",
                                    value=20,
                                    min=0,
                                    max=100,
                                    size=250,
                                    step=None,
                                    handleLabel={
                                        "showCurrentValue": 'True', "label": "VALUE"},
                                    marks={"0": "0", "10": '', "20": '', "30": "", "40": "",
                                           "50": "50", "60": "", "70": "", "80": "", "90": "", "100": "100"},
                                    targets={"80": {"showCurrentValue": "False",
                                                    "label": "WARNING", "color": "#685"}, "100": ""})
                            ],
                            style={"display": "flex",
                                   "justify-content": "center",
                                   "align-items": "center", "marginBottom": "12%"}
                        ),
                        html.H5(
                            "Step Size",
                            style={"textAlign": "Center",
                        "marginBottom": "12%"}
                        ),
                        html.Div(
                            [
                                daq.Slider(
                                    id='step-size',
                                    value=4,
                                    color="default",
                                    min=1,
                                    max=256,
                                    size=250,
                                    step=None,
                                    handleLabel={
                                        "showCurrentValue": 'True', "label": "VALUE"},
                                    marks={"1": "1", "2": '', "4": '', "8": "", "16": "",
                                           "32": "", "64": "", "128": "128", "256": "256"})
                            ],
                            style={"display": "flex",
                                   "justify-content": "center",
                                   "align-items": "center", "marginBottom": "12%"}
                        ),
                        html.Div(
                            [
                                daq.ColorPicker(
                                    id="color-picker",
                                    label="Color Picker",
                                    value=dict(hex="#000"),
                                    size=150,
                                    style={"border":"0px"}
                                )
                            ],
                            style={"border-radius": "1px",
                                   "border-width": "5px",
                                   "border-top": "1px solid rgb(216, 216, 216)",
                                   "paddingTop": "5%", "paddingBottom": "5%"
                                   }
                        )
                    ], 
                    className="four columns", 
                    style={"border-radius": "5px",
                           "border-width": "5px",
                           "border": "1px solid rgb(216, 216, 216)"
                    }
                )
            ], 
            className="row"
        ),
        # Placeholder Divs
        html.Div(
            [
                html.Div(id="div-one"),
                html.Div(id="div-two"),
                html.Div(id="div-three"),
                html.Div(id="div-four"),
                html.Div(id="com-value"),
                html.Div(id='color-return')
            ],
            style={"visibility": "hidden"}
            )
   ], 
    style={'padding': '0px 10px 10px 10px',
           'marginLeft': 'auto', 'marginRight': 'auto', "width": "1100",
           'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}
    )


# Global Variables Comport (optional)
@app.callback(
    Output('com-value', 'children'),
    [Input('com-port', 'value')])
def clean_data(com_port):
    com_port = "COM" + com_port
    return


# Enable Preset Settings
@app.callback(
    Output("div-one", 'children'),
    [Input("pre-settings", 'value')],
    [State('address-set', 'value'),
     State('motor-current', 'value'),
     State('hold-current', 'value'),
     State('step-size', 'value'),
     State('acceleration-set', 'value'),
     State('baudrate', 'value')])
def presetting_start(preset_switch, address, motor_current, hold_current, stepsize, accel_set, baud):
    if (baud != '') and (accel_set != '') and (address != '') and (preset_switch == True):
        response = "xff/0@"
        return response
    else:
        response = "Enable set. Set motor settings before using."
        return response

# Preset Switch Disable Power Button
@app.callback(
    Output("start-stop", 'disabled'),
    [Input("pre-settings", 'value')],
    [State('address-set', 'value'),
     State('acceleration-set', 'value'),
     State('baudrate', 'value'),
     State('com-port', 'value')
     ]
)
def presetting_enable_power(preset_switch, address, accel_set, baud, com):
    if (baud != '') and (accel_set != '') and (address != '') and (com != '') and (preset_switch == True):
        return False
    else:
        return True

# Stop Button Terminate
@app.callback(
    Output("div-two", 'children'),
    [Input("start-stop", "n_clicks")]
)
def start_terminate(stop):
    stopchange = stop % 2
    if stop >= 1:
        if stopchange == 0:
            response = "xff/0'"
        else:
            response = "xff/0B"

        return response
    else:
        response = 'Terminate commands and flush serial.'
        return response

# Enable Velocity
@app.callback(
    Output("switch-velocity", "disabled"),
    [Input("start-stop", "n_clicks")]
)
def enable_velocity(stop):
    if stop >= 1:
        return False
    else:
        return True

# Enable Position
@app.callback(
    Output("switch-position", "disabled"),
    [Input("start-stop", "n_clicks")]
)
def enable_position(stop):
    if stop >= 1:
        return False
    else:
        return True

# Velocity Knob Position
@app.callback(
    Output("div-three", "children"),
    [Input("stepper-velocity", "value"),
     Input("switch-velocity", "on")],
    [State("address-set", "value"),
     State("acceleration-set", "value"),
     State("switch-position", "on")]
     )
def velocity_mode(stepper_velo, switch_velo, address, acceleration, switch_position):
    if (switch_velo == True):
        step_velo = int(stepper_velo)
        if step_velo == 0 or step_velo == 5000:
            response = "xff/0B"
        else:
            response = 'Bring to 0 or 5000 for serial response.'
        return response
    else:
        response = 'Set velocity knob. Enable velocity.'
        return response

# Speed Gauge
@app.callback(
    Output("speed-gauge", "value"),
    [Input("stepper-velocity", "value")],
    [State("switch-velocity", "on")]
)
def speed_gauge(stepper_velo, switch_velo):
    if (switch_velo == True):
        step_velo = int(stepper_velo/1000)
        return step_velo

# Position Knob Position
@app.callback(
    Output("div-four", 'children'),
    [Input("switch-position", "on"),
     Input("stepper-position", "value")],
    [State("address-set", "value"),
     State("acceleration-set", "value"),
     State("stepper-velocity", "value"),
     State("step-size", 'value')]
)
def position_mode(switch_position, step_position, address, acceleration, step_velocity, step_size):

    if (switch_position == True):
        if step_position == 0 or step_position == 360:
            response = "xff/0@"
        else:
            response = "Bring to 0 or 360 for serial response."
        return response
    else:
        response = "Set velocity and position knobs. Enable position."
        return response

# Position Gauge
@app.callback(
    Output("position-gauge", "figure"),
    [Input("stepper-position", "value"),
     Input("color-return", "children")]
)
def position_gauge(stepper_position, colorful):

    trace = Scatterpolar(

        r=[0, 1],
        theta=[0, stepper_position],
        mode='lines',
        name='Figure',
        line=dict(
            color=colorful,
        )
    )

    layout = Layout(
        width=250,
        height=250,
        polar=dict(
            domain=dict(
                x=[0, 1],
                y=[0, 1]
            ),

        ),

        margin=Margin(
            t=80,
            b=20,
            r=0,
            l=0
        ),

        title="Position",
        font=dict(
            family='Arial, sans-serif;',
            size=10,
            color="#000"
        ),
        showlegend=False
    )

    return Figure(data=[trace], layout=layout)

# Color Picker
@app.callback(
    Output("step-size", "color"),
    [Input("color-picker", "value")]
)
def color_picker(color):
    return color['hex']


@app.callback(
    Output("stepper-velocity", "color"),
    [Input("color-picker", "value")]
)
def color_picker(color):
    return color['hex']


@app.callback(
    Output("stepper-position", "color"),
    [Input("color-picker", "value")]
)
def color_picker(color):
    return color['hex']


@app.callback(
    Output("switch-position", "color"),
    [Input("color-picker", "value")]
)
def color_picker(color):
    return color['hex']


@app.callback(
    Output("switch-velocity", "color"),
    [Input("color-picker", "value")]
)
def color_picker(color):
    return color['hex']


@app.callback(
    Output("speed-gauge", "color"),
    [Input("color-picker", "value")]
)
def color_picker(color):
    return color['hex']


@app.callback(
    Output("pre-settings", "color"),
    [Input("color-picker", "value")]
)
def color_picker(color):
    return color['hex']


@app.callback(
    Output("motor-current", "color"),
    [Input("color-picker", "value")]
)
def color_picker(color):
    return color['hex']


@app.callback(
    Output("hold-current", "color"),
    [Input("color-picker", "value")]
)
def color_picker(color):
    return color['hex']


@app.callback(
    Output("color-return", "children"),
    [Input("color-picker", "value")]
)
def color_picker(color):
    return color['hex']


@app.callback(
    Output("container", "style"),
    [Input("color-return", "children")]
)
def color_picker(color):
    style = {"background-color": ""}
    style["background-color"] = color
    return style

# Mode
@app.callback(
    Output("word", 'children'),
    [Input('switch-velocity', 'on'),
     Input('switch-position', 'on')]
)
def mode_set(switch_velo, switch_position):
    if (switch_position) == True and (switch_velo == True):
        mode = "Invalid Mode Set"
        return mode
    elif (switch_position == True):
        mode = "Position Mode Enabled"
        return mode
    elif (switch_velo == True):
        mode = "Velocity Mode Enabled"
        return mode
    else:
        mode = "No Mode Set"
        return mode


# Serial Monitor Response
@app.callback(
    Output("serial-response", "value"),
    [Input("div-one", "children"),
     Input("div-two", "children"),
     Input("div-three", "children"),
     Input("div-four", "children")]
)
def serial_monitor_response(div_one, div_two, div_three, div_four):
    #Div_one -> Response of pre-set
    #Div_two -> Response of stop button
    #Div_three -> Response of velocity 
    #Div_four -> Response of position

    read = (
        "---------------READ ME----------------\n" +
        "This Dash app was made for the Silverpak 17C stepper motor. " +
        "The motor driver has two modes: Position and Velocity. " +
        "Position mode controls the absolute location of the motor. " +
        "Velocity mode controls the speed of constant rotation of the motor. " +
        "The user can only be in either Position or Velocity mode at one time.\n\n\n")

    instructions = (
        "------------INSTRUCTIONS------------\n" +
        "1. Fill in input boxes and enable set. \n" +
        "2. Click stop to flush serial. \n" +
        "3. Enable position or velocity. \n" +
        "4.1 Turn velocity and positon knobs in position mode.\n"
        "4.2 Turn velocity knob in velocity mode.\n\n\n"
        "-----------SERIAL RESPONSE---------\n")

    one = "Preset: {} \n".format(div_one)
    two = "Stop: {} \n".format(div_two)
    three = "Velocity Mode: {} \n".format(div_three)
    four = "Position Mode: {} \n\n\n".format(div_four)

    reference = (
        "-------WHAT DOES IT MEAN??--------\n"
        "/0' indicates command terminated \n" +
        "/0@ indicates good command \n" +
        "/0C indicates command out of range \n" +
        "/0b indicates bad command \n")

    response = read + instructions + one + two + three + four + reference
    return response


if __name__ == '__main__':

    app.run_server(debug=True)
