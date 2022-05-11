from setuptools import setup

setup(
        name = 'odroid-homecloud',
        version = '0.1',
        description = 'ODROID LCD panel script',
        author = 'Dongjin Kim',
        author_email = 'tobetter@gmail.com',
        license = 'MIT',
        install_requires = [
            'luma.core >= 1.17.1',
            'luma.oled >= 3.6.0',
            'luma.lcd >= 2.5.0',
            'bitcoinrpc >= 0.3.1',
            'requests >= 2.27.1'
            ],
        packages = [
            'odroid_homecloud_display'
            ],
        entry_points = {
            'console_scripts' : [
                'odroid_homecloud_display = odroid_homecloud_display.clock:main']
            },
        zip_safe = False)
