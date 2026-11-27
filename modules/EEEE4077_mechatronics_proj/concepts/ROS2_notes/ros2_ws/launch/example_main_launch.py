from pathlib import Path
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    colors = {
        'background_r': '200'
    }

    # Locate example_substitutions_launch.py in the same directory for direct workspace launching
    substitutions_launch_path = Path(__file__).resolve().parent / 'example_substitutions_launch.py'

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(substitutions_launch_path)),
            launch_arguments={
                'turtlesim_ns': 'turtlesim2',
                'use_provided_red': 'True',
                'new_background_r': colors['background_r'],
            }.items()
        )
    ])

