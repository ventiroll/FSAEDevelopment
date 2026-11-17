from setuptools import setup
package_name = 'aer_safety'
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
    description='Safety and liveliness monitor nodes',
    license='BSD-3-Clause',
    entry_points={
        'console_scripts': [
            'safety_monitor = aer_safety.safety_monitor_node:main',
        ],
    },
)
