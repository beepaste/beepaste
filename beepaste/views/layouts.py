from pyramid_layout.layout import layout_config

@layout_config(name='main', template='templates/layouts/main.jinja2')
@layout_config(template='templates/layouts/main.jinja2')
class MainLayout():
    def __init__(self, context, request):
        self.request = request
        self.context = context
