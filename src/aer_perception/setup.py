from setuptools import setup
package_name = 'aer_perception'
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
    description='Perception pipeline nodes',
    license='BSD-3-Clause',
    entry_points={
        'console_scripts': [
            'lane_detection = aer_perception.lane_detection_node:main',
            'object_detection = aer_perception.object_detection_node:main',
            'position_estimation = aer_perception.position_estimation_node:main',
            'obstacle_detection = aer_perception.obstacle_detection_node:main',
        ],
    },
)
