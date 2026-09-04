cmake_minimum_required(VERSION 3.8)

project(my_robot)


# ============================================================
# Compiler options
# ============================================================

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")

  add_compile_options(
    -Wall
    -Wextra
    -Wpedantic
  )

endif()


# ============================================================
# Dependencies
# ============================================================

find_package(ament_cmake REQUIRED)

find_package(rclcpp REQUIRED)

find_package(std_msgs REQUIRED)

find_package(sensor_msgs REQUIRED)


# ============================================================
# Install directories
# ============================================================

install(

  DIRECTORY
    launch
    model
    config

  DESTINATION
    share/${PROJECT_NAME}

)


# ============================================================
# Publisher
# ============================================================

add_executable(
  publisher_node
  src/publisher_node.cpp
)


ament_target_dependencies(

  publisher_node

  rclcpp
  std_msgs

)


# ============================================================
# Subscriber
# ============================================================

add_executable(
  subscriber_node
  src/subscriber_node.cpp
)


ament_target_dependencies(

  subscriber_node

  rclcpp
  std_msgs

)


# ============================================================
# Install executables
# ============================================================

install(

  TARGETS

    publisher_node
    subscriber_node

  DESTINATION
    lib/${PROJECT_NAME}

)


# ============================================================
# Testing
# ============================================================

if(BUILD_TESTING)

  find_package(ament_lint_auto REQUIRED)

  set(
    ament_cmake_copyright_FOUND
    TRUE
  )

  set(
    ament_cmake_cpplint_FOUND
    TRUE
  )

  ament_lint_auto_find_test_dependencies()

endif()


# ============================================================
# Package
# ============================================================

ament_package()