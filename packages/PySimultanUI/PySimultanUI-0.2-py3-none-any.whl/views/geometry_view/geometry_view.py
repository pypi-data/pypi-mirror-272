import os

from PySimultan2.geometry import GeometryModel
from nicegui import ui, events, app

# from ..detail_views import show_detail
from .tools import create_stl_file
from ..type_view import TypeView
from ... import user_manager

if not os.path.exists('/static/stl'):
    os.makedirs('/static/stl')

app.add_static_files('/stl', '/static/stl')


class GeometryDetailView(object):

    def __init__(self, *args, **kwargs):
        self.component: GeometryModel = kwargs.get('component')
        self.parent: GeometryView = kwargs.get('parent')

    @property
    def geometry_model(self) -> GeometryModel:
        return self.component

    def ui_content(self, *args, **kwargs):
        with ui.row():
            ui.input(label='Name', value=self.component.name).bind_value(self.component, 'name')

        with ui.row():
            ui.label('Key:')
            ui.label(self.geometry_model.key)

        show_geo_button = ui.button('Show Geometry', on_click=self.show_geometry)

        with ui.expansion(icon='format_list_bulleted',
                          text=f'Geometry ({len(self.geometry_model.vertices)})').classes(
            'w-full h-full'):

            with ui.expansion(icon='format_list_bulleted',
                              text=f'Vertices ({len(self.geometry_model.vertices)})').classes(
                'w-full h-full') as exp:
                with ui.list().classes('w-full h-full'):
                    for vertex in self.geometry_model.vertices:
                        with ui.item():
                            with ui.item_section():
                                ui.label(f'Vertex {vertex.id}')
                            with ui.item_section():
                                ui.label(f'x: {vertex.x}')
                            with ui.item_section():
                                ui.label(f'y: {vertex.y}')
                            with ui.item_section():
                                ui.label(f'z: {vertex.z}')

            with ui.expansion(icon='format_list_bulleted',
                              text=f'Edges ({len(self.geometry_model.edges)})').classes(
                'w-full h-full') as exp:
                with ui.list().classes('w-full h-full'):
                    for edge in self.geometry_model.edges:
                        with ui.item():
                            with ui.item_section():
                                ui.label(f'Edge {edge.id}')
                            with ui.item_section():
                                ui.label(f'Vertex 1: {edge.vertex_0.id}')
                            with ui.item_section():
                                ui.label(f'Vertex 2: {edge.vertex_1.id}')
                            with ui.item_section():
                                ui.label(f'Length: {edge.length}')

            with ui.expansion(icon='format_list_bulleted',
                              text=f'Faces ({len(self.geometry_model.faces)})').classes('w-full h-full') as exp:
                with ui.list().classes('w-full h-full'):
                    for face in self.geometry_model.faces:
                        with ui.item():
                            with ui.item_section():
                                ui.label(f'Face {face.id}')
                            with ui.item_section():
                                ui.label(f'Area: {face.area}')

            with ui.expansion(icon='format_list_bulleted',
                              text=f'Volumes ({len(self.geometry_model.volumes)})').classes(
                'w-full h-full') as exp:
                with ui.list().classes('w-full h-full'):
                    for volume in self.geometry_model.volumes:
                        with ui.item():
                            with ui.item_section():
                                ui.label(f'Volume {volume.id}')
                            with ui.item_section():
                                ui.label(f'Volume: {volume.volume}')

        delete_button = ui.button('Delete', on_click=self.delete_model)

    def delete_model(self, *args, **kwargs):
        ui.notify('Delete not implemented yet', type='negative')

    def show_geometry(self):
        # create dialog with geometry
        with ui.dialog() as dialog, ui.card().classes('w-full h-full'):
            file_lookup = create_stl_file(self.geometry_model)
            with ui.scene(on_click=self.handle_click).classes('w-full h-full') as self.scene_3d:
                self.scene_3d.spot_light(distance=100, intensity=0.5).move(-10, 0, 10)
                for f_id, f in file_lookup.items():
                    self.scene_3d.stl(f[0]).with_name(str(f_id)).material(f[1])

            ui.button('Cancel', on_click=dialog.close)

        dialog.open()

    def handle_click(self, e: events.SceneClickEventArguments, *args, **kwargs):
        hit = e.hits[0]
        name = hit.object_name or hit.object_id
        ui.notify(f'You clicked on the {name} at ({hit.x:.2f}, {hit.y:.2f}, {hit.z:.2f})')

    def refresh(self):
        self.ui_content()


class GeometryView(TypeView):

    detail_view = GeometryDetailView

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def geometry_model(self) -> GeometryModel:
        return self.component

    @ui.refreshable
    def ui_content(self):
        from ..detail_views import show_detail
        with ui.card().classes(f"{self.colors['item']} w-full h-full") as self.card:
            self.card.on('click', lambda e: show_detail(value=self.component,
                                                        parent=self)
                         )
            with ui.row().classes('h-full w-full') as self.row:
                self.row.on('click', lambda e: show_detail(value=self.component,
                                                           parent=self)
                            )
                self.checkbox = ui.checkbox(on_change=self.select)
                ui.label('Name:')
                ui.label(self.geometry_model.name)
                ui.label('Key:')
                ui.label(self.geometry_model.key)

    def delete_model(self, *args, **kwargs):
        ui.notify('Delete not implemented yet', type='negative')
