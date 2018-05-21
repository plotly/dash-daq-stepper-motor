import serial
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import State, Input, Output


app = dash.Dash(__name__)
server = app.server

app.scripts.config.serve_locally = True
#app.css.config.serve_locally = True


# CSS Imports
external_css = ["https://codepen.io/chriddyp/pen/bWLwgP.css",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]


for css in external_css:
    app.css.append_css({"external_url": css})

#ser = serial.Serial('COM21')
# ser.Serial('COM21')


# def defaultset():
#     ser.bytesize = 8
#     ser.parity = 'N'
#     ser.stopbits = 1
#     ser.timeout = None
#     ser.xonxoff = 0
#     ser.rtscts = 0
#     ser.dsrdtr = False
#     ser.writeTimeout = 0


app.layout = html.Div([

    # Header Banner
    html.Div([
        html.H2("Stepper Motor Control Panel"),
        html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"),
    ], className='banner'),

    # First Box
    html.Div([
        # Second Box
        # Serial Monitor
        html.Div([
            html.H3("Serial Monitor",
                    style={"textAlign": "Left"}),


            dcc.Textarea(
                id="serial-response",
                placeholder='',
                value='',
                style={'width': '100%', 'height': '500%'},
                disabled=True,
                rows=10,
            ),
            # Third Box
            # Velocity and Position Knobs
            html.Div([
                html.Div([
                    daq.Knob(
                        id="stepper-velocity",
                        label="Velocity (Steps)",
                        max=10000,
                        min=0,
                        value=0,
                        size=120,
                        scale=1)
                ], className="three columns"),

                html.Div([
                    daq.Knob(
                        id="stepper-position",
                        label="Position (Degree)",
                        max=360,
                        min=0,
                        value=0,
                        scale=1,
                        size=120,
                        className="three columns offset-by-two"
                    ),


                ], className="one columns offset-by-two"),

                # Power Button Velo Switch and Pos Switch
                html.Div([
                    daq.PowerButton(
                        id="start-stop",
                        label="On/Off",
                        on=False,
                        disabled=True,
                        className="one columns offset-by-four",
                        style={"paddingTop": "15%"}
                    ),

                    daq.BooleanSwitch(
                        id='switch-position',
                        on=False,
                        label="Position Mode",
                        vertical=True,
                        labelPosition="top",
                        disabled=True,
                        className='three columns offset-by-one',
                        style={"paddingTop": "15%", "textAlign": "center"}
                    ),

                    daq.BooleanSwitch(
                        id='switch-velocity',
                        on=False,
                        label="Velocity Mode",
                        vertical=True,
                        labelPosition="top",
                        disabled=True,
                        className='three columns',
                        style={"paddingTop": "15%", "textAlign": "center"}

                    ),
                ], className="six columns"),


            ], className="row"),
        ],  className="five columns"),

        # Speed Gauge
        # Second Box
        html.Div([
            daq.Gauge(
                id="speed-gauge",
                showCurrentValue=True,
                units="Microsteps/Seconds",
                scale={"0": "Low", "5": "Medium", "10": "High"},
                value=0,
                size=240,
                color="#FF5E5E",
                label="Speed",
                style={"paddingRight": "10%", "paddingTop": "10%"}
            )], className="three columns"),

        # Second Box
        # Start Settings Switch
        html.Div([
            # Third Box
            html.Div([
                # Fourth Box
                html.Div([
                    html.H3("Start Settings",
                            style={"textAlign": "Left", "paddingLeft": "5%"}),

                    daq.ToggleSwitch(
                        id="pre-settings",
                        label=["Not Set", "Set"],
                        color="#FF5E5E",
                        size=32,
                        value=False,
                        style={"marginLeft": "4%", "marginBottom": "1%"},

                        className="nine columns"
                    )], className="four columns"),
            ]),
            # Fourth Box
            html.Div([
                # Fifth Box
                # Input Settings Boxes
                html.Div([
                    dcc.Input(
                        id='acceleration-set',
                        placeholder='Acceleration',
                        type='text',
                        value='300',
                        className='three columns',
                        style={"width": "30%", "marginLeft": "4.87%"}
                    ),

                    dcc.Input(
                        id='address-set',
                        placeholder='Address',
                        type='text',
                        value='1',
                        className='three columns',
                        maxlength="1",
                        style={"width": "30%"}
                    ),

                    dcc.Input(
                        id='baudrate',
                        placeholder='Baudrate',
                        type='text',
                        value='9600',
                        className='three columns',
                        style={"width": "30%", "marginTop": "3%",
                               "marginLeft": "5%"}
                    ),

                    dcc.Input(
                        id='com-port',
                        placeholder='Comport',
                        type='text',
                        value='21',
                        className='three columns',
                        style={"width": "30%",  "marginTop": "3%"}
                    ),

                ], className="four columns")
            ]),
            # Fourth Box

            # Sliders
            html.Div([
                # Fifth Box
                html.Div([
                     html.H5("Motor Current",
                             style={"textAlign": "Left"}),
                     daq.Slider(
                         id='motor-current',
                         value=30,
                         min=0,
                         max=100,
                         size=550,
                         step=1,
                         handleLabel={
                             "showCurrentValue": 'True', "label": "VALUE"},
                         marks={"0": "0", "100": "100", "50": "50"},
                         targets={"80": {"showCurrentValue": "False",
                                         "label": "WARNING", "color": "#685"}, "100": ""},
                         className='six columns'
                     ),

                     ], className="four columns column", style={"paddingLeft": "4%", "marginTop": "1.5%"}),
                # Fifth Box
                html.Div([
                    html.H5("Hold Current",
                            style={"textAlign": "Left"}),
                    daq.Slider(
                        id='hold-current',
                        value=20,
                        min=0,
                        max=100,
                        size=550,
                        step=1,
                        handleLabel={
                            "showCurrentValue": 'True', "label": "VALUE"},
                        marks={"0": "0", "100": "100", "50": "50"},
                        targets={"80": {"showCurrentValue": "False",
                                        "label": "WARNING", "color": "#685"}, "100": ""},
                        className='six columns'
                    )], className="four columns", style={"marginTop": "1.5%"}),

                # Fifth Box
                html.Div([
                    html.H5("Step Size",
                            style={"textAlign": "Left"}),
                    daq.Slider(
                        id='step-size',
                        value=4,
                        min=1,
                        max=256,
                        size=550,
                        step=None,
                        handleLabel={
                            "showCurrentValue": 'True', "label": "VALUE"},
                        marks={"1": "1", "2": '', "4": '', "8": "", "16": "",
                               "32": "", "64": "", "128": "", "256": "256"},
                        className='six columns'
                    )], className="four columns", style={"marginTop": "1.5%"}),
                # classname
            ]),
        ]),
    ], style={"marginLeft": "10%", "marginRight": "auto"}),

    html.Div([
        html.Div(id='div-one'),
        html.Div(id="div-two"),
        html.Div(id="div-three"),
        html.Div(id="div-four"),
        html.Div(id="intermediate-value")
    ],  style={"visibility": "hidden"})

], style={'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})


# Global Variables

# @app.callback(
#     Output('intermediate-value', 'children'),
#     [Input('baudrate', 'value')])
# def clean_data(baudrate):

#      cleaned_df = baudrate
#      return cleaned_df.to_json(date_format='iso', orient='split')

@app.callback(
    Output('intermediate-value', 'children'),
    [Input('com-port', 'value')])
def clean_data(com_port):
    com_port = "COM" + com_port
    return com_port


# Enable Preset Settings
@app.callback(
    Output("div-one", 'children'),
    [Input("pre-settings", 'value')],
    [State('address-set', 'value'),
     State('motor-current', 'value'),
     State('hold-current', 'value'),
     State('step-size', 'value'),
     State('acceleration-set', 'value'),
     State('baudrate', 'value'),
     State('intermediate-value', 'children')
     ])
def presetting_start(preset_switch, address, motor_current, hold_current, stepsize, accel_set, baud, com):
    if ((baud != '') and (accel_set != '') and (address != '') and (preset_switch == True)):

        ser = serial.Serial(com)
        ser.bytesize = 8
        ser.parity = 'N'
        ser.stopbits = 1
        ser.timeout = None
        ser.xonxoff = 0
        ser.rtscts = 0
        ser.dsrdtr = False
        ser.writeTimeout = 0
        ser.baudrate = baud

        command = "/{}m{}h{}j{}L{}RR\r".format(
            address, motor_current, hold_current, stepsize, accel_set)
        print(command)
        ser.flush()

        ser.write(command.encode("utf-8"))

        response = str(ser.read(7))
        return response
    else:
        response = "Press set to enable motor settings."
        return response


# @app.callback(Output('graph', 'figure'),
# [Input('intermediate-value', 'children')])
# def update_graph(jsonified_cleaned_data):

#     # more generally, this line would be
#     baud = json.loads(jsonified_cleaned_data)
#     return baud

# Preset Switch Disable Power Button
@app.callback(
    Output("start-stop", 'disabled'),
    [Input("pre-settings", 'value')]
)
def presetting_enable_power(pre_setting_switch):
    if pre_setting_switch == True:
        return False
    else:
        return True

# Power Button Terminate Edit


@app.callback(
    Output("div-two", 'children'),
    [Input("start-stop", "on")],
    [State('intermediate-value', 'children')]
)
def start_terminate(power_button, com):
    #ser = serial.Serial(com)
    if power_button == False:
        #ser.flush()
        term = "/1TRR\r".encode('utf-8')
        #ser.write(term)

        #response = str(ser.read(7))
        return #response
    else:
        #response = 'Press off to terminate current command and flush serial.'
        return #response

#Enable Velocity


@app.callback(
    Output("switch-velocity", "disabled"),
    [Input("start-stop", "on")]
)
def enable_velocity(start_stop):
    if start_stop == True:
        return False
    else:
        return True

# Enable Position


@app.callback(
    Output("switch-position", "disabled"),
    [Input("start-stop", "on")]
)
def enable_position(start_stop):
    if start_stop == True:
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
     State("switch-position", "on"),
     State('intermediate-value', 'children')])
