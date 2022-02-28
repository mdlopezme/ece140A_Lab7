from wsgiref.simple_server import make_server
from pyramid.response import Response, FileResponse
from pyramid.config import Configurator
import threading

class Webserver():
    def __init__(self, root_path):
        # Temp to make it work nice with our systems
        self.root_path = root_path
        self.pub_path = self.root_path + '/public'
        self.img_path = self.pub_path + '/images'

        with Configurator() as config:
            # Add routes
            config.add_route('home', '/')

            # Creates views for routes
            config.add_view(self.get_home, route_name='home')

            # Create static routes
            config.add_static_view(name='/', path=self.img_path, cache_max_age=3600)

            app = config.make_wsgi_app()

        self.server = make_server('localhost', 6543, app)

    def start(self):
        print('Web server started on: http://localhost:6543')
        self.server_thread=threading.Thread(target=self.server.serve_forever,name="Web Server")
        self.server_thread.start()

    def stop(self):
        print("Ending web server")
        self.server.shutdown()
    
    def get_home(self,req):
        return FileResponse(self.root_path+'/index.html')

if __name__ == '__main__':
    app = Webserver('Challenges')
    app.start()