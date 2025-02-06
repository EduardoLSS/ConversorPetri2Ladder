
#!/usr/bin/env python3
import xml.etree.ElementTree as ElementTree
import copy
import AST

localId = 3
rightTrailOffset = 300
positionX = 256
positionY = 150

def generate_xml(ast, filepath):
  calculateRightTrailDistance(ast)
  project = xmlProject(ast)
  xmlString = ElementTree.tostring(project, encoding='utf-8', method='xml').decode()
  with open(filepath, 'w') as xmlFile:
    xmlFile.write(xmlString)

def xmlFileHeader(root):
  header = ElementTree.SubElement(root,'fileHeader')
  header.set('companyName','UFSCar')
  header.set('productName','Conversor PNML2Ladder')
  header.set('productVersion','1')
  header.set('creationDateTime','2025-01-15T12:13:14')

def xmlContentHeader(root):
  header = ElementTree.SubElement(root,'contentHeader')
  header.set('name','Desconhecido')
  header.set('modificationDateTime','2025-01-15T12:13:14')
  info = ElementTree.SubElement(header, 'coordinateInfo')
  pageSize = ElementTree.SubElement(info,'pageSize')
  pageSize.set('x','3000')
  pageSize.set('y','3000')
  fbd = ElementTree.SubElement(info, 'fbd')
  fdb_scaling = ElementTree.SubElement(fbd, 'scaling')
  fdb_scaling.set('x','0')
  fdb_scaling.set('y','0')
  ld = ElementTree.SubElement(info, 'ld')
  ld_scaling = ElementTree.SubElement(ld, 'scaling')
  ld_scaling.set('x','0')
  ld_scaling.set('y','0')
  sfc = ElementTree.SubElement(info, 'sfc')
  sfc_scaling = ElementTree.SubElement(sfc, 'scaling')
  sfc_scaling.set('x','0')
  sfc_scaling.set('y','0')

def xmlLeftTrail(root, ast):
  leftTrail = ElementTree.SubElement(root, 'leftPowerRail')
  setLocalId(leftTrail, 1)
  xmlPosition(leftTrail, positionX, positionY - 20)
  size_for_each_net = [len(net.setOutputList) + len(net.resetOutputList) for net in ast]
  offset = 0
  current_size = 0
  for i in range(len(ast)):
    if i > 0:
      offset += size_for_each_net[i-1]
    current_size = 20 + 40 * offset
    connectionPointOut = ElementTree.SubElement(leftTrail, 'connectionPointOut')
    connectionPointOut.set('formalParameter','')
    relPosition = ElementTree.SubElement(connectionPointOut, 'relPosition')
    relPosition.set('x','3')
    relPosition.set('y',str(current_size))
  leftTrail.set('width','3')
  leftTrail.set('height',str(current_size+20))

def calculateRightTrailDistance(ast):
  global rightTrailOffset
  maxLength = 0
  for conditionList in ast:
    if len(conditionList.conditions) > maxLength:
      maxLength = len(conditionList.conditions)
  rightTrailOffset = 300 + 30 * (maxLength + 1)

def xmlRightTrail(root, ast):
  rightTrail = ElementTree.SubElement(root, 'rightPowerRail')
  setLocalId(rightTrail, 2)
  xmlPosition(rightTrail, positionX + rightTrailOffset, positionY - 20)
  size_for_each_net = [len(net.setOutputList) + len(net.resetOutputList) for net in ast]
  totalOutputs = sum(size_for_each_net)
  current_size = 0
  for i in range(totalOutputs):
    current_size = 20 + 40 * i
  rightTrail.set('width','3')
  rightTrail.set('height',str(current_size+20))
  return rightTrail

def xmlLadderNet(root, rightTrail, ast):
  line = 0
  for i in range(len(ast)):
    net = ast[i]
    previousId = '1'
    previousPosX = 0
    previousPosY = 0
    for j in range(len(net.conditions)):
      conn = net.conditions[j]
      referenceId = copy.deepcopy(previousId)
      previousId, previousPosX, previousPosY = xmlContact(root,conn, referenceId, line, j, j != 0)
    setOutNumber = len(net.setOutputList)
    for j in range(setOutNumber):
      conn = net.setOutputList[j]
      xmlCoil(root, conn, rightTrail, copy.deepcopy(previousId), (previousPosX, previousPosY), line + j, len(net.conditions) + 1, True)
    line = line + setOutNumber
    resetOutNumber = len(net.resetOutputList)
    for j in range(resetOutNumber):
      conn = net.resetOutputList[j]
      xmlCoil(root, conn, rightTrail, copy.deepcopy(previousId), (previousPosX, previousPosY), line + j, len(net.conditions) + 1, False)
    line = line + resetOutNumber

def xmlContact(root, conn, previousId, line, offset, correctId):
  contact = ElementTree.SubElement(root, 'contact')
  updateLocalId(contact)
  if conn.negated:
    contact.set('negated','true')
  else:
    contact.set('negated','false')
  x,y = xmlContactCoilPosition(contact,line,offset)
  previousX, previousY = contactCoilPosition(line,offset-1)
  xmlContactCoilConnectionIn(contact,previousId, (previousX+21,previousY), (x,y), correctId)
  xmlContactCoilConnectionOut(contact)
  xmlContactCoilName(contact, conn.identifier)
  xmlContactCoilSize(contact)

  global localId
  return localId, x, y

