from nicegui import ui

from ..type_view import TypeView
from nicegui import ui, app

from ..detail_views import show_detail
from ... import user_manager
from ...core.edit_dialog import DictEditDialog
from PySimultan2.simultan_object import SimultanObject
from PySimultan2.default_types import ComponentDictionary

from ..parameter_view import ParameterView
from ..mapped_cls.mapped_cls_view import ContentItemView


class DictItemView(object):

    def __init__(self, *args, **kwargs):
        self.component: SimultanObject = kwargs.get('component')
        self.parent = kwargs.get('parent')
        self.key = kwargs.get('key')

    @property
    def view_manager(self):
        return self.parent.view_manager

    @ui.refreshable
    def ui_content(self):
        with ui.item().classes('w-full h-full'):
            with ui.item_section():
                ui.label(f'{self.key}:')

            val = self.component
            if isinstance(val, SimultanObject):
                if val.__ui_element__ is None:
                    self.view_manager.cls_views[val.__class__]['item_view_manager'].add_item_to_view(val)
                with ui.item_section():
                    ui.label(f'{val.name}')
                    ui.button('Details', on_click=lambda e: show_detail(val))
                with ui.item_section():
                    ui.label(f'{val.id}')
            elif isinstance(val, (int, float, str)):
                with ui.item_section():
                    raw_val = self.parent.component.get_raw_attr(self.key)
                    ParameterView(component=val,
                                  raw_val=raw_val,
                                  parent=self).ui_content()
            else:
                with ui.item_section():
                    if hasattr(val, 'name'):
                        ui.label(f'{val.name}:')
                    else:
                        ui.label('No Name')
                with ui.item_section():
                    if hasattr(val, 'id'):
                        ui.label(f'{val.id}:')
                    else:
                        ui.label('No ID')

    def edit(self, event):
        ui.notify('Edit not implemented yet', type='negative')
        raise NotImplementedError

    def remove(self, event):
        ui.notify('Edit not implemented yet', type='negative')
        raise NotImplementedError


class DictView(object):

    def __init__(self, *args, **kwargs):
        self.component: ComponentDictionary = kwargs.get('component')
        self.parent = kwargs.get('parent')
        self.card = None

        self.content_item_views: dict[str: ContentItemView] = {}

    @property
    def view_manager(self):
        return self.parent.view_manager

    @ui.refreshable
    def list_content(self):
        with ui.list().classes('w-full h-full'):

            for key, value in self.component.items():
                if self.content_item_views.get(key, None) is None or self.content_item_views[key].component != value:
                    self.content_item_views[key] = DictItemView(component=value,
                                                                parent=self,
                                                                key=key)
                try:
                    self.content_item_views[key].ui_content()
                    ui.separator()
                except Exception as e:
                    print(e)
                    ui.label(f'Could not display {key}: {value}')

        ui.button(f'Add new item to {self.component.name}',
                  on_click=self.parent.add_new_item, icon='add').classes('q-ml-auto')

    @ui.refreshable
    def ui_content(self):
        with ui.expansion(icon='format_list_bulleted',
                          text=f'Content ({len(self.component)})',
                          value=True
                          ).classes('w-full h-full').bind_text_from(self,
                                                                    'data',
                                                                    lambda x: f'Content ({len(self.component)})'
                                                                    ) as self.card:
            self.list_content()


class DictDetailView(object):

    def __init__(self, *args, **kwargs):
        self.component: ComponentDictionary = kwargs.get('component')
        self.parent = kwargs.get('parent')
        self.card = None

        self.content_view = DictView(component=self.component, parent=self)

    def add_new_item(self, event):
        self.parent.add_new_item(event)

    def ui_content(self, *args, **kwargs):
        with ui.row().classes('w-full h-full'):
            ui.input(label='Name', value=self.component.name).bind_value(self.component, 'name')

        with ui.row().classes('w-full h-full'):
            ui.label('ID: ')
            with ui.row():
                with ui.row():
                    ui.label(f'{self.component.Id.GlobalId.ToString()}')
                with ui.row():
                    ui.label(f'{self.component.Id.LocalId}')

        content_view = DictView(component=self.component, parent=self)
        content_view.ui_content()

    def refresh(self):
        self.ui_content()


class ComponentDictView(TypeView):

    detail_view = DictDetailView

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def view_manager(self):
        return self.parent.view_manager

    @ui.refreshable
    def ui_content(self):

        with ui.card().classes(f"{self.colors['item']} w-full h-full") as self.card:
            self.card.on('click', show_detail(self.component,
                                              parent=self.parent)
                         )
            with ui.row().classes(f"{self.colors['item']} w-full") as self.row:
                self.row.on('click', show_detail(self.component,
                                                 parent=self.parent)
                            )
                self.checkbox = ui.checkbox(on_change=self.select)
                ui.input(label='Name', value=self.component.name).bind_value(self.component, 'name')
                ui.label(f'{str(self.component.id)}')

    def add_new_item(self, event):

        parent = self

        component = self.component
        edit_dialog = DictEditDialog(component=None,
                                     key=None,
                                     parent=self,
                                     options=['Component'])

        def save(self, *args, **kwargs):

            edit_diag = edit_dialog.edit_dialog.edit_dialog

            value = edit_diag.value
            key = edit_dialog.key
            component[key] = value

            if value in [int, float]:
                raw_val = component[key]
                setattr(raw_val, 'ValueMin', edit_diag.min)
                setattr(raw_val, 'ValueMax', edit_diag.max)
                setattr(raw_val, 'Unit', edit_diag.unit)

            parent.content_view.ui_content.refresh()
            edit_dialog.close()

        edit_dialog.save = save
        edit_dialog.create_edit_dialog()

    def show_details(self, *args, **kwargs):
        self.detail_view(component=self.component,
                         parent=self).ui_content()
