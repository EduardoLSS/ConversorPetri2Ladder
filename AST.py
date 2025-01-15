
# --- AST ---
# --- [Condition] [Resets] [Sets]
class LadderNet:
  def __init__(self, conditions, setOutputList, resetOutputList):
    self.conditions = conditions
    self.setOutputList = setOutputList
    self.resetOutputList = resetOutputList

  def __repr__(self):
    return "AST.LadderNet: conditions=%s, sets=%s, resets=%s " % (str(self.conditions), str(self.setOutputList), str(self.resetOutputList))
  
class Input:
  def __init__(self, identifier, negated = False, output = None):
    self.identifier = identifier
    self.negated = negated
    self.output = output

  def __repr__(self):
    if self.output is None:
      return "AST.Input(id=%s, negated=%s, output=None)" % (self.identifier, self.negated)
    else:
      return "AST.Input(id=%s, negated=%s, output=%s)" % (self.identifier, self.negated,self.output)
    
class ResetOutput:
  def __init__(self, identifier):
    self.identifier = identifier
  def __repr__(self):
    return "AST.ResetOutput(id=%s)" % self.identifier
  
class SetOutput:
  def __init__(self, identifier):
    self.identifier = identifier
  def __repr__(self):
    return "AST.SetOutput(id: %s)" % self.identifier
