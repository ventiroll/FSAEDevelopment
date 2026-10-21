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
    maintainer='AER CS Subteam',
    maintainer_email='mliu6758@sdsu.edu',
    description='AER Perception Node',
    license='BSD-3-Clause',
    entry_points={
        'console_scripts': [
            'mock_sensor_node = aer_perception.mock_sensor_node:main',
        ],
    },
)
