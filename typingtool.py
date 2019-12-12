from app import create_app, db
from app.models import User, Sortable
import os
import json

app = create_app()

with app.app_context():
    items = json.loads(os.getenv('SEG_INFO'))['Items']

    db.create_all()
    a = "+".join([str(i) for i in range(1, len(items)+1)]) #'1+2+3+4+5+6+7+8+9+10+11'
    b = Sortable(a)
    db.session.add(b)
    db.session.commit()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Sortable': Sortable}