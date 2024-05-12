
'''
	import recycling.instrument.layer.start_dev as flask_dev
'''

import recycling.instrument.layer as instrument_flask

def start (port):
	print ('starting')
	
	app = instrument_flask.build ()
	app.run (port = port)

	return;
	
#if __name__ == "__main__":
#	start ()