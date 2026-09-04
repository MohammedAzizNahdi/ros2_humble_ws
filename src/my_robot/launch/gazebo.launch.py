import os

import xacro

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription

from launch.actions import IncludeLaunchDescription

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    # ======================================================
    # Package
    # ======================================================

    package_name = "my_robot"

    package_path = get_package_share_directory(package_name)


    # ======================================================
    # Robot Xacro
    # ======================================================

    xacro_file = os.path.join(
        package_path,
        "model",
        "robot.xacro"
    )

    robot_description = xacro.process_file(
        xacro_file
    ).toxml()


    # ======================================================
    # Gazebo world
    # ======================================================

    world_file = os.path.join(
        package_path,
        "model",
        "empty_world.world"
    )


    gazebo_launch_file = os.path.join(
        get_package_share_directory("gazebo_ros"),
        "launch",
        "gazebo.launch.py"
    )


    # ======================================================
    # Gazebo
    # ======================================================

    gazebo = IncludeLaunchDescription(

        PythonLaunchDescriptionSource(
            gazebo_launch_file
        ),

        launch_arguments={
            "world": world_file
        }.items()

    )


    # ======================================================
    # Robot State Publisher
    # ======================================================

    robot_state_publisher = Node(

        package="robot_state_publisher",

        executable="robot_state_publisher",

        name="robot_state_publisher",

        output="screen",

        parameters=[

            {
                "robot_description": robot_description,
                "use_sim_time": True
            }

        ]

    )


    # ======================================================
    # Spawn robot
    # ======================================================

    spawn_entity = Node(

        package="gazebo_ros",

        executable="spawn_entity.py",

        arguments=[

            "-topic",
            "robot_description",

            "-entity",
            "differential_drive_robot"

        ],

        output="screen"

    )


    # ======================================================
    # RViz
    # ======================================================

    rviz_config = os.path.join(
        package_path,
        "config",
        "robot.rviz"
    )


    rviz = Node(

        package="rviz2",

        executable="rviz2",

        name="rviz2",

        arguments=[
            "-d",
            rviz_config
        ],

        parameters=[
            {
                "use_sim_time": True
            }
        ],

        output="screen"

    )


    # ======================================================
    # Launch
    # ======================================================

    return LaunchDescription([

        gazebo,

        robot_state_publisher,

        spawn_entity,

        rviz

    ])