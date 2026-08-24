from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_robot',
            executable='publisher_node',
            name='publisher_node',
            output='screen'
        ),
        Node(
            package='my_robot',
            executable='subscriber_node',
            name='subscriber_node',
            output='screen'
        )
    ])