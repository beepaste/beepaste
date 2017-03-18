from pyramid.response import Response
from pyramid.view import view_config, view_defaults
import beepaste.pasteFunctions as func
from beepaste.selectOptions import languagesList
from beepaste.models.api import API
import json
import base64
from beepaste.models.pastes import Pastes

def verifyKey(apikey, request):
    api_count = request.dbsession.query(API).filter_by(apikey=apikey).count()
    if api_count == 0:
        return {'error': 'api-key is not valid.'}

@view_config(
                route_name='api_intro',
                request_method='GET',
                renderer='templates/apiView.jinja2'
        )
def apiIntro(request):
    title = 'API' + " - " + request.registry.settings['beepaste.siteName']
    description = '''Here is the rest-ful api! With this api you can create or
                get pastes in beepaste! For more information on how to
                work with API and for samples please visit the link.'''
    samples = {}
    samples['create'] = '''import requests
data = {'api-key': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'pasteRaw': 'some text!', 'pasteLanguage': 'text'}
r = requests.post(\'''' + request.route_url('api_post') + '''\', json=data)'''
    samples['get'] = '''import requests
r = requests.get(\'''' + request.route_url('api_get', pasteid='AAAAAA') + '''\')'''
    return {'title': title, 'description': description, 'samples': samples}


@view_config(
        route_name='api_get',
        request_method='GET',
        renderer='json',
        )
def get_api(request):
    pasteid = request.matchdict['pasteid']
    paste = func.getPaste(pasteid, request)

    if paste:
        retData = {}
        retData['url'] = request.route_url(
                                            'view_paste',
                                            pasteID=paste.pasteURI)
        retData['pasteTitle'] = paste.title
        retData['pasteAuthor'] = paste.name
        retData['pasteLanguage'] = paste.lang
        retData['pasteRaw'] = base64.b64decode(paste.text).decode('utf-8')
        retData['pasteEncryption'] = paste.encryption
        retData['shortURL'] = paste.shortURL

        resp = Response()
        resp.status_int = 200
        resp.json = retData
        return resp
    else:
        resp = Response()
        resp.status_int = 404
        retData = {'error':'paste not found.'}
        resp.json = retData
        return resp


@view_config(
        route_name='api_post',
        request_method='POST',
        renderer='json',
        )
def post_api(request):
    try:
        data = request.json_body
    except:
        resp = Response()
        resp.status_int = 409
        retData = {"error":"invalid request"}
        resp.json = retData
        return resp

    try:
        if data:
            apikey = func.fetchData(data, 'api-key')
            verifyKey(apikey, request)

            pasteRaw = func.fetchData(data, 'pasteRaw')
            data['pasteRaw'] = base64.b64encode(pasteRaw.encode('utf-8')).decode('utf-8')

            pasteLanguage = func.fetchData(data, 'pasteLanguage')
            func.verifyLanguage(pasteLanguage)

            pasteTitle = func.fetchData(data, 'pasteTitle', False)
            if pasteTitle:
                func.verifyTitleAndAuthor(pasteTitle)
            else:
                data['pasteTitle'] = pasteTitle

            pasteAuthor = func.fetchData(data, 'pasteAuthor', False)
            if pasteAuthor:
                func.verifyTitleAndAuthor(pasteAuthor)
            else:
                data['pasteAuthor'] = pasteAuthor

            pasteExpire = func.fetchData(data, 'pasteExpire', False)
            if pasteExpire:
                func.verifyExpire(pasteExpire)
            else:
                data['pasteExpire'] = "0"

            pasteEncryption = func.fetchData(data, 'pasteEncryption', False)
            if pasteEncryption:
                func.verifyEncryption(pasteEncryption)
            else:
                data['pasteEncryption'] = pasteEncryption

            newPasteURI = func.createPasteFromData(data, request)

            retData = {}
            retData['url'] = request.route_url('view_paste', pasteID=newPasteURI)

            resp = Response()
            resp.status_int = 201
            resp.json = retData
            return resp
    except Exception as e:
        resp = Response()
        resp.status_int = 409
        retData = {'error': str(e)}
        resp.json = retData
        return resp


@view_config(route_name='api_langs')
def apiLang(request):
    retData = {}
    retData['pasteLanguages'] = languagesList

    resp = Response()
    resp.status_int = 200
    resp.json = retData

    return resp
