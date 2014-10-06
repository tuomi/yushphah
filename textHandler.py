import re

import staticData

# TODO support for groups

def textHandler(serf):
	lineEx = re.compile("<([^>]*)>(.*)")
	ih = serf.inpHandler
	paramsBuilder = ParamsBuilder(serf.textHandlerContext)

	while(True):
		line = ih.getLine()
		if not line:
			break
		
		params = paramsBuilder.getPrototype()
		m = lineEx.match(line)
		if(m):
			params.merge(m.groups()[0])
			cont = m.groups()[1]
		else:
			cont = line

		paramsBuilder.update(params)	# TODO this also updates params -- better naming convention
		outputTextField(cont, params.dic, serf)
		ih.nextLine()

class Params():
	singleVal = re.compile('[ \t]*([^"]*)[ \t]*=[ \t]*"([^"]*)"')	# explanation: matches ' par = "value" '
	def __init__(t, dic):
		t.dic = dic
	def merge(t, params):
		while True:
			m = singleVal.match(params)
			if not m:
				break	# TODO check for trailing
			params = params[m.end():]
			t.dic[m.group(1)] = m.group(2)

def outputTextField(cont, params, serf):
	s = ""
	s += staticData.jrxmlSnips["textFieldIntro"].format(**params)
	s += staticData.jrxmlSnips["reportElement"].format(**params)
	s += staticData.jrxmlSnips["textExpression"].format(**params)
	s += staticData.jrxmlSnips["textFieldOutro"].format(**params)
	serf.outHandler.put(s)
	
class ParamsBuilder():
	def __init__(t, context):
		t.prototype = {	# NOTE all this might be overriden from textHandlerContext (preferable way for setting default/starting configuration)
			"x" : 0, "xPre" : 0, "xPost" : 0,
			"y" : 0, "yPre" : 0, "yPost" : 0,
			"key" : 1,
			"linewidth" : 483, "lineheight" : 13
		}
		for k in context.parDict:
			t.prototype[k] = context.parDict[k]	# TODO aint there a bultin for that?
	def getPrototype(t):
		return Params(t.prototype.copy())
	def updatePrototype(t, pPrint):
		dNext = t.prototype
		dPrint = pPrint.dic
		dNext["x"] += dPrint["xPre"] + dPrint["xPost"]
		dPrint["x"] += dPrint["xPre"]
		dNext["y"] += dPrint["yPre"] + dPrint["yPost"]
		dPrint["y"] += dPrint["yPre"]
		dNext["key"] += 1
