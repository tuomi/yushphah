import textHandler

# requires:
# textHandlerContext
# 	// initializes ParamsBuilder
# inpHandler
# 	getLine
# 	nextLine
# outHandler
#	put
class ServantFactory():
	@staticmethod
	def getServant():
		s = Servant()
		s.textHandlerContext = textHandler.TextHandlerContext()
		s.ioHandler = None
		return s
class Servant():
	def setIOHandler(t, ioh):
		t.ioHandler = ioh
	def defaultProcessFileSettings(t, ifname):
		t.ioHandler.inputFile(ifname)
		t.ioHandler.outputDfltFile()
		t.textHandlerContext.parDict["reportName"] = ifname[:-len(t.ioHandler.dfltInpExt)]

class IOHandlerFactory():
	@staticmethod
	def getIOHandler():
		return IOHandler()
class IOHandler():
	dfltInpExt = ".pjr"
	dfltOutExt = ".jrxml"
	eof = True
	def inputFile(t, fname):
		t.ifname = fname
		t.ihandle = open(fname, 'r')
		t.line = t.ihandle.readline()
		if(t.line != ""):
			t.eof = False
	def getLine(t):
		return t.line
	def nextLine(t):
		t.line = t.ihandle.readline()
		if(t.line == ""):
			t.eof = True
		return t.line
	def outputFile(t, fname):
		t.ofname = fname
		t.ohandle = open(fname, 'w')
	def outputDfltFile(t):
		if(t.ifname.endswith(t.dfltInpExt)):
			t.ofname = t.ifname[:-len(t.dfltInpExt)] + t.dfltOutExt
			t.outputFile(t.ofname)
		else:
			raise Exception("unable to open file -- no supplied arguments")
	def put(t, s):
		t.ohandle.write(s)
