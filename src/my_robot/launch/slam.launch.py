import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription

from launch_ros.actions import Node


def generate_launch_description():

    # ======================================================
    # Package
    # ======================================================

    package_name = "my_robot"

    package_path = get_package_share_directory(package_name)


    # ======================================================
    # SLAM Toolbox configuration
    # ======================================================

    slam_config = os.path.join(
        package_path,
        "config",
        "slam_toolbox.yaml"
    )


    # ======================================================
    # SLAM Toolbox
    # ======================================================

    slam_toolbox = Node(

        package="slam_toolbox",

        executable="async_slam_toolbox_node",

        name="slam_toolbox",

        output="screen",

        parameters=[
            slam_config
        ]

    )


    # ======================================================
    # Launch
    # ======================================================

    return LaunchDescription([

        slam_toolbox

    ])