import sys

def debug(msg):
  out = "[ DEBUG ]: %s" % msg
  print(out)

def error(msg):
  out = "[ ERROR ]: %s" % msg
  sys.exit(out)

def info(msg):
  out = "[ INFO  ]: %s" % msg
  print(out)
