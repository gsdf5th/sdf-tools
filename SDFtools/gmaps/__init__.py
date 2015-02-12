__author__ = 'kwhatcher'



from werkzeug.local import LocalProxy


class Gmap(object):

    def __init__(self, app):
        if app is not None:
            self.init_app(app)

    def init_app(self, app, *args, **kwargs):
        app.context_processor(Gmap.gmap_context_processor)

        self.app = app
        if not hasattr(app, 'extensions'):
            app.extensions = {}




    @staticmethod
    def gmap():
        """Backend function for weather proxy

        :return: A list of weather items
        """
        # Construct weather
        gmap_key= "AIzaSyCaj3O8v3HR2ZmDxQClYaiQ0JnhWg8gPKQ"

        return gmap_key

    @staticmethod
    def gmap_context_processor():
        """add variable ''weather'' to template context

        It contains the list of weather entries to render as a widget
        """

        return dict(gmapkey=gmap_key)





#: A proxy for current weather list.
gmap_key = LocalProxy(Gmap.gmap)