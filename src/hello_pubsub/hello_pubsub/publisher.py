import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Publisher(Node):

    def __init__(self):
        super().__init__('hello_publisher')

        self.publisher = self.create_publisher(
            String,
            'hello_topic',
            10
        )

        self.timer = self.create_timer(
            1,
            self.publish_message
        )


    def publish_message(self):

        msg = String()

        msg.data = "Hello World from Publisher"

        self.publisher.publish(msg)

        self.get_logger().info(
            "Publishing: " + msg.data
        )


def main(args=None):

    rclpy.init(args=args)

    node = Publisher()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()