# A simple forum written using flask. 

### How to run application?

1) Create virtual environment.
```
$ python3 -m venv venv

```

2) Activate virtual environment.
```
$ source ./venv/bin/activate

```

3) Install python dependencies.
```
$ pip install -r ./requirements.txt

```

4) Create .env file in project directory.

5) Static js and css libraries .
   1) Check if you have installed node and npm:
    ```
    $ node --version && npm --version

    ```
   2) Run script:
    ```
    $ bash ./main.sh type="build-static-css-and-js-libs"

    ```

6) Use database container.
   1) Check if you have installed docker and docker-compose:
    ```
    $ docker --version && docker-compose --version
    ```
   2) Run container:
    ```
    $ docker-compose -f ./docker-compose-dev.yaml up -d
    ```
   3) Do not forget to turn it off after work =)
    ```
    $ docker-compose -f ./docker-compose-dev.yaml down
    ```   
   
7) Migrate database.
```
$ cd ./web-application/
$ python ./manage.py db migrate
$ python ./manage.py db upgrade
$ python ./manage.py insert
$ cd ..   # back to project dir.
```

8) Run application.
```
$ cd ./web-application/
$ flask run 
```