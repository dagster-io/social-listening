from setuptools import find_packages, setup

setup(
    name="social_listening",
    packages=find_packages(exclude=["social_listening_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster_slack",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