# Modify to pps
def velocity_mode(stepper_velo, switch_velo, address, acceleration, switch_position, com):

    if (switch_velo == True):
        ser = serial.Serial(com)
        step_velo = int(stepper_velo)

        velo = "/{}V{}L{}P0RR\r".format(address, step_velo, acceleration)
        print(velo)
        ser.write(velo.encode("utf-8"))

        if step_velo == 0 or step_velo == 5000:
            response = str(ser.read(7))
        else:
            response = 'Bring to 0 or 5000 to see response.'
        return response
    else:
        response = 'Set velocity and bring to 0 or 5000 to see response.'
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
     State("step-size", 'value'),
     State("switch-velocity", "on"),
     State('intermediate-value', 'children')])
def position_mode(switch_position, step_position, address, acceleration, step_velocity, step_size, velocity_position, com):

    if (switch_position == True):
        ser = serial.Serial(com)
        step_velocity = int(step_velocity)
        step_position = int(step_position)
        step_pos = int(step_position * (200*(step_size))/360)

        velo = "/{}V{}L{}A{}RR\r".format(address, step_velocity, acceleration, step_pos)
        ser.write(velo.encode("utf-8"))

        print(velo)

        if step_position == 0 or step_position == 360:
            response = str(ser.read(7))
        else:
            response = "Bring to 0 or 360 to see response."
        return response
    else:
        response = "Set velocity and bring to 0 or 360 to see response."
        return response


# Serial Monitor Response

@app.callback(
    Output("serial-response", "value"),
    [Input("div-one", "children"),
     Input("div-two", "children"),
     Input("div-three", "children"),
     Input("div-four", "children")]
)
def serial_monitor_response(div_one, div_two, div_three, div_four):

    one = "Preset: {} \n".format(div_one)
    two = "On/Off: {} \n".format(div_two)
    three = "Velocity: {} \n".format(div_three)
    four = "Position: {} \n\n\n".format(div_four)

    reference = "/0' indicates that the command is terminated \n" + "/0@ indicates good command and that it was received correctly \n" + "/0C indicates that the command is out of range \n" + "/0b indicates bad command \n"

    response = one + two + three + four + reference
    return response


if __name__ == '__main__':
    # ser = serial.Serial("COM21")
    # defaultset()

    app.run_server(debug=False)
