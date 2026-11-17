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
    maintainer='SDSU AER',
    maintainer_email='aer@sdsu.edu',
    description='Planning and decision-making nodes',
    license='BSD-3-Clause',
    entry_points={
        'console_scripts': [
            'trajectory_planning = aer_planning.trajectory_planning_node:main',
            'global_path_planning = aer_planning.global_path_planning_node:main',
            'decision_making = aer_planning.decision_making_node:main',
        ],
    },
)
