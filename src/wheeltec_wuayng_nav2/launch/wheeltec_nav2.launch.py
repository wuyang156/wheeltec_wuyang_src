import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    wheeltec_robot_dir = get_package_share_directory('turn_on_wheeltec_robot')
    wheeltec_launch_dir = os.path.join(wheeltec_robot_dir, 'launch')

    wheeltec_nav_dir = get_package_share_directory('wheeltec_wuyang_nav2')
    wheeltec_nav_launch_dir = os.path.join(wheeltec_nav_dir, 'launch')


    map_dir = os.path.join(wheeltec_nav_dir, 'map')
    map_file = LaunchConfiguration('map', default=os.path.join(
        map_dir, 'WHEELTEC.yaml'))


    #Modify the model parameter file, the options are:
    #param_mini_akm.yaml/param_mini_4wd.yaml/param_mini_diff.yaml/
    #param_mini_mec.yaml/param_mini_omni.yaml/param_mini_tank.yaml/
    #param_senior_akm.yaml/param_senior_diff.yaml/param_senior_mec_bs.yaml
    #param_senior_mec_dl.yaml/param_top_4wd_bs.yaml/param_top_4wd_dl.yaml
    #param_top_akm_dl.yaml/param_four_wheel_diff_dl.yaml/param_four_wheel_diff_bs.yaml
    #
    # For odometry-only navigation (no AMCL), use param_odom_akm.yaml for
    # Ackermann chassis or provide your own parameter file that does not launch AMCL.

    param_dir = os.path.join(wheeltec_nav_dir, 'param','wheeltec_params')
    param_file = LaunchConfiguration('params', default=os.path.join(
        param_dir, 'param_odom_akm.yaml'))

    initial_pose_x = LaunchConfiguration('initial_pose_x', default='0.0')
    initial_pose_y = LaunchConfiguration('initial_pose_y', default='0.0')
    initial_pose_yaw = LaunchConfiguration('initial_pose_yaw', default='0.0')


    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value=map_file,
            description='Full path to map file to load'),

        DeclareLaunchArgument(
            'params',
            default_value=param_file,
            description='Full path to param file to load'),

        DeclareLaunchArgument(
            'initial_pose_x',
            default_value=initial_pose_x,
            description='Initial X position of the robot in the map frame (meters)'),

        DeclareLaunchArgument(
            'initial_pose_y',
            default_value=initial_pose_y,
            description='Initial Y position of the robot in the map frame (meters)'),

        DeclareLaunchArgument(
            'initial_pose_yaw',
            default_value=initial_pose_yaw,
            description='Initial yaw of the robot in the map frame (radians)'),

        Node(
            name='waypoint_cycle',
            package='nav2_waypoint_cycle',
            executable='nav2_waypoint_cycle',
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [wheeltec_launch_dir, '/turn_on_wheeltec_robot.launch.py']),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [wheeltec_launch_dir, '/wheeltec_lidar.launch.py']),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [wheeltec_nav_launch_dir, '/bringup_odom_launch.py']),
            launch_arguments={
                'map': map_file,
                'use_sim_time': use_sim_time,
                'params_file': param_file,
                'initial_pose_x': initial_pose_x,
                'initial_pose_y': initial_pose_y,
                'initial_pose_yaw': initial_pose_yaw}.items(),
        ),

    ])
