# JULO_mini_wallet
mini wallet exercise for JULO interview

This Project was developed in Ubuntu 22.04.2 LTS

#### install Python and virtual environment

* pyenv and pyenv-virtualenv

    1. Install pyenv and pyenv-virtualenv
    visit [here](https://github.com/pyenv/pyenv) to read more about pyenv installation and [here](https://github.com/pyenv/pyenv-virtualenv) for pyenv-virtualenv installation

        ```shell
        $ pyenv --version
        pyenv 2.3.16-1-gb1ee6c93
        ```

    2. Install Python 3.10.9 on Pyenv

        ```shell
        $ pyenv install 3.10.9
        Downloading Python-3.10.9.tar.xz...
        -> https://www.python.org/ftp/python/3.10.9/Python-3.10.9.tar.xz
        Installing Python-3.10.9...
        Installed Python-3.10.9 to /path/to/.pyenv/versions/3.10.9
        ```

    3. Install mini-wallet virtualenv using python 3.10.9

        ```shell
        $ pyenv virtualenv 3.10.9 mini-wallet
        Looking in links: /tmp/tmpsnwijw0c
        Requirement already satisfied: setuptools in /path/to/.pyenv/versions/3.10.9/envs/mini-wallet/lib/python3.6/site-packages (40.6.2)
        Requirement already satisfied: pip in /path/to/.pyenv/versions/3.10.9/envs/mini-wallet/lib/python3.6/site-packages (18.1)
        ```

    4. Autoactivate virtualenv

        ```shell
        $ cd /path/to/mini-wallet
        $ pyenv local mini-wallet
        (mini-wallet) $ which python
        /path/to/.pyenv/shims/python
        ```

#### Installing python app requirements
1. Install latest pip
    ```shell
    $ pip install --upgrade pip
    ```
2. Define .env for flask environment
    ```shell
    $ cp .env.example .env
    $ pip install python-dotenv
    Collecting python-dotenv
        Using cached python_dotenv-1.0.0-py3-none-any.whl (19 kB)
    Installing collected packages: python-dotenv
    Successfully installed python-dotenv-1.0.0

3. Install poetry for package dependencies
    ```shell
    $ pip install poetry
    ```
4. Install all needed libraries
    ```shell
    $ poetry install

#### Modifying Database models and tables

We're using Alembic for the database models, we just replaced 'alembic' with 'flask db'

* to auto generate migration file after modifying models, run this in your terminal at the project root folder
    ``` shell script
    flask db revision --autogenerate -m "[revision description]"
    ```
* to upgrade data base to the latest revision, run this in your terminal at the project root folder

    ``` shell script
    flask db upgrade head
    ```
* if alembic do not detect the models, make sure that the PYTHONPATH environment variable is set. Run this in your terminal at the project root folder
    ``` shell script
    export PYTHONPATH=$(pwd)
    ```

* other alembic commands and tutorials can be viewed at https://alembic.sqlalchemy.org/en/latest/index.html