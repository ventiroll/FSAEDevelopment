from setuptools import setup
import os
from glob import glob

package_name = 'aer_demo_inverter'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='AER Autonomous Subteam',
    maintainer_email='aer@sdsu.edu',
    description='Simple 1-node ROS 2 inverter demo node pushing control commands to micro-ROS microcontroller',
    license='BSD-3-Clause',
    entry_points={
        'console_scripts': [
            'demo_inverter_node = aer_demo_inverter.demo_inverter_node:main',
        ],
    },
)
