import xml.etree.ElementTree as ET


def convert_to_beremiz_format(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Criar a estrutura XML esperada pelo Beremiz
    project = ET.Element("project")
    configurations = ET.SubElement(project, "configurations")
    configuration = ET.SubElement(configurations, "configuration")
    resource = ET.SubElement(configuration, "resource")
    tasks = ET.SubElement(resource, "tasks")
    task = ET.SubElement(tasks, "task", name="MainTask", interval="100ms")
    program = ET.SubElement(task, "program", name="MainProgram", type="Ladder")
    ldProgram = ET.SubElement(program, "ldProgram")

    # Adicionar os elementos do arquivo original ao novo formato
    for rung in root.findall(".//rung"):
        new_rung = ET.SubElement(ldProgram, "rung")
        for coil in rung.findall(".//coil"):
            ET.SubElement(new_rung, "coil", variable=coil.get("variable"))
        for contact in rung.findall(".//contact"):
            ET.SubElement(new_rung, "contact", variable=contact.get("variable"))

    tree = ET.ElementTree(project)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


# Exemplo de uso
convert_to_beremiz_format("petrinetfile.xml", "beremizladder.xml")
