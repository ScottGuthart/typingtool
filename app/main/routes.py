import pandas as pd
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import User, Sortable
from app.main import bp
from app.auth.confirm import check_confirmed
import os
import json
from app.main.graph import pie

import plotly

import pandas as pd
import numpy as np

info = json.loads(os.getenv('SEG_INFO'))
s_names = info['Segment Names']
s = info['Items']
coef = info['Coef']
t='?'

@bp.route('/index')
@bp.route('/')
@login_required
@check_confirmed
def index():
    sort = Sortable.query.filter_by(id=1).first()
    ordem = str(sort.data)

    return render_template('index.html', ordem=ordem, s=s, t=t)

@bp.route('/post', methods=['GET', 'POST'])
def post():
    json = request.json
    final = ("+".join(json))
    sort = Sortable.query.filter_by(id=1).first()
    sort.data = final
    db.session.commit()

    return str('')

@bp.route('/gettype', methods=['POST'])
def get_type():
    final = ("+".join(request.form['final'][1:-1].replace('"', "").split(",")))
    model = pd.DataFrame(coef)
    l = [int(c) for c in final.split('+')]
    print(l)
    l = pd.Series([l.index(i)+1 for i in range(1, len(l)+1)] + [1])
    seg = pd.Series([(l * model[col]).sum() for col in model]).idxmax()

    return jsonify({'Segment' : s_names[seg]})

@bp.route('/api/<order>')
def api(order):
    l = [int(c) for c in order.split('+')]
    if len(l)!= len(s) or len(set(l)) != len(l) or [i for i in range(1, len(l)+1) if i not in l]:
        return "Invalid submission"

    l = pd.Series([l.index(i)+1 for i in range(1, len(l)+1)] + [1])
    model = pd.DataFrame(coef)
    seg = pd.Series([(l * model[col]).sum() for col in model]).idxmax()
    return str(seg+1)

@bp.route('/graph')
@login_required
@check_confirmed
def graph():
    graphs = []
    dogs_owned = {
        'One Dog': 67,
        'Two Dogs': 26,
        'Three Dogs': 7
    }
    past_owner = {
        'First Time': 15,
        'Past Owner': 85
    }
    graphs.append(pie(dogs_owned))
    graphs.append(pie(past_owner, inner_radius=.5))
    return render_template("graph.html", graphs=graphs)

@bp.route('/plotly')
@login_required
@check_confirmed
def plotly_graph():
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)
    colors = ["#7fc97f",
                "#beaed4",
                "#fdc086",
                "#ffff99",
                "#386cb0",
                "#f0027f"]
    graphs = [
        dict(
            data=[
                dict(
                    labels=['Own One Dog', 'Own Two Dogs', ' Own Three Dogs'],
                    values=[67, 26, 7],
                    type='pie',
                    textposition="inside",
                    textinfo="percent+label",
                    hole=0,
                    textfont={
                        "size":24,
                        "family":"Overpass"
                    },
                    marker= {
                        "colors": colors
                    },
                    hoverinfo='skip',
                    pull=[0,0,0.1]
                ),
            ],
            layout=dict(
                autosize=True,
                #automargin=True,
                font={
                    "size":16,
                    "family":"Overpass"
                },
                title=None,
                showlegend=False,
                margin={
                    "l":10,
                    "t":10,
                    "r":10,
                    "b":10
                },
            ),
        ),

        dict(
            data=[
                dict(
                    labels=['First Time Owner', 'Past Owner'],
                    values=[85, 15],
                    type='pie',
                    textposition="inside",
                    textinfo="percent+label",
                    hole=0.5,
                    textfont={
                        "size":24,
                        "family":"Overpass"
                    },
                    marker= {
                        "colors": colors[::-1]
                    },
                    hoverinfo='skip',
                    pull = [0,0.1]
                ),
            ],
            layout=dict(
                font={
                    "size":16,
                    "family":"Overpass"
                },
                margin={
                    "l":10,
                    "t":10,
                    "r":10,
                    "b":10
                },
                #title=,
                showlegend=False,
            ),
        ),

        dict(
            data=[
                dict(
                    x=['Yorkie', 'Lab', 'Boxer', 'Golden', 'Husky'],  # Can use the pandas data structures directly
                    y=[.06,.15,.05,.07,.03],
                    type='bar',           
                    textfont={
                        "size":24,
                        "family":"Overpass"
                    },
                    marker= {
                        "opacity":0.8,
                        "color":colors,
                    },
                    hoverinfo='y',
                )
            ],
            layout=dict(
                yaxis={
                    "tickformat":',.0%'
                }
            )
        )
    ]
    graphs = [graphs[0], graphs[2], graphs[1]]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('plotly.html',
                           ids=ids,
                           graphJSON=graphJSON)