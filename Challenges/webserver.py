from wsgiref.simple_server import make_server
from pyramid.response import Response, FileResponse
from pyramid.config import Configurator
import threading
from os import listdir
from os.path import isfile, join
from detector import Detector
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import cv2 as cv

class Logger():
    def __init__(self):
        load_dotenv('credentials.env')
        self.db_host = os.environ['MYSQL_HOST']
        self.db_user = os.environ['MYSQL_USER']
        self.db_pass = os.environ['MYSQL_PASSWORD']
        self.db_name = os.environ['MYSQL_DATABASE']

        self.db = mysql.connect(
        host=self.db_host,
        user=self.db_user,
        password=self.db_pass,
        database=self.db_name,
        )

        self.cursor = self.db.cursor()

        print('Connected to database')

    def __del__(self):
        self.db.close()

    def add_entry(self, img_name, lin_plate):
        try:
            self.cursor.execute(f'INSERT INTO Logs (name, text) VALUES (\'{img_name}\',\'{lin_plate}\');')
            self.db.commit()
            print("Added entry to database")
        except:
            print('Unable to add entry into database')
        
class Webserver(Logger):
    def __init__(self, root_path):
        # Initialize logger
        super().__init__()

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
            config.add_route('plate', '/plate')
            config.add_route('text', '/text')

            # Creates views for routes
            config.add_view(self.get_home, route_name='home')
            config.add_view(self.get_names, route_name='names', renderer='json')
            config.add_view(self.get_text, route_name='text', renderer='json')
            config.add_view(self.get_frame, route_name='frame')
            config.add_view(self.make_detector, route_name='detect')
            config.add_view(self.get_plate, route_name='plate')

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
        self.detector.detect_plate()
        self.detector.get_text()
        
        # Add entry to database
        super().add_entry(the_name,self.detector.text)

        return Response('ok')

    def get_frame(self,req):
        cv.imwrite(self.pub_path+'/temp/frame.jpg',self.detector.frame)
        return FileResponse(self.pub_path+'/temp/frame.jpg')

    def get_plate(self,req):
        cv.imwrite(self.pub_path+'/temp/plate.jpg',self.detector.plate)
        return FileResponse(self.pub_path+'/temp/plate.jpg')

    def get_text(self,req):
        return Response(f'[\"{self.detector.text}\"]')

def main():
    app = Webserver('./Challenges')
   
    try:
        app.start()
    except KeyboardInterrupt:
        app.stop()

if __name__ == '__main__':
    main()