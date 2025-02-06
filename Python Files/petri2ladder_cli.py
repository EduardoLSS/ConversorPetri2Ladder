
import parser
import analyzer as AL
import ladder_generator as LG

def petri2ladder(source, destination):
  filepath = source
  dest = destination
  petrinet = parser.netFromFile(filepath)
  astNet = AL.analyze_net(petrinet)
  LG.generate_xml(astNet,dest)
