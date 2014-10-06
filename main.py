#!/usr/bin/python
import sys
import textHandler
import servant

def processFile(serf, fname):
	serf.defaultProcessFileSettings(fname)
	ioh = serf.ioHandler

	sectionHandlers = {
		"=Data=" : None, 
		"=Conf=" : None,
		"=Text=" : textHandler.textHandler,
	}

	while(True):
		l = ioh.getLine().strip()
		if(ioh.eof):
			break;
		elif(l in sectionHandlers):
			ioh.nextLine()
			sectionHandlers[l](serf)
		elif(l == ""):
			ioh.nextLine()
		else:
			raise Exception("malformed input, detected on line: <" + l + ">")


if __name__ == "__main__":
	serf = servant.ServantFactory.getServant()
	serf.setIOHandler(servant.IOHandlerFactory.getIOHandler())
	processFile(serf, sys.argv[1])
