# Codebang Test Cases
Here are robot test cases to verify the main functions of `codebang`, each test case has one `.robot` file. These test cases also could be as a guide for end users to understand how to use codebang.

## Let's start!
In order to run them automatically, first install RobotFramework and SeleniumLibrary by `pip`

```sh
python3 -m pip install robotframework robotframework-SeleniumLibrary
```

then, please complete the following preparations step by step

### 1. install webDirvers
The general approach to install a browser driver is downloading a right driver, such as chromedriver for Chrome, and **placing it into a directory that is in** `path`. here are two fast links about chrome and firefox drivers in `npm.taobao.org` for chinese users.

[chrome webdriver](https://npm.taobao.org/mirrors/chromedriver/)

[firefox geckodriver](https://npm.taobao.org/mirrors/geckodriver/)

### 2. start codebang and future-server

you have to start future-server at port `9092`. change directory to `future-server` in a terminal,
then
```sh
python3 manage.py runserver 9092
```

change directory to `codebang` in a terminal and start codebang at any port you want(default: `8080`), then
```sh
npm run serve
```

or you may want to use a shell script named `autostart.sh` for starting codebang and future-server automaticaly
```sh
./autostart.sh
``` 

### 3. run tests
create a directory for testing
```sh
mkdir test-results

cd test-results
```

run any of one test case. for ecample
```sh
robot -X -d ./test-results course_management_test.robot
```

or run the whole test suite
```sh
robot -d test-results .
```

## Test cases List

## Reference

* [robotframework](https://robotframework.org/#examples)
* [SeleniumLibrary](https://robotframework.org/SeleniumLibrary/)