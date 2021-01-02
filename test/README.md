# Codebang Tests
This folder contains the various test runners for **codebang**.

## Requirements

### 1. Install the dependencis
Before running the test, install the dependencies:
```sh
python3 -m pip install robotframework robotframework-SeleniumLibrary
```

### 2. Install webDirvers
The general approach to install a browser driver is downloading a right driver, such as chromedriver for Chrome, and placing it into a directory that is in **PATH**. Drivers for different browsers can be found as follows

* [ChromeDriver for google Chrome](https://npm.taobao.org/mirrors/chromedriver/)

* [Geckodriver for firefox](https://npm.taobao.org/mirrors/geckodriver/)

### 3. Start server

You have to start future-server at port `9092`. Change directory to `future-server` in a terminal,
then
```sh
python3 manage.py runserver 9092
```

Change directory to `codebang` in a terminal and start codebang at any port you expected(default: `8080`), then
```sh
npm run serve
```

You may want to use a shell script named `autostart.sh` for starting codebang and future-server automaticaly.
```sh
./autostart.sh
``` 

## Run tests
Create a directory for test log files
```sh
mkdir test-results
```

Run any of one test suite which contains some test cases. for ecample
```sh
cd codebang/test
robot -X -d test-results --suite login_suite code_manager_test
```

Or run the whole test suite
```sh
robot -X -d test-results .
```

## Test cases List

### Login
* Login With Valid User
* Login With Invalid Username
* Login With Invalid Password
* Login With Invalid Username And Password