def xmlCoil(root, conn,rightTrail, previousId, previousPos, line, offset, isSet):
  coil = ElementTree.SubElement(root,'coil')
  updateLocalId(coil)
  coil.set('negated','false')
  if isSet:
    coil.set('storage','set')
  else:
    coil.set('storage','reset')
  x,y = xmlContactCoilPosition(coil,line,offset,1)
  previousX, previousY = previousPos
  xmlContactCoilConnectionIn(coil,previousId,(previousX + 21, previousY),(x,y), True)
  xmlContactCoilConnectionOut(coil)
  xmlContactCoilName(coil, conn.identifier)
  xmlContactCoilSize(coil)
  global localId
  xmlContactCoilConnectionIn(rightTrail,localId, (x,y), (positionX + rightTrailOffset, positionY + 21), True)

  return x, y

def xmlContactCoilConnectionIn(root,referenceId, previousPosition, currentPosition, correctId = False):
  connIn = ElementTree.SubElement(root,'connectionPointIn')
  relPosition = ElementTree.SubElement(connIn, 'relPosition')
  relPosition.set('x','0')
  relPosition.set('y','8')
  conn = ElementTree.SubElement(connIn, 'connection')
  if correctId:
    conn.set('refLocalId',str(referenceId-1))
  else:
    conn.set('refLocalId',str(referenceId))

  currentX, currentY = currentPosition
  previousX, previousY = previousPosition

  xmlPosition(conn, currentX, currentY + 8)
  if previousY != currentY:
    xmlPosition(conn, round((previousX + currentX)/2), currentY + 8)
    xmlPosition(conn, round((previousX + currentX)/2), previousY + 8)
  xmlPosition(conn,previousX, previousY + 8)

def xmlPosition(root, x, y):
  position = ElementTree.SubElement(root, 'position')
  position.set('x',str(x))
  position.set('y',str(y))

def contactCoilPosition(line, offset):
  global positionY
  global positionX
  y = line * 40 + positionY - 8
  x = (offset + 1) * 60 + positionX
  return (x,y)

def xmlContactCoilPosition(root, line, offset, isCoil = 0):
  global positionX, rightTrailOffset
  x,y = contactCoilPosition(line,offset)
  if isCoil == 1:
    x = positionX + rightTrailOffset - 60
  xmlPosition(root, x, y)
  return x,y

def xmlContactCoilConnectionOut(root):
  out = ElementTree.SubElement(root,'connectionPointOut')
  relPosition = ElementTree.SubElement(out, 'relPosition')
  relPosition.set('x','21')
  relPosition.set('y','8')

def xmlContactCoilName(root, name):
  variable = ElementTree.SubElement(root, 'variable')
  variable.text = name

def xmlContactCoilSize(root):
  root.set('height','15')
  root.set('width','21')

def updateLocalId(root):
  global localId
  setLocalId(root, localId)
  localId = localId + 1

def setLocalId(root, newId):
  root.set('localId',str(newId))

def xmlLadder(root, ast):
  ladder = ElementTree.SubElement(root,'LD')
  xmlLeftTrail(ladder, ast)
  rightTrail = xmlRightTrail(ladder, ast)
  xmlLadderNet(ladder, rightTrail, ast)

def xmlTypes(root, ast):
  types = ElementTree.SubElement(root,'types')
  dataTypes = ElementTree.SubElement(types, 'dataTypes')
  pous = ElementTree.SubElement(types, 'pous')
  pou = ElementTree.SubElement(pous, 'pou')
  pou.set('name','instance0')
  pou.set('pouType','program')
  interface = ElementTree.SubElement(pou,'interface')
  body = ElementTree.SubElement(pou, 'body')
  xmlLadder(body, ast)

def xmlInstanceConfig(root):
  instances = ElementTree.SubElement(root,'instances')
  configurationList = ElementTree.SubElement(instances,'configurations')
  configuration = ElementTree.SubElement(configurationList,'configuration')
  configuration.set('name','config0')
  resource = ElementTree.SubElement(configuration,'resource')
  resource.set('name','resource1')
  task = ElementTree.SubElement(resource,'task')
  task.set('name','task0')
  task.set('priority','0')
  task.set('interval','T#20ms')
  pou = ElementTree.SubElement(task,'pouInstance')
  pou.set('name','instance0')
  pou.set('typeName','program0')

def xmlProject(ast):
  root = ElementTree.Element('project')
  root.set('xmlns','http://www.plcopen.org/xml/tc6_0201')
  root.set('xmlns:ns1','http://www.plcopen.org/xml/tc6.xsd')
  root.set('xmlns:xhtml','http://www.w3.org/1999/xhtml')
  root.set('xmlns:xsd','http://www.w3.org/2001/XMLSchema')

  xmlFileHeader(root)
  xmlContentHeader(root)
  xmlTypes(root,ast)
  xmlInstanceConfig(root)
  return root
