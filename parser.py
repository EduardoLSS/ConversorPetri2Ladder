
import xml.etree.ElementTree as ElementTree
import Petri

def xml2Net(xml):
  net = Petri.Net()
  net.places = [placeFromElement(x) for x in xml.findall(".//place")]
  net.arcs = [arcFromElement(x) for x in xml.findall(".//arc")]
  net.transitions = [transitionFromElement(x) for x in xml.findall(".//transition")]
  return net
def arcFromElement(element):
  source = element.get("source")
  destination = element.get("target")
  inhibitor = element.find("type").get("value") == "inhibitor"
  return Petri.Arc(source,destination, inhibitor)
def placeFromElement(element):
  identifier = element.get("id")
  name = element.find("name").find("value").text
  return Petri.Place(identifier, name)
def transitionFromElement(element):
  identifier = element.get("id")
  name = element.find("name").find("value").text
  return Petri.Transition(identifier, name)
def netFromFile(filepath=None):
  with open(filepath) as xmlFile:
    xml = ElementTree.parse(xmlFile)
    return xml2Net(xml.getroot())
