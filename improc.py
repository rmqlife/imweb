import cv2
def process(src_path,dst_path):
	im=cv2.imread(src_path,0)
	cv2.imwrite(dst_path,im)

def improc(filename):
	import os.path as op
	dst_path=op.join('static/',op.basename(filename))
	#dst_path=op.join('static','show.jpg')
	process(filename,dst_path)
	return dst_path

if __name__=='__main__':
	print improc('pics/baidu.png')
