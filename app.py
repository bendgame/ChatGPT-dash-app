#import dependencies
from dash import Dash, dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from openaikey import apikey
import openai


# Load your API key from an environment variable or secret management service
openai.api_key = apikey

def system_prompts():
    return  html.Div([
             html.H3('Select your writing genre:')
             , dbc.Row([
                dbc.Col(
                    dcc.Dropdown(id = 'sys-prompt', options=['Academic Essay', 'Horror Story', 'Romance Novel']
                    , value='Academic Essay')
                , width=4)#end col 1
             , dbc.Col(
                    html.P('Sets the system level prompt to improve the style of the output.')
                    , width=6
                    )#end col 2          
             ])#end row 
         ])#end div

def output_style():
    return  html.Div([
             html.H3('Select your output style:')
             , dbc.Row([
                dbc.Col(
                    dcc.Dropdown(id = 'output-style', options=['Outline', 'Paragraph', 'List']
                    , value='Outline')
                , width=4)#end col 1
             , dbc.Col(
                    html.P('Sets the style of output returned (outline, paragraph, or list)')
                    , width=6
                    )#end col 2          
             ])#end row 
         ])#end div

def text_areas():
    return html.Div([ 
            html.H3('Enter your prompt:')
            , dbc.Textarea(id = 'my-input'
                , size="lg"
                , placeholder="Enter your text")
            , dbc.Button("Generate Text"
                , id="gen-button"
                , className="me-2"
                , n_clicks=0)
            ])

#instantiate dash
app = Dash(__name__
, external_stylesheets=[dbc.themes.SOLAR]
)#create layout

app.layout = html.Div([
        dbc.Container([
            html.H1('ChatGPT Writing Assitant')
            , html.Br()
            , system_prompts()
            , html.Br()
            , output_style()
            , html.Br()
            , text_areas()
            , html.Br()
            , html.H3('Output:')
            , html.Div(id='my-output')
        ]) #end container
  ]) #end div

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='gen-button', component_property='n_clicks'),
    Input(component_id='sys-prompt', component_property='value'),
    Input(component_id='output-style', component_property='value'),
    State(component_id='my-input', component_property='value')    
)
def update_output_div(gen, sp, os, input_value):
    #print(input_value) #debug
    
    #set text to sample
    text = "This is a \nsample"
    
    #listen for button clicks
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    #create system prompt logic
    if sp == 'Academic Essay':
        system_prompt = 'You are a world class academic professor and a world class technical writer that wants to produce coherent academic essays. Produce content step by step.'
    elif sp == 'Horror Story':
        system_prompt = 'You are a world class horror author with a style similar to Stephen King and Anne Rice. Generate content that contains logical twists and builds suspense. Produce content step by step.'
    else:
        system_prompt = 'You are a world class romance novelist with a style similar to Nora Roberts and Jane Austen. Generate content that is tantilizing, lustrious, and very erotic. Produce content step by step.'

   #create output style logic 
    if os == 'Outline':
        style = 'Respond with an outline no longer than 500 words'
    elif os == 'Paragraph':
        style = 'Respond with at least one paragraph. Output at least 200 words.'
    else:
        style = 'Respond with a top 15 list. Output is limited to 150 words.'
    
    #build messages payload
    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": style},
            {"role": "assistant", "content": "On what topic?"},
            {"role": "user", "content": input_value}
        ]

    
    #button logic to submit to chatGPT API
    if 'gen-button' in changed_id:
        print(input_value)
        if input_value is None or input_value == "":
            input_value = ""
            text = html.P('hello <br> this is </br> a <br> test ')

        else:
            print(input_value)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature = 0.8,
                top_p = 1, 
                presence_penalty = 0.5,
                frequency_penalty = 0.4            
            )
            text = (response['choices'][0]['message']['content'])

    return html.P(text, style = {'white-space': 'pre-wrap'})

#run app server
if __name__ == '__main__':
    app.run_server(debug=True)
