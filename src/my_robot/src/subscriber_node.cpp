#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "sensor_msgs/msg/image.hpp"

class SensorSubscriber : public rclcpp::Node
{
public:
    SensorSubscriber() : Node("subscriber_node")
    {
        // 1. Abonnement au topic du LiDAR (/scan)
        lidar_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/scan", 10, std::bind(&SensorSubscriber::lidar_callback, this, std::placeholders::_1));

        // 2. Abonnement au topic de la Caméra (/camera/image_raw)
        camera_sub_ = this->create_subscription<sensor_msgs::msg::Image>(
            "/camera/image_raw", 10, std::bind(&SensorSubscriber::camera_callback, this, std::placeholders::_1));

        RCLCPP_INFO(this->get_logger(), "Nœud abonné aux capteurs démarré avec succès !");
    }

private:
    // Fonction appelée à chaque fois que le LiDAR envoie une mesure (10 fois par seconde)
    void lidar_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg)
    {
        // On récupère l'index du milieu du tableau pour avoir la distance juste en face du robot
        int center_index = msg->ranges.size() / 2;
        float distance_en_face = msg->ranges[center_index];
        
        RCLCPP_INFO(this->get_logger(), "LiDAR - Obstacle en face à : %.2f mètres", distance_en_face);
    }

    // Fonction appelée à chaque fois que la caméra envoie une image (30 fois par seconde)
    void camera_callback(const sensor_msgs::msg::Image::SharedPtr msg)
    {
        // On confirme la réception en affichant la résolution de l'image
        RCLCPP_INFO(this->get_logger(), "Caméra - Image reçue ! Résolution : %d x %d", msg->width, msg->height);
    }

    // Déclaration des pointeurs d'abonnement
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr lidar_sub_;
    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr camera_sub_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    // Lancement du nœud
    rclcpp::spin(std::make_shared<SensorSubscriber>());
    rclcpp::shutdown();
    return 0;
}