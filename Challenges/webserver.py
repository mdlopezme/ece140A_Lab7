import imghdr
from wsgiref.simple_server import make_server
import cv2
from pyramid.response import Response, FileResponse
from pyramid.config import Configurator
import threading
from os import listdir
from os.path import isfile, join
from detector import Detector
from PIL import Image
import numpy as np
import cv2 as cv

class Webserver():
    def __init__(self, root_path):
        # Temp to make it work nice with our systems
        self.root_path = root_path
        self.pub_path = self.root_path + '/public'
        self.img_path = self.pub_path + '/images'

        with Configurator() as config:
            # Add routes
            config.add_route('home', '/')
            config.add_route('names', '/names')
            config.add_route('frame', '/frame')
            config.add_route('detect', '/detect')

            # Creates views for routes
            config.add_view(self.get_home, route_name='home')
            config.add_view(self.get_names, route_name='names', renderer='json')
            config.add_view(self.get_frame, route_name='frame')
            config.add_view(self.make_detector, route_name='detect', renderer='json')

            # Create static routes
            config.add_static_view(name='/', path='main:public/')

            app = config.make_wsgi_app()

        self.server = make_server('localhost', 6543, app)

    def start(self):
        print('Web server started on: http://localhost:6543')
        self.server_thread=threading.Thread(target=self.server.serve_forever,name="Web Server")
        self.server_thread.start()
        self.server_thread.join()

    def stop(self):
        print("Ending web server")
        self.server.shutdown()
    
    def get_home(self,req):
        return FileResponse(self.root_path+'/index.html')

    def get_names(self,req):
        names = [f for f in listdir(self.img_path) if isfile(join(self.img_path, f))]

        names.sort()
        return names

    def make_detector(self,req):
        the_name=req.params['image']
        self.detector = Detector(self.img_path+'/'+ the_name,'C',False)

        return Response(f'[{the_name}]')

    def get_frame(self,req):
        cv.imwrite(self.pub_path+'/temp/frame.jpg',self.detector.frame)
        return FileResponse(self.pub_path+'/temp/frame.jpg')

if __name__ == '__main__':
    app = Webserver('./Challenges')
   
    try:
        app.start()
        # while(True):
        #     sleep(100)
    except KeyboardInterrupt:
        app.stop()