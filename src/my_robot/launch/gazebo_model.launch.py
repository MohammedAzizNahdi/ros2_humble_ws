import os
import xacro

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Nom du robot (doit correspondre au xacro)
    robotXacroName = 'differential_drive_robot'

    # Nom du package
    namePackage = 'my_robot'

    # Chemin relatif du fichier xacro
    modelFileRelativePath = 'model/robot.xacro'

    # Chemin relatif du monde Gazebo
    worldFileRelativePath = 'model/empty_world.world'


    # Chemin absolu du world
    pathWorldFile = os.path.join(
        get_package_share_directory(namePackage),
        worldFileRelativePath
    )


    # Chemin absolu du fichier xacro
    pathModelFile = os.path.join(
        get_package_share_directory(namePackage),
        modelFileRelativePath
    )


    # Conversion xacro en URDF
    robotDescription = xacro.process_file(
        pathModelFile
    ).toxml()


    # Lancement Gazebo Classic
    gazebo_rosPackageLaunch = PythonLaunchDescriptionSource(
        os.path.join(
            get_package_share_directory('gazebo_ros'),
            'launch',
            'gazebo.launch.py'
        )
    )


    gazeboLaunch = IncludeLaunchDescription(
        gazebo_rosPackageLaunch,
        launch_arguments={
            'world': pathWorldFile
        }.items()
    )


    # Spawn du robot dans Gazebo
    spawnModelNode = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic',
            'robot_description',
            '-entity',
            robotXacroName
        ],
        output='screen'
    )


    # Robot State Publisher
    nodeRobotStatePublisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robotDescription,
                'use_sim_time': True
            }
        ]
    )


    return LaunchDescription([
        gazeboLaunch,
        spawnModelNode,
        nodeRobotStatePublisher
    ])