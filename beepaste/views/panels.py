from pyramid_layout.panel import panel_config
from pyramid.view import view_config
from os.path import join
from beepaste.paths import base
from ..models.users import Users
import datetime
import json

@panel_config(name='navbar', renderer='templates/panels/navbar.jinja2')
def navbar(context, request):
    return {}

@panel_config(name='footer', renderer='templates/panels/footer.jinja2')
def footer(context, request):
    year = datetime.datetime.now().year
    version = request.registry.settings['beepaste.version']
    return {'version': version, 'year': year}


@panel_config(name='menu', renderer='templates/panels/menu.jinja2')
def menu(context, request):
    def nav_item(name, path, items=[]):
        active = any([item['active'] for item in items]) if items else request.path == path

        item = dict(
            name=name,
            path=path,
            active=active,
            items=items
            )

        return item

    items = []
    # items.append(nav_item('resume', '#', [nav_item(name, request.route_path(name)) for name in ['resume_list','resume_edit']]))
    items.append(nav_item('<i class="fa fa-plus-circle" aria-hidden="true"></i> Create Paste', request.route_path('home')))
    items.append(nav_item('<i class="fa fa-cogs" aria-hidden="true"></i> API', request.route_path('api_intro')))
    items.append(nav_item('<i class="fa fa-info" aria-hidden="true"></i> About Us', request.route_path('about')))
    return {'items': items}

@panel_config(name='authors', renderer='templates/panels/authors.jinja2')
def authors(context, request):
    def authorItems(name, img, about, social):
        #item = dict(name = name, about = about, img = img, social = social)
        item = {'name': name, 'about': about, 'img': img, 'social': social}
        return item

    with open(join(base, 'AUTHORS.txt')) as f:
        content = f.read()
        items = json.loads(content)
    return {'items': items}
