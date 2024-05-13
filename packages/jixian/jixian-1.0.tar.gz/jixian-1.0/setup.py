from setuptools import setup,find_packages

setup(
    name='jixian',
    url='https://github.com/Moxin1044/jixian',
    version='1.0',
    author="Moxin",
    author_email='lqn@jixiannet.com',
    description='set your encoding and logger',
    long_description='Show Chinese for your mark.parametrize(). Define logger variable for getting your log',
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.8',
    ],
    license='proprietary',
    packages = find_packages(),
    keywords=[
        'pytest', 'py.test', 'pytest_encode',
    ],
    zip_safe=False
)
