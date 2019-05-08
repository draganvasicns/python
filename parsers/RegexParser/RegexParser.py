import sys
import getopt
import os.path
import re
import datetime

optionExpression = re.compile("(?P<root>[a-zA-Z0-9 ]{6})(?P<expiration>[\d]{6})(?P<callPut>[PC]{1})(?P<strike>\d{8})")
today = datetime.date.today()

def createFile(infile, outfile):
  input = open(infile,"r")
  output = open(outfile, "w+")
  i = 0
  w = 0
  for line in input:
      i += 1
      if i % 1000 == 0:
          print('Read %d lines '%i)
      try:
        retLine = parseLine(line)
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


def parseLine(line):
  lineElements = line.split("|")
  if (len(lineElements)<114):
     return None #this could be header file
  qty = lineElements[73]
  if(float(qty) == 0): #skip lines that have qty = 0
    return None
  instrumentType = lineElements[14].strip()
  symbol = None
  instType = None
  if(instrumentType == "EQUITY") :
    symbol = lineElements[16]
    instType = "E"
  elif(instrumentType == "OPTION") :
    symbol = formatOption(lineElements[114])
    instType = "O"
  if(symbol is None or len(symbol.strip()) == 0):
    return None
  retLine = []
  account = lineElements[3]
  price = lineElements[76]
  retLine.append(account.strip())
  retLine.append(symbol.strip())
  retLine.append(str(int(float(qty))))
  retLine.append(str(float(price)))
  retLine.append(instType)
  return ",".join(retLine)

def formatOption(optionString):
  #for now just return it
  #(?P<root>[a-zA-Z0-9 ]{6})(?P<expirationC>[\dPC]{7})(?P<strike>\d{8})
  #uncoment if some parsing of option is needed
  match = optionExpression.match(optionString)
  if (match):
    expirationDate = datetime.datetime.strptime(match.group('expiration'), "%y%m%d").date()
    retVal = None
    if (expirationDate >= today):
      retVal = match.group('root').strip()+' '+match.group('expiration')+match.group('callPut')+(str(int(float(match.group('strike')))))
    return retVal
  return optionString

usage = "Usage: RegexParser.py -i <inputfile> -o <outputfile>"

if __name__ == "__main__":
  
  inputfile = ''
  outputfile = ''
  try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile="])
  except getopt.GetoptError:
    print(usage)
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
        print(usage)
        sys.exit()
    elif opt in ("-i", "--ifile"):
        inputfile = arg
    elif opt in ("-o", "--ofile"):
        outputfile = arg
  if(not os.path.exists(inputfile)):
    print ("Input file is not accesible or do not exists: ",inputfile)
    print(usage)
    sys.exit(2)
  createFile(inputfile, outputfile)