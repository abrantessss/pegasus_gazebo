#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable, RegisterEventHandler, LogInfo, IncludeLaunchDescription, OpaqueFunction
from launch.event_handlers import OnProcessExit
from launch.conditions import LaunchConfigurationEquals
from launch.conditions import LaunchConfigurationEquals
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def launch_vehicle(context, *args, **kwargs):
    
    pegasus_models_dir = get_package_share_directory('pegasus_gazebo')
    
    # Spawn the 3D model in the gazebo world (it requires that a gzserver is already running)
    spawn_3d_model = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=['-entity', 'aruco_cube', 
               '-file', os.path.join(pegasus_models_dir, 'models/aruco_cube/model.sdf'),
               '-x', LaunchConfiguration('x').perform(context),
               '-y', LaunchConfiguration('y').perform(context),
               '-z', LaunchConfiguration('z').perform(context),
               '-R', LaunchConfiguration('R').perform(context),
               '-P', LaunchConfiguration('P').perform(context),
               '-Y', LaunchConfiguration('Y').perform(context)],
        output='screen'
    )

    return [spawn_3d_model]


def generate_launch_description():
    """Launch Gazebo with a drone running PX4 communicating over ROS 2."""
            
    # ---------------------------------------------------------------------
    # Create the Processes that need to be launched to simulate the vehicle
    # ---------------------------------------------------------------------

    return LaunchDescription([
        

        # Define where to spawn the vehicle (in the inertial frame) 
        # TODO - receive coordinates in ned perform the conversion to ENU and f.l.u here
        # so that the user only needs to work in NED coordinates
        DeclareLaunchArgument('x', default_value='0.0', description='X position expressed in ENU'),
        DeclareLaunchArgument('y', default_value='0.0', description='Y position expressed in ENU'),
        DeclareLaunchArgument('z', default_value='0.0', description='Z position expressed in ENU'),
        DeclareLaunchArgument('R', default_value='0.0', description='Roll orientation expressed in ENU'),
        DeclareLaunchArgument('P', default_value='0.0', description='Pitch orientation expressed in ENU'),
        DeclareLaunchArgument('Y', default_value='0.0', description='Yaw orientation expressed in ENU'),

        # Default to launch the pegasus control stack with the default configurations for the iris vehicle
        OpaqueFunction(function=launch_vehicle)
])