
from setuptools import setup

setup(
    name='markdown-fenced-code-tabs-next',
    version='1.1.0',
    url='https://github.com/elmahio/markdown-fenced-code-tabs-next',
    project_urls={
        'Bug Reports': 'https://github.com/elmahio/markdown-fenced-code-tabs-next/issues',
        'Source': 'https://github.com/elmahio/markdown-fenced-code-tabs-next',
    },
    packages=['markdown_fenced_code_tabs_next'],
    install_requires=[
        'markdown>=3.4',
        'htmlmin>=0.1.12',
        'Jinja2>=2.7.1'
    ],
    include_package_data=True,
    description='Generates a html structure for consecutive fenced code blocks content',
    author='Yassir Barchi',
    author_email='github@yassir.fr',
    maintainer='elmah.io',
    maintainer_email='info@elmah.io',
    license='MIT',
    keywords=['fenced code blocks', 'code', 'fenced', 'tabs', 'mkdocs', 'markdown', 'next'],
    long_description=""" Markdown extension who generates HTML tabs for consecutive fenced code blocks in markdown syntax """,
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing'
    ]
)
