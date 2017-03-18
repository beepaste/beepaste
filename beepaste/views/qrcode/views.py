from pyramid.response import Response
from pyramid.view import view_config
from qrcode import *

@view_config(route_name='qrcode')
def qrcode(request):
    uri = request.matchdict['uri']
    qr = QRCode(version=3, error_correction=ERROR_CORRECT_L)
    qr.add_data(request.route_url('view_paste', pasteID=uri))
    qr.make() # Generate the QRCode itself
    # im contains a PIL.Image.Image object
    im = qr.make_image()
    resp = Response()
    resp.status_int = 200
    resp.content_type = "image/png"
    im.save(resp.body_file, 'PNG')
    return resp
