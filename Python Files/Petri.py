
class Place:
  def __init__(self, place_id, place_name):
    self.id = place_id
    self.name = place_name

  def __repr__(self):
    return "Place(%s, %s)" % (self.id, self.name)

class Transition:
  def __init__(self, transition_id, transition_name):
    self.id = transition_id
    self.name = transition_name

  def __repr__(self):
    return "Transition(%s, %s)" % (self.id, self.name)

class Arc:
  def __init__(self, source_id, destination_id, negated=False):
    self.source_id = source_id
    self.destination_id = destination_id
    self.negated = negated

  def __repr__(self):
    return "Arc(%s, %s, %s)" % (self.source_id, self.destination_id, self.negated)

class Net:
  def __init__(self):
    self.places = []
    self.transitions = []
    self.arcs = []

  def __repr__(self):
    return " places: %s \n transitions: %s \n arcs: %s " % (str(self.places), str(self.transitions), str(self.arcs))
