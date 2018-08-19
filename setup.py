import setuptools

setuptools.setup(
    name="html_report_scale",
    packages=["html_report_scale"],
    version="0.0.1",
    package_data={
        'templates': [
            'report.html'
        ],
    },
    install_requires=[
        'jinja2', 'nose2'
    ]

)