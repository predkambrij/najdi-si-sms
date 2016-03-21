from setuptools import setup

version = '0.3.2'

tests_require = [
    'response',
]
testing_extras = tests_require + [
    'nose',
    'coverage',
    'betamax',
    'betamax_serializers',
]

setup(name='najdisi-sms',
      version=version,
      description="Najdi.si sms command line tool and API",
      long_description="""""",
      classifiers=[
          'Development Status :: 3 - Alpha',

          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',

          'Topic :: Communications :: Telephony',
          'Topic :: System :: Logging',

          'License :: OSI Approved :: BSD License',

          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      keywords='development notification sms gateway najdi telekom slovenia',
      author='Domen Kozar, Andraz Brodnik',
      author_email='brodul@brodul.org',
      url='https://github.com/brodul/najdi-si-sms',
      license='BSD',
      py_modules=['najdisi_sms'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          # -*- Extra requirements: -*-
          'requests==2.9.1',
          'beautifulsoup4==4.3.2',
      ],
      extras_require={
          'testing': testing_extras,
      },
      tests_require=tests_require,

      entry_points="""
      [console_scripts]
      najdisi-sms = najdisi_sms:main
      """,
      )
