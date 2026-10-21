from setuptools import setup
package_name = 'aer_planning'
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
    description='AER Path Planner',
    license='BSD-3-Clause',
    entry_points={
        'console_scripts': [
            'path_planner_node = aer_planning.path_planner_node:main',
        ],
    },
)
