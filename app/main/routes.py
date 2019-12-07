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