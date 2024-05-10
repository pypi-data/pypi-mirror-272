from distutils.core import setup

setup(
    name="tiny_progress_bar",  # How you named your package folder (MyLib)
    packages=["tiny_progress_bar"],  # Chose the same as "name"
    version="0.1.1",  # Start with a small number and increase it with every change you make
    license="GPL-3.0",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="Simple progress bar for Python 3",  # Give a short description about your library
    readme="README.md",
    author="Alan Lin",  # Type in your name
    author_email="lin.alan.k@gmail.com",  # Type in your E-Mail
    url="https://github.com/aklin2/tiny_progress_bar",  # Provide either the link to your github or to your website
    download_url="https://github.com/aklin2/tiny_progress_bar/archive/refs/tags/v0.1.1.tar.gz",  # I explain this later on
    keywords=[
        "progress",
        "progress bar",
        "tiny_progress_bar",
        "loading",
        "loading bar",
        "loading_bar",
    ],  # Keywords that define your package best
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",  # Again, pick a license
        "Programming Language :: Python :: 3",  # Specify which pyhton versions that you want to support
    ],
)
