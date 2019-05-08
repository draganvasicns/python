import RegexParserObject
import re
import sys
import getopt


class RegexForSREParsingObject(RegexParserObject.RegexParserObject):
  def __init__(self):
    self.optionExpression = re.compile(
        "(?P<root>[a-zA-Z0-9 ]{6})(?P<expirationC>[\dPC]{7})(?P<strike>\d{8})")

  def formatOption(self, optionString):
    # for now just return it
    # (?P<root>[a-zA-Z0-9 ]{6})(?P<expirationC>[\dPC]{7})(?P<strike>\d{8})
    # uncoment if some parsing of option is needed
    match = self.optionExpression.match(optionString)
    if (match):
      retVal = '.'+match.group('root').strip()+' '+match.group(
          'expirationC')+(str(int(float(match.group('strike')))))
      return retVal
    return optionString

  def parseLine(self, line):
    lineElements = line.split("|")
    if (len(lineElements)<114):
      return None #this could be header file
    qty = lineElements[73]
    if(float(qty) == 0): #skip lines that have qty = 0
      return None
    instrumentType = lineElements[14].strip()
    symbol = None
    if(instrumentType == "EQUITY") :
      symbol = lineElements[16]
    elif(instrumentType == "OPTION") :
      symbol = self.formatOption(lineElements[114])
    if(symbol is None or len(symbol.strip()) == 0):
      return None
    retLine = []
    account = lineElements[3]
    price = lineElements[76]
    retLine.append(account.strip())
    retLine.append(account.strip())
    retLine.append(symbol.strip())
    retLine.append(str(int(float(qty))))
    return ",".join(retLine)
 
if __name__ == "__main__":
  parser = SumoForSREParsingObject()
  parser.start(sys.argv[1:])

