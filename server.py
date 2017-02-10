#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.websocket import *
from tornado.template import *
from tornado.ioloop import *
from tornado.web import *
from tornado.concurrent import *
import time
import cv2

isPi=0
if isPi==0:
	import serial
	ser=serial.Serial('/dev/ttyACM0',9600)
else:
	from RPi.GPIO import *
	l1=37
	reset=35
	setmode(BOARD)
	setup(l1,OUT)
	setup(reset,OUT)


TIMEOUT_CAM=2 #cam
TIMEOUT_IND=4 #indicator



print('VDS')
print('')



place_template="template"

spisok=[]






class Index(RequestHandler):
	def get(self):
		template=Loader(place_template)
		self.write(template.load("index.html").generate(s=spisok))
	def post(self):
		spisok.append([self.get_argument('name'), str(self.get_argument('value'))[-1]])
		self.redirect(r'/')


class MyStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')



def vid():
	cam = cv2.VideoCapture(0)
	cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
	cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
	cam.set(cv2.cv.CV_CAP_PROP_FPS, 25)
	ret_val, img = cam.read()
	cv2.waitKey(10)
	#~ cv2.imshow('r',img)
	cv2.imwrite('template/img/index.jpg',img)
	IOLoop.current().add_timeout(time.time() + TIMEOUT_CAM, vid)

	#~
def indicator():
	if spisok!=[]:
		ser.write(spisok.pop(0)[1])
	IOLoop.current().add_timeout(time.time() + TIMEOUT_IND, indicator)



def indicator_pi():
	if spisok!=[]:
		output(reset,0)
		output(reset,1)
		output(reset,0)
		for i in range(int(spisok.pop(0)[1])):
			output(l1,0)
			output(l1,1)

	IOLoop.current().add_timeout(time.time() + TIMEOUT_IND, indicator_pi)

application = Application([
	(r"/", Index),
	#~ (r"/1.html", StaticFileHandler, {'path': ''}),
	(r"/img/(.*)", MyStaticFileHandler, {'path': 'template/img/'}),
	(r"/css/(.*)", MyStaticFileHandler, {'path': 'template/css/'}),
])



if __name__ == "__main__":
	application.listen(1337)
	IOLoop.current().add_timeout(time.time() + TIMEOUT_CAM, vid)
	if isPi==1:
		IOLoop.current().add_timeout(time.time() + TIMEOUT_IND, indicator_pi)
	else:
		IOLoop.current().add_timeout(time.time() + TIMEOUT_IND, indicator)
	IOLoop.current().start()
