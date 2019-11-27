from setuptools import setup, find_packages

PACKAGE_NAME = 'clickhouse'

setup(
    name=PACKAGE_NAME,
    description="Clickhouse table monitor",
    version="0.0.1",
    install_requires=[
		"gunicorn",
        "flask==1.1.1",
        "clickhouse-driver==0.1.2",
		"ldap3==2.6.1",
		"flask-wtf==0.14.2",
		"flask-login==0.4.1",
        "flask-sqlalchemy==2.4.1",
        "flask-cors==3.0.7",
        "flask-migrate==2.5.2",
    ],
    include_package_data=True,
)
