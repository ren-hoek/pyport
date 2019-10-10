import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyport',
    version='0.2.3',
    author="Ren Hoek",
    author_email="ren.hoek@daex.com",
    description="A Portainer API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ren-hoek/pyport",
    packages=setuptools.find_packages(),
    install_requires=['requests>==2.22.0'],
    scripts=[
        'bin/add_daex_user', 'bin/add_folder', 'bin/build_image',
        'bin/deploy_stack', 'bin/init_admin', 'bin/pull_image',
        'bin/redeploy_stack', 'bin/remove_stack', 'bin/tag_image',
        'bin/add_secret', 'bin/push_image', 'bin/remove_secret'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
 )

