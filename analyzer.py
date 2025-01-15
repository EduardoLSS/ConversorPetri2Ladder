
import re
import AST
import Petri

def analyze_net(petrinet):
  # Validate Petri Net
  for arc in petrinet.arcs:
    hasPlaceSource = [place for place in petrinet.places if arc.source_id == place.id]
    hasPlaceDestination = [place for place in petrinet.places if arc.destination_id == place.id]
    hasTransitionSource = [transition for transition in petrinet.transitions if arc.source_id == transition.id]
    hasTransitionDestination = [transition for transition in petrinet.transitions if arc.destination_id == transition.id]

  if hasPlaceSource and hasPlaceDestination:
    raise ValueError("Petri Net not suported")
  if hasTransitionSource and hasTransitionDestination:
    raise ValueError("Petri Net not suported")
  
  # Construct Symbols
  arc_destinations = [arc.destination_id for arc in petrinet.arcs]
  arc_sources = [arc.source_id for arc in petrinet.arcs]
  flags_places = [place for place in petrinet.places if place.id in arc_destinations and place.id in arc_sources]
  input_places = [place for place in petrinet.places if place.id not in arc_destinations and place.id in arc_sources]
  laddernetList = []

  for transition in petrinet.transitions:
    arcs_input = [arc.source_id for arc in petrinet.arcs if arc.destination_id == transition.id]
    normal_inputs = [place for place in petrinet.places if place.id in arcs_input and not arc.negated]
    negated_inputs = [place for place in petrinet.places if place.id in arcs_input and arc.negated]
    arcs_output = [arc.destination_id for arc in petrinet.arcs if arc.source_id == transition.id]
    outputs = [place for place in petrinet.places if place.id in arcs_output]

    if not normal_inputs and not negated_inputs:
      raise ValueError("Petri Net invalida: Não contem input")
    if not outputs:
      raise ValueError("Petri Net invalida: não contem output")

    normalConditions = [AST.Input(place.id, False) for place in normal_inputs]
    negatedConditions = [AST.Input(place.id, True) for place in negated_inputs]
    resetOutputList = [AST.ResetOutput(place.id) for place in normal_inputs if place in flags_places]
    setOutputList = [AST.SetOutput(place.id) for place in outputs]
    outTransition = outputForTransition(transition)

    if isinstance(outTransition,AST.SetOutput):
      setOutputList.append(outTransition)
    if isinstance(outTransition,AST.ResetOutput):
      resetOutputList.append(outTransition)

    conditions = normalConditions
    conditions.extend(negatedConditions)

    laddernet = AST.LadderNet(conditions, setOutputList, resetOutputList)
    laddernetList.append(laddernet)

  return laddernetList

def outputForTransition(transition):
  regex = re.compile(r".*\((.*) - (.*)\)")
  match = regex.match(transition.id)
  if match is None:
    return None

  isSet = match.group(1) != 'R'
  output = match.group(1)
  if isSet:
    return AST.SetOutput(output)
  else:
    return AST.ResetOutput(output)
