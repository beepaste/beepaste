from pyramid.response import Response
from pyramid.view import view_config
from beepaste.models.pastes import Pastes
from beepaste.pasteFunctions import pasteExists
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
import base64, datetime

@view_config(route_name='schedeuled_remove')
def viewPaste(request):
    cronkey = request.matchdict['cronkey']
    if cronkey != request.registry.settings['beepaste.cronkey']:
        resp = Response()
        resp.status_int = 409
        resp.text = "invalid cron-key"

        return resp

    try:
        cur = datetime.datetime.utcnow()
        pastes = request.dbsession.query(Pastes).filter(Pastes.expire <= cur).filter(Pastes.toexpire == True).delete()

        resp = Response()
        resp.status_int = 200
        resp.text = "done!"
    except:
        resp = Response()
        resp.status_int = 409
        resp.text = "some error occured"

    return resp
