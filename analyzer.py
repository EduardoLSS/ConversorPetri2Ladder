
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
      setOutputList.insert(0, outTransition)
    if isinstance(outTransition,AST.ResetOutput):
      resetOutputList.insert(0, outTransition)

    conditions = normalConditions
    conditions.extend(negatedConditions)

    laddernet = AST.LadderNet(conditions, setOutputList, resetOutputList)
    laddernetList.append(laddernet)

  return sorted(
    laddernetList,
    key=lambda item: (
      min(
        (int(input.identifier[1:]) for input in item.conditions if input.identifier.startswith('P')),
        default=float('inf')
      )
    )
  )

def outputForTransition(transition):
  if transition.id.startswith('S'):
    return AST.SetOutput(transition.id)
  elif transition.id.startswith('R'):
    return AST.ResetOutput(transition.id)
  else:
    return None
