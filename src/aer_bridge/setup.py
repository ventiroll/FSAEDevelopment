from setuptools import setup
package_name = 'aer_bridge'
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
    description='Hardware UART bridge node to STM32',
    license='BSD-3-Clause',
    entry_points={
        'console_scripts': [
            'uart_bridge = aer_bridge.uart_bridge_node:main',
        ],
    },
)
