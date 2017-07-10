from setuptools import setup

INSTALL_REQUIRES = [
    'erppeek',
    'rq',
    'click'
]

setup(
    name='shera',
    version='0.1',
    packages=['shera'],
    url='',
    license='',
    install_requires=INSTALL_REQUIRES,
    entry_points="""
        [console_scripts]
        shera=shera.runner:shera
    """,
    author='',
    author_email='',
    description='Report delivery engine'
)
