from setuptools import setup, find_packages

setup(
    name="quizzer",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "colorama",
    ],
    entry_points={
        'console_scripts': [
            'quiz=quiz_app.quiz:main',
        ],
    },
    description="hope you pass",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dromaniv/quizzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
