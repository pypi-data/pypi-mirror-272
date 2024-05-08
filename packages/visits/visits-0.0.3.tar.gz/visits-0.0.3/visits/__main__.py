#!/usr/bin/env python3

import sys

from terbilang import Terbilang
from tremolo import Tremolo
from tremolo_session import Session

t = Terbilang()
app = Tremolo()

# this is a session middleware
# that enables you to use context.session or request.context.session
Session(app, expires=86400)


@app.route('/')
async def index(request=None, **server):
    session = request.context.session

    if session is None:
        return b'The session will be created after you reload this page.'

    if 'visits' in session:
        session['visits'] += 1
    else:
        session['visits'] = 0

    return '<h2>%d (%s)</h2>' % (session['visits'],
                                t.parse(session['visits']).getresult())

if __name__ == '__main__':
    PORT = 8000

    try:
        PORT = int(sys.argv[1])
    except (IndexError, ValueError):
        pass

    app.run('::', PORT, debug=True, reload=True)
