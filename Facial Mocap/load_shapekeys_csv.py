import csc
import csv
import os
from typing import Optional, Tuple
from scipy.signal import savgol_filter

window_length = 5  # Must be an odd number, and greater than polyorder
polyorder = 3

def command_name():
    return "Import Facial Mocap CSV"


def get_selected_object(scene) -> csc.model.ObjectId:
    """
    Return the object id of the selected object

    :raises ValueError: If there is not exactly one object selected
    :return csc.model.ObjectId: Object ID of the selected object
    """
    selected_objects = {
        sid
        for sid in scene.selector().selected().ids
        if isinstance(sid, csc.model.ObjectId)
    }
    if len(selected_objects) == 1:
        return next(iter(selected_objects))
    elif len(selected_objects) == 0:
        raise ValueError("No object selected.")
    else:
        raise ValueError("More than one object selected.")


def run(scene):
    """
    Main function for setting blendshape values using CSV data and filtering.
    """
    scene = csc.app.get_application().current_scene().domain_scene()
    layer_viewer = scene.layers_viewer()
    model_viewer = scene.model_viewer()
    data_viewer = scene.data_viewer()
    behaviour_viewer = model_viewer.behaviour_viewer()
    mesh_id = get_selected_object(scene)
    layer_id = layer_viewer.layer_id_by_obj_id(mesh_id)
    filename = None

    def get_data_id_by_name(shape_key: str) -> Optional[csc.model.DataId]:
        """
        Retrieve the DataId of a blendshape by name (case-insensitive match).
        """
        blendshape_behaviour = behaviour_viewer.get_behaviour_by_name(
            mesh_id, "Dynamic"
        )
        blendshape_data = behaviour_viewer.get_behaviour_data_range(
            blendshape_behaviour, "datas"
        )
        blendshape_names = behaviour_viewer.get_behaviour_data_range(
            blendshape_behaviour, "dataNames"
        )

        for name_id, value_id in zip(blendshape_names, blendshape_data):
            name = data_viewer.get_data(name_id).name
            if shape_key.lower() in name.lower():
                return value_id
        return None

    def read_and_process_csv() -> Tuple[list, list]:
        """
        Read the CSV file and process the data by applying the Savitzky-Golay filter.
        """
        with open(filename, "r") as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)[1:]  # Skip first column (timestamp)
            data = [
                [float(value) if value else None for value in row[1:]]
                for row in csv_reader
            ]

        columns = list(zip(*data))  # Transpose rows to columns for filtering
        filtered_columns = [
            savgol_filter(column, window_length=window_length, polyorder=polyorder)
            for column in columns
        ]
        return headers, list(zip(*filtered_columns))  # Transpose back to rows

    def set_shapekey(model_editor, update_editor, scene_updater):
        """
        Set shapekey values in the scene based on the filtered CSV data.
        """
        if not filename:
            return
        data_editor = model_editor.data_editor()
        layers_editor = model_editor.layers_editor()

        headers, filtered_data = read_and_process_csv()

        for frame, row in enumerate(filtered_data):
            for header, cell in zip(headers[2:], row[2:]):
                try:
                    value = float(cell) * 100
                    value_id = get_data_id_by_name(header)
                    if not value_id:
                        continue
                    layers_editor.set_fixed_interpolation_or_key_if_need(
                        layer_id, frame, True
                    )
                    model_editor.fit_animation_size_by_layers()
                    data_editor.set_data_value(value_id, frame=frame, value=value)
                    scene_updater.run_update({value_id}, frame)
                except ValueError:
                    print(f"Skipping malformed element: {header}")
        scene.success("Finished importing Facial Mocap")

    def show_path(path):
        """
        Handle file path selection and prompt the user for filter settings.
        """
        nonlocal filename
        scene.info(path)
        filename = path

        csc.view.DialogManager.instance().show_inputs_dialog(
            "Smoothing (Savitzky-Golay filter)",
            ["Polyorder", "Window Length (odd number, and greater than polyorder)"],
            [str(polyorder), str(window_length)],
            2,
            set_filter_options,
        )

    def set_filter_options(values):
        """
        Set filter options based on user input and trigger the shapekey update.
        """
        global polyorder, window_length

        if values:
            polyorder = int(values[0])
            window_length = int(values[1])

            if polyorder >= window_length:
                scene.warning("Window length must be greater than polyorder!")
                return
            if window_length % 2 == 0:
                scene.warning("Window length must be an odd number!")
                return

            scene.modify_update("Set Shapekey", set_shapekey)

    # File dialog manager to select the CSV file
    file_dialog_manager = csc.app.get_application().get_file_dialog_manager()
    file_dialog_manager.show_save_file_dialog("Choose file", "", ["*.csv"], show_path)

    # Trigger modification after file selection
    scene.modify_update("Set Shapekey", set_shapekey)

