#!/usr/bin/env python

# Copyright 1996-2023 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Launch Webots TurtleBot3 Burger driver."""

import os
import pathlib
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.substitutions.path_join_substitution import PathJoinSubstitution
from launch import LaunchDescription
from launch_ros.actions import Node
import launch
from ament_index_python.packages import get_package_share_directory, get_packages_with_prefixes
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.wait_for_controller_connection import WaitForControllerConnection
from webots_ros2_driver.utils import controller_url_prefix


# def get_ros2_nodes(*args):
#     package_dir = get_package_share_directory('my_turtlebot')
#     use_nav = LaunchConfiguration('nav', default=False)
#     use_slam = LaunchConfiguration('slam', default=False)
#     robot_description = pathlib.Path(os.path.join(package_dir, 'resource', 'my_turtlebot.urdf')).read_text()
#     ros2_control_params = os.path.join(package_dir, 'resource', 'ros2control.yml')
#     nav2_params = os.path.join(package_dir, 'resource', 'nav2_params.yaml')
#     nav2_map = os.path.join(package_dir, 'resource', 'turtlebot3_burger_example_map.yaml')
#     use_sim_time = LaunchConfiguration('use_sim_time', default=True)

#     # TODO: Revert once the https://github.com/ros-controls/ros2_control/pull/444 PR gets into the release
#     # ROS control spawners
#     controller_manager_timeout = ['--controller-manager-timeout', '50']
#     controller_manager_prefix = 'python.exe' if os.name == 'nt' else ''
#     diffdrive_controller_spawner = Node(
#         package='controller_manager',
#         executable='spawner',
#         output='screen',
#         prefix=controller_manager_prefix,
#         arguments=['diffdrive_controller'] + controller_manager_timeout,
#     )
#     joint_state_broadcaster_spawner = Node(
#         package='controller_manager',
#         executable='spawner',
#         output='screen',
#         prefix=controller_manager_prefix,
#         arguments=['joint_state_broadcaster'] + controller_manager_timeout,
#     )
#     ros_control_spawners = [diffdrive_controller_spawner, joint_state_broadcaster_spawner]

#     mappings = [('/diffdrive_controller/cmd_vel_unstamped', '/cmd_vel')]
#     if 'ROS_DISTRO' in os.environ and os.environ['ROS_DISTRO'] in ['humble', 'rolling']:
#         mappings.append(('/diffdrive_controller/odom', '/odom'))

#     turtlebot_driver = Node(
#         package='webots_ros2_driver',
#         executable='driver',
#         output='screen',
#         additional_env={'WEBOTS_CONTROLLER_URL': controller_url_prefix() + 'TurtleBot3Burger'},
#         parameters=[
#             {'robot_description': robot_description,
#              'use_sim_time': use_sim_time,
#              'set_robot_state_publisher': True},
#             ros2_control_params
#         ],
#         remappings=mappings
#     )

#     robot_state_publisher = Node(
#         package='robot_state_publisher',
#         executable='robot_state_publisher',
#         output='screen',
#         parameters=[{
#             'robot_description': '<robot name=""><link name=""/></robot>'
#         }],
#     )

#     footprint_publisher = Node(
#         package='tf2_ros',
#         executable='static_transform_publisher',
#         output='screen',
#         arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'base_footprint'],
#     )

#     # Navigation
#     navigation_nodes = []
#     os.environ['TURTLEBOT3_MODEL'] = 'burger'
#     if 'turtlebot3_navigation2' in get_packages_with_prefixes():
#         turtlebot_navigation = IncludeLaunchDescription(
#             PythonLaunchDescriptionSource(os.path.join(
#                 get_package_share_directory('turtlebot3_navigation2'), 'launch', 'navigation2.launch.py')),
#             launch_arguments=[
#                 ('map', nav2_map),
#                 ('params_file', nav2_params),
#                 ('use_sim_time', use_sim_time),
#             ],
#             condition=launch.conditions.IfCondition(use_nav))
#         navigation_nodes.append(turtlebot_navigation)

#     # SLAM
#     if 'turtlebot3_cartographer' in get_packages_with_prefixes():
#         turtlebot_slam = IncludeLaunchDescription(
#             PythonLaunchDescriptionSource(os.path.join(
#                 get_package_share_directory('turtlebot3_cartographer'), 'launch', 'cartographer.launch.py')),
#             launch_arguments=[
#                 ('use_sim_time', use_sim_time),
#             ],
#             condition=launch.conditions.IfCondition(use_slam))
#         navigation_nodes.append(turtlebot_slam)

#     # Wait for the simulation to be ready to start navigation nodes
#     waiting_nodes = WaitForControllerConnection(
#         target_driver=turtlebot_driver,
#         nodes_to_start=navigation_nodes + ros_control_spawners
#     )

#     return [
#         robot_state_publisher,
#         turtlebot_driver,
#         footprint_publisher,
#         waiting_nodes,
#     ]


def generate_launch_description() -> LaunchDescription:
    package_dir = get_package_share_directory('my_turtlebot')
    use_nav = LaunchConfiguration('nav', default=False)
    use_slam = LaunchConfiguration('slam', default=False)
    rviz_config_file = os.path.join(package_dir, 'config', 'rviz_config.rviz')
    nav2_params = os.path.join(package_dir, 'resource', 'nav2_params.yaml')
    nav2_map = os.path.join(package_dir, 'resource', 'turtlebot3_burger_example_map.yaml')
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)

    footprint_publisher = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'base_footprint'],
    )
    navigation_nodes = []
    os.environ['TURTLEBOT3_MODEL'] = 'burger'
    if 'turtlebot3_navigation2' in get_packages_with_prefixes():
        turtlebot_navigation = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(
                get_package_share_directory('turtlebot3_navigation2'), 'launch', 'navigation2.launch.py')),
            launch_arguments=[
                ('map', nav2_map),
                ('params_file', nav2_params),
                ('use_sim_time', use_sim_time),
            ],
            condition=launch.conditions.IfCondition(use_nav))
        navigation_nodes.append(turtlebot_navigation)

    # SLAM
    cartographer_config_dir = os.path.join(package_dir, 'config')
    configuration_basename = 'carto_params.lua'
    resolution = '0.05'
    publish_period_sec = '1.0'

    cartographer_node = Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=['-configuration_directory', cartographer_config_dir,
                       '-configuration_basename', configuration_basename])
    cartographer_occupency_grid_node = Node(
            package='cartographer_ros',
            executable='occupancy_grid_node',
            name='occupancy_grid_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=['-resolution', resolution,
                       '-publish_period_sec', publish_period_sec])
    rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen')

    return LaunchDescription([
        # webots,
        footprint_publisher,
    ])
