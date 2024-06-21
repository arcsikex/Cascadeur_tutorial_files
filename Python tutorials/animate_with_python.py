import csc
import numpy

framerate = 30
num_frames = 90
amplitude = 100
cycle_duration = 1  # sec


def calculate_cube_path(framerate, num_frames, amplitude, cycle_duration):
    angular_frequency = 2 * numpy.pi / cycle_duration
    path_coordinates = []

    for frame in range(num_frames):
        time = frame / framerate
        x = frame * 10
        y = amplitude * numpy.sin(angular_frequency * time)
        path_coordinates.append(numpy.array([x, y, 0]))

    return path_coordinates


motion_path = calculate_cube_path(framerate, num_frames, amplitude, cycle_duration)

# Required viewers
model_viewer = scene.model_viewer()
layer_viewer = scene.layers_viewer()
behaviour_viewer = scene.behaviour_viewer()

cube_id = model_viewer.get_objects("Cube")[0]
layer_id = layer_viewer.layer_id_by_obj_id(cube_id)

transform_behaviour = behaviour_viewer.get_behaviour_by_name(cube_id, "Transform")
global_position_id = behaviour_viewer.get_behaviour_data(
    transform_behaviour, "global_position"
)


def move_cube(model_editor, update_editor, scene_updater):
    data_editor = model_editor.data_editor()
    layers_editor = model_editor.layers_editor()

    for frame, coordinate in enumerate(motion_path):
        layers_editor.set_fixed_interpolation_or_key_if_need(layer_id, frame, True)
        model_editor.fit_animation_size_by_layers()
        data_editor.set_data_value(global_position_id, frame=frame, value=coordinate)
        scene_updater.run_update({global_position_id}, frame)


scene.modify_update("Move the cube", move_cube)
