from setuptools import setup
import os
from glob import glob

package_name = 'aer_drivers'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='SDSU AER',
    maintainer_email='aer@sdsu.edu',
    description='Sensor driver nodes for FSAE Autonomous',
    license='BSD-3-Clause',
    entry_points={
        'console_scripts': [
            'camera_driver = aer_drivers.camera_driver_node:main',
            'lidar_driver = aer_drivers.lidar_driver_node:main',
            'gps_driver = aer_drivers.gps_driver_node:main',
            'imu_driver = aer_drivers.imu_driver_node:main',
            'encoder_driver = aer_drivers.encoder_driver_node:main',
        ],
    },
)
