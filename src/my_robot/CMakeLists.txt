cmake_minimum_required(VERSION 3.8)
project(my_robot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
# NOUVEAU : On ajoute les dépendances pour les capteurs
find_package(sensor_msgs REQUIRED) 

install(
  DIRECTORY launch model
  DESTINATION share/${PROJECT_NAME}
)

add_executable(publisher_node src/publisher_node.cpp)

ament_target_dependencies(publisher_node
  rclcpp
  std_msgs
)

add_executable(subscriber_node src/subscriber_node.cpp)

# NOUVEAU : On lie sensor_msgs à l'exécutable subscriber_node
ament_target_dependencies(subscriber_node
  rclcpp
  std_msgs
  sensor_msgs 
)

install(TARGETS
  publisher_node
  subscriber_node
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)

  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)

  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
