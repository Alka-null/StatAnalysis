from msvcrt import kbhit
from flask import Flask, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd

import base64
from io import BytesIO

# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)

yticks={}
j=3
k=0
fig = Figure(figsize=(10,10))
ax = fig.subplots(j)

df = pd.read_csv('C:\\Users\\Esang Ekarika\\Desktop\\Data Gada\\b9.csv')

# Create a new column with index values
df['saveindex'] = df.index
df['static'] = 1
print(df)

i=1
def prisor(x):
    global i
    global k
    global fig
    global ax
    print(i)
    #print(x)
    print('x.size is')
    print(x.size)
    print(len(x.index))
    x.sort_values(by=['saveindex'], ascending=False)
    x.loc[:,'static']=i
    x['xaxis']=range(len(x.index))
    print("x['xaxis']")
    print(x['xaxis'])
    #x['static']= i
    print(x['static'])

    conditions = [
    x['TeamWinOutcome'].eq(1),
    x['TeamWinOutcome']!= 1,
    ]

    choices = [i,'NA']
    
    x['XWin'] = np.select(conditions, choices, default=0)
    print("x['XWin']")
    print(x['XWin'])

    #Team draw
    conditions = [
    x['TeamWinOutcome'].eq(0),
    x['TeamWinOutcome']!= 0,
    ]

    choices = [i,'NA']
    
    x['XDraw'] = np.select(conditions, choices, default=0)

    #Team Lose
    conditions = [
    x['TeamWinOutcome'].eq(2),
    x['TeamWinOutcome']!= 2,
    ]

    choices = [i,'NA']
    
    x['XLose'] = np.select(conditions, choices, default=0)


    #Colors
    conditions = [
    x['TeamWinOutcome'].eq(2),
    x['TeamWinOutcome'].eq(1),
    x['TeamWinOutcome'].eq(0),
    ]

    Colorchoices = ["red", 'green','grey']
    
    x['Colors'] = np.select(conditions, Colorchoices, default=0)
    print(x)

    global yticks
    yticks[i] = x.name
    ax[1].scatter(x['xaxis'], x['static'], c=x['Colors'])

    #ax.figure(figsize=(10,6))
    ax[0].scatter(x['xaxis'], x['XWin'], color='green')
    k+=1
    ax[0].scatter(x['xaxis'], x['XDraw'], color='grey')
    k+=1
    ax[0].scatter(x['xaxis'], x['XLose'], color='red')
    k+=1

    i+=1
    return x

def awayswitchwinoutcome(x):
    conditions = [
    x['WinOutcome'].eq(2),
    x['WinOutcome'].eq(1),
    x['WinOutcome'].eq(0),
    ]

    choices = [1, 2, 0]
    
    x['TeamWinOutcome'] = np.select(conditions, choices, default=0)

    return x

def homeswitchwinoutcome(x):
    conditions = [
    x['WinOutcome'].eq(2),
    x['WinOutcome'].eq(1),
    x['WinOutcome'].eq(0),
    ]

    choices = [2, 1, 0]
    
    x['TeamWinOutcome'] = np.select(conditions, choices, default=0)

    return x

homewindf = df.groupby("Home", group_keys=False).apply(lambda x: homeswitchwinoutcome(x)).rename(columns={'Home':'Team'})[['Team', 'WinOutcome','TeamWinOutcome' ,'saveindex','static']]
#homewindf = df.groupby("Home").apply(lambda x: x).rename(columns={'Home':'Team'})[['Team', 'WinOutcome', 'saveindex']]
print('homewindf%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
print(homewindf)
#independenthomedf = [homewindf.get_group(x) for x in homewindf.groups]

awaywindf = df.groupby("Away", group_keys=False).apply(lambda x: awayswitchwinoutcome(x)).rename(columns={'Away':'Team'})[['Team', 'WinOutcome','TeamWinOutcome' ,'saveindex', 'static']]
#independentawaydf = [awaywindf.get_group(x) for x in awaywindf.groups]

#teamwin = pd.concat(homewindf, awaywindf)
teamwin = pd.concat([homewindf, awaywindf]).groupby("Team", group_keys=True).apply(lambda x: prisor(x))
#teamwin['static']= teamwin.ngroup() 
print('teamwin$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
print(teamwin)
print('teamwin.size()')
print(teamwin.size)
#seperateteamsdf= [teamwin.get_group(x) for x in teamwin.groups]

#ax[1].axes.set_yticks([1,2,3,4], minor=False)
ax[1].axes.set_yticks(list(yticks.keys()), minor=False)
print('yticks.values()')
print(yticks.values())
keys=yticks.keys()
values = (yticks[key] for key in keys)
#ax[1].axes.set_yticklabels(['a','b','c','d'], fontdict=None, minor=False)
ax[1].axes.set_yticklabels(list(yticks.values()), fontdict=None, minor=False)

pivoteddata  = teamwin.pivot(index='xaxis', columns='Team', values='static')
print('pivoteddata########################################################')
print(pivoteddata)
#print(seperateteamsdf)
# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

@app.route('/')
@app.route('/hello')
def hello():
    #teamwin.plot(kind="bar")
    # Generate the figure **without using pyplot**.
    #fig = Figure()
    #ax = fig.subplots(2)
    #ax[0].scatter(pivoteddata.index, pivoteddata['VfL Wolfsburg'])
    #ax[1].plot(teamwin['Team'], teamwin['WinOutcome'])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
    # Render the page
    return "Hello Python!"


if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)
