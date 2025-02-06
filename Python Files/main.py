import flet as ft
import petri2ladder_cli as p2l
from flet import FilePicker, FilePickerResultEvent, TextField, ElevatedButton, Page, Row, Column, VerticalDivider, \
    MainAxisAlignment, CrossAxisAlignment, Image
import graphviz
import base64
from io import BytesIO
import xml.etree.ElementTree as ET


def main(page: Page):
    page.title = "Conversor de PNML"
    page.window_width = 1600
    page.window_height = 900

    origin_file_path = ""
    destination_file_path = ""

    xml_content = TextField(label="Arquivo XML (PNML)", multiline=True, width=700, height=400)
    graph_image = Image(width=600, height=800)

    def show_dialog(title, text):
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(text),
            actions=[ft.TextButton("Clique fora da caixa para sair", on_click=lambda e: close_dialog(dialog, page))],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def close_dialog(dialog, page):
        dialog.open = False
        page.overlay.remove(dialog)
        page.update()

    def on_file_picker_result(e: FilePickerResultEvent):
        nonlocal origin_file_path, destination_file_path
        if e.files:
            try:
                with open(e.files[0].path, 'r') as file:
                    origin_file_path = e.files[0].path
                    diretorio, _, _ = origin_file_path.rpartition("\\")
                    destination_file_path = f"{diretorio}\\plc.xml"
                    xml_content.value = file.read()
                page.update()
                display_graph(xml_content.value)
            except Exception as ex:
                print(f"Erro ao ler o arquivo: {ex}")

    def on_convert_click(e):
        if not origin_file_path:
            show_dialog("Erro", "Selecione um arquivo antes de iniciar a conversão")
            return

        if xml_content.value:
            try:
                p2l.petri2ladder(origin_file_path, destination_file_path)
                print("Sucesso na conversão do arquivo")
                show_dialog("Sucesso", "O arquivo xml foi gerado e salvo!")
            except Exception as ex:
                print(f"Erro na conversão do arquivo: {ex.stderr}")

    def display_graph(xml_str):
        try:
            dot = pnml_to_dot(xml_str)
            print(f"DOT: {dot}")
            graph = graphviz.Source(dot)
            img = BytesIO()
            img.write(graph.pipe(format='png'))
            img.seek(0)
            img_data = base64.b64encode(img.read()).decode('utf-8')
            graph_image.src_base64 = img_data
            page.update()
        except Exception as ex:
            print(f"Erro ao exibir o gráfico: {ex}")

    def pnml_to_dot(xml_str):
        try:
            root = ET.fromstring(xml_str)
            dot = ['digraph G {']
            dot.append('    rankdir=TB;')

            # Mapeia os nós
            nodes = {}
            for place in root.findall(".//place"):
                place_id = place.get('id')
                nodes[place_id] = place_id
                dot.append(f'    {place_id} [shape=circle,label="{place_id}"];')

            for transition in root.findall(".//transition"):
                transition_id = transition.get('id')
                nodes[transition_id] = transition_id
                dot.append(f'    {transition_id} [shape=box,label="{transition_id}"];')
         
            top_node = "P0" if "P0" in nodes else "P1" if "P1" in nodes else None
            if top_node:
                dot.append(f'    {{rank=source; {top_node};}}')

            # Mapeia as arestas
            for arc in root.findall(".//arc"):
                source = arc.get('source')
                target = arc.get('target')
                dot.append(f'    {source} -> {target};')

            dot.append('}')
            return '\n'.join(dot)
        except Exception as ex:
            print(f"Erro ao converter PNML para DOT: {ex}")
            return ""

    file_picker = FilePicker(on_result=on_file_picker_result)
    page.overlay.append(file_picker)

    btn_select_file = ElevatedButton(text="Selecionar Arquivo XML", on_click=lambda _: file_picker.pick_files())
    btn_convert = ElevatedButton(text="Converter Arquivo", on_click=on_convert_click)

    page.add(
        Row(
            [
                Column(
                    [
                        btn_select_file,
                        xml_content,
                        btn_convert
                    ],
                    alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                ),
                VerticalDivider(),
                Column(
                    [
                        graph_image
                    ],
                    alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                ),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            height=1080
        )
    )


ft.app(target=main)
