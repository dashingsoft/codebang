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

Run any test suite which contains some test cases
```sh
cd codebang/test
robot -X -d test-results --suite login_suite code_manager
```

Run one test case that is in a test suite
```sh
robot -X -d test-results --suite login_suite --test login_with_valid_user
```

Run the smoke test with `-i tag`
```sh
robot -X -d test-results -i normal .
```

Run the whole test suite
```sh
robot -X -d test-results .
```

## Test cases
See [Test Cases List](codebang_test_cases.md)

## Test guide
[Codebang Test Guide For Developer](codebang_test_guide.md)
