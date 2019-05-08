import sys
import getopt
import os.path
import re


class SumoParserObject :
  usage = "Usage: SumoParser.py -i <inputfile> -o <outputfile>"
  
  def formatOption(self, optionString):
    #for now just return it
    #(?P<root>[a-zA-Z0-9 ]{6})(?P<expirationC>[\dPC]{7})(?P<strike>\d{8})
    #uncoment if some parsing of option is needed
    #match = optionExpression.match(optionString)
    #if (match):
    #  retVal = '.'+match.group('root').strip()+' '+match.group('expirationC')+(str(int(float(match.group('strike')))))
    #  return retVal
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
    retLine.append(symbol.strip())
    retLine.append(str(int(float(qty))))
    retLine.append(str(float(price)))
    return ",".join(retLine)


  def createFile(self, infile, outfile):
    input = open(infile,"r")
    output = open(outfile, "w+")
    i = 0
    w = 0
    for line in input:
        i += 1
        if i % 1000 == 0:
            print('Read %d lines '%i)
        try:
          retLine = self.parseLine(line)
          if (retLine):
            w += 1
            output.write(retLine)
            output.write('\n')
            if w % 1000 == 0:
              print(f'Wrote {w} lines')
        except Exception as e:
          print(f'Error {e} in line {line} ')
    input.close()
    output.flush()
    output.close()
    print('Finish writing! Wrote %d lines '%w)

  def start(self, argsv):
    inputfile = ''
    outputfile = ''
    try:
      opts, args = getopt.getopt(argsv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
      print(self.usage)
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
          print(self.usage)
          sys.exit()
      elif opt in ("-i", "--ifile"):
          inputfile = arg
      elif opt in ("-o", "--ofile"):
          outputfile = arg
    if(not os.path.exists(inputfile)):
      print ("Input file is not accesible or do not exists: ",inputfile)
      print(self.usage)
      sys.exit(2)
    
    self.createFile(inputfile, outputfile)



if __name__ == "__main__":
  parser = SumoParserObject()
  parser.start(sys.argv[1:])
