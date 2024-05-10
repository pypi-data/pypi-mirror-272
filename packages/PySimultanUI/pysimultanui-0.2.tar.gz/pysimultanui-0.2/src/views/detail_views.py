import numpy as np
import pandas as pd
from pandas import DataFrame
# import pandas as pd

from nicegui import ui, app
from logging import getLogger
from PySimultan2.simultan_object import SimultanObject
from PySimultan2.geometry import GeometryModel
# from PySimultan2.default_types import ComponentDictionary, ComponentList

from SIMULTAN.Data.MultiValues import (SimMultiValueField3D, SimMultiValueField3DParameterSource, SimMultiValueBigTable,
                                       SimMultiValueBigTableHeader, SimMultiValueBigTableParameterSource)

from .. import user_manager

from .pandas_df_view import DataFrameDetailView
from .numpy_view import NDArrayDetailView
from .geometry_view.geometry_view import GeometryDetailView


logger = getLogger('py_simultan_ui')


def show_next_detail(*args, **kwargs):
    user = user_manager[app.storage.user['username']]
    show_detail(value=user.detail_history.move_next(), *args, **kwargs)


def show_previous_detail(*args, **kwargs):
    user = user_manager[app.storage.user['username']]
    show_detail(value=user.detail_history.move_previous(), *args, **kwargs)


def show_detail(value, *args, **kwargs):
    user = user_manager[app.storage.user['username']]
    user.detail_history.add_item(value)
    if len(user.detail_history) > 10:
        user.detail_history.pop(0)
        user.detail_history_index = len(user.detail_history)
    # current_detail = user.detail_history[-1] if user.detail_history else None
    logger.debug(f'Showing details for {value}')
    user.detail_view.clear()
    with user.detail_view:
        with ui.card().classes('w-full h-full'):
            with ui.row():
                if user.detail_history.get_previous_detail() is not None:
                    ui.button(on_click=show_previous_detail(),
                              icon='arrow_back').classes('q-mr-md')
                ui.space()
                if user.detail_history.get_next_detail() is not None:
                    ui.button(on_click=show_next_detail(),
                              icon='arrow_forward').classes('q-mr-md')

            user.current_detail = value

            if isinstance(value, SimMultiValueBigTable):
                detail_view = DataFrameDetailView(component=value, **kwargs).ui_content()
            elif isinstance(value, SimMultiValueField3D):
                detail_view = NDArrayDetailView(component=value, **kwargs).ui_content()
            elif isinstance(value, GeometryModel):
                detail_view = GeometryDetailView(component=value, **kwargs).ui_content()
            else:
                cls_view = user.view_manager.cls_views.get(value.__class__, None)
                if cls_view is None:
                    ui.label(f'No view for {value.__class__}')
                    return
                type_view = cls_view.get('type_view', None)
                if type_view is None:
                    ui.label(f'No type view for {value.__class__}')
                    return
                if not hasattr(type_view, 'detail_view'):
                    ui.label(f'No detail view for {value.__class__}')
                    return
                detail_view = type_view.detail_view

            detail_view(component=value, *args, **kwargs).ui_content()
