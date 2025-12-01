import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

cv2.startWindowThread()
cv2.namedWindow("Camera View", cv2.WINDOW_AUTOSIZE)

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_sub')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image,
            '/raspicam/image_raw',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2.imshow("Camera View", cv_image)
        cv2.waitKey(1)

rclpy.init()
node = CameraSubscriber()
rclpy.spin(node)
rclpy.shutdown()
