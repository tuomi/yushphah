import re

import staticData

# TODO support for groups

# responsible for setting up TextHandlerContext
def confHandler(serf):
	pass
	

def controlStatementSubhandler(statementLine, textController):
	print 'statement subh: ' + statementLine
	controlStatements = [
		(
			re.compile('group (.*)'),
			lambda m : textController.newGroup(m.groups()[0])
		),
		(
			re.compile('groupFt'),
			lambda m : textController.groupFooter()
		),
	]
	for case in controlStatements:
		m = case[0].match(statementLine)
		if(m):
			case[1](m)
			break

# responsible for creating the resulting .jrxml document
def textHandler(serf):
	ioh = serf.ioHandler
	textController = TextController(serf.textHandlerContext, serf.ioHandler)
	getParams = textController.getPrototype

	textElementOutput = lambda params : outputElements(["textFieldIntro", "reportElement", "textExpression", "textFieldOutro"], textController.updateAfter(params).dic, textController.putTextElement)
	subhandlers = [
		# '<' + control-statement (without '>')
		(
			re.compile("<([^>])*$"),
			lambda m : controlStatementSubhandler(m.group()[1:], textController)
		),
		# '<' + params + '>' + text
		(
			re.compile("<([^>]*)>(.*)"),
			lambda m : textElementOutput(getParams().merge(m.groups()[0]).setKey("cont",m.groups()[1]))
		),
		# anything else
		(
			re.compile(".*"),
			lambda m : textElementOutput(getParams().setKey("cont",m.group()))
		),
	]
		
	
	outputElements(["reportIntro"], serf.textHandlerContext.parDict, serf.ioHandler.put)

	while(True):
		if ioh.eof:
			break
		line = ioh.getLine().strip()
		
		for case in subhandlers:
			m = case[0].match(line)
			if(m):
				case[1](m)
				break
		ioh.nextLine()

	textController.flushState()
	textController.flushState()	# NOTE not a bug -- if input ended with a definition of a header but without definition of a footer
	outputElements(["reportOutro"], serf.textHandlerContext.parDict, serf.ioHandler.put)

class Params():
	singleVal = re.compile('[ \t]*([^"]*)[ \t]*=[ \t]*"([^"]*)"')	# explanation: matches ' par = "value" '
	def __init__(t, dic):
		t.dic = dic
	def merge(t, params):
		while True:
			m = t.singleVal.match(params)
			if not m:
				break	# TODO check for trailing
			params = params[m.end():]
			t.dic[m.group(1)] = m.group(2)
		return t
	def setKey(t, key, value):
		t.dic[key] = value
		return t

def outputElement(key, params):
	return staticData.jrxmlSnips[key].format(**params)
def outputElements(keyList, params, putFunction):
	s = ""
	for k in keyList:
		s += outputElement(k,params)
	putFunction(s)

class TextController():
	def __init__(t, context, ioHandler):
		t.prototype = {	# NOTE all this might be overriden from textHandlerContext (preferable way for setting default/starting configuration)
			"x" : 0, "xPre" : 0, "xPost" : 0,
			"y" : 0, "yPre" : 0, "yPost" : 13,
			"key" : 1,
			"style" : "Text12",
			"linewidth" : 483, "lineheight" : 13,
			"cont" : "",
		}
		t.groupName = None
		t.groupState = None
		t.bufferHeight = 0
		t.groupBuffer = ""
		for k in context.parDict:
			t.prototype[k] = context.parDict[k]	# TODO aint there a bultin for that?
		t.ioHandler = ioHandler
	def getPrototype(t):
		return Params(t.prototype.copy())
	def updateAfter(t, pPrint):
		dNext = t.prototype
		dPrint = pPrint.dic
		dNext["x"] += int(dPrint["xPre"]) + int(dPrint["xPost"])
		dPrint["x"] += int(dPrint["xPre"])
		dNext["y"] += int(dPrint["yPre"]) + int(dPrint["yPost"])
		dPrint["y"] += int(dPrint["yPre"])
		dNext["key"] += 1	# NOTE non-standard, beware
		if( t.bufferHeight < int(dNext["y"]) ):
			t.bufferHeight = int(dNext["y"])
		return pPrint
	def putTextElement(t,s):
		if not t.groupState:
			raise Exception('Malformed input -- text element not in a group')
		t.groupBuffer += s
	def put(t, s):
		t.ioHandler.put(s)
	def flushTextElements(t):
		print 'flush'
		t.bufferHeight = 0
		t.prototype["y"] = 0	# TODO not a good idea, somehow read something more default (thc?)
		t.put(t.groupBuffer)
		t.groupBuffer = ""
	def flushState(t):
		if(t.groupState == "Header"):
			t.groupFooter()
			t.groupState = "Footer"
		elif(t.groupState == "Footer"):
			outputElements(["groupFooterIntro"], { "height" : t.bufferHeight}, t.put)
			t.flushTextElements()
			outputElements(["groupOutro"], {}, t.put)
			t.groupState = None
	def newGroup(t, name):
		t.flushState()
		outputElements(["groupIntro"] , { "groupName" : name }, t.put)
		t.groupState = "Header"
	def groupFooter(t):
		outputElements(["groupHeaderIntro"], { "height" : t.bufferHeight}, t.put)
		t.flushTextElements()
		t.groupState = "Footer"
	

class TextHandlerContext():
	def __init__(t):
		t.parDict = {
			"reportName" : "DefaultReportName",
			"orientation" : "Portrait",
			"pageWidth" : "595",
			"pageHeight" : "842",
			"columnWidth" : "483",
		}
