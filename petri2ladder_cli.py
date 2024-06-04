
import argparse
import parser
import analyzer as AL
import ladder_generator as LG

def petri2ladder(args):
  filepath = args.source
  dest = args.destination
  petrinet = parser.netFromFile(filepath)
  astNet = AL.analyze_net(petrinet)
  LG.generate_xml(astNet,dest)

cliparser = argparse.ArgumentParser()
cliparser.add_argument("--destination")
cliparser.add_argument("--source")

if __name__ == "__main__":
  args = cliparser.parse_args()
  petri2ladder(args)
