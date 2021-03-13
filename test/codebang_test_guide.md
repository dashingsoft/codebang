# Codebang test guide

## Getting started
This is a tutorial for developer to prefect test cases of codebang. There is a [specification](#Specification) that we must follow

### Prerequisites
See [README](README.md)

### Specification

#### File encoding
* utf-8

#### Separated format
* Space: 4 in genaral or more in special, for example
  ```Robot Framework
  *** Settings ***
  Documentation     Example using the space separated format.
  Library           OperatingSystem
  
  *** Variables ***
  ${MESSAGE}        Hello, world!
  
  *** Test Cases ***
  My Test
      [Documentation]    Example test.
      Log    ${MESSAGE}
      My Keyword    ${CURDIR}
  
  Another Test
      Should Be Equal    ${MESSAGE}    Hello, world!
  
  *** Keywords ***
  My Keyword
      [Arguments]    ${path}
      Directory Should Exist    ${path}
  ```

#### File name
* File names must be all lowercase and may include underscores: `_`
* No additional punctuation.
* Filenames’ extension must be `.robot`.

  For example: `login_action.robot`

#### Structure
* a test suite of codebang with fandamental capability created from only **two** files: 
  * Resource file: `anction.robot`
  * Test case file: `case.robot`

  Any costomized `keyword` about the current suite should be defined in Resource file `anction.robot`. All cases for the current suite within test case file `case.robot` are expected.
* A high level suite of codebang created from a directory with a initialization file. An initialization file name must always be of the format `__init__.ext`, where the extension must be one of the supported file formats (typically `__init__.robot`).The main usage for initialization files is specifying test suite related settings in global. For example
  ```
  *** Settings ***
  Documentation     the code manager test suite
  Metadata          Version    0.1
  Library           SeleniumLibrary
  Resource          ../common.robot
  Suite Setup       Open Codebang To Home Page
  Suite Teardown    Close Browser
  ```
#### Keywords, cases and documentions
See [How to write good test cases using Robot Framework](https://github.com/robotframework/HowToWriteGoodTestCases/blob/master/HowToWriteGoodTestCases.rst)

#### Tags
In order to costomize **smoke test**, we should create test cases with `Tags`.A test case can specified with multiple tags.
* Use the `main` for the most important test case, such as login, add course etc.
* Use the `normal` for legal operations
* Use the `abnormal` for iilegal operations
* Continually updating...

## Reference

* [Robot Framework User Guide](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
* [The home page of SeleniumLibrary](https://robotframework.org/SeleniumLibrary/)
* [How to write good test cases using Robot Framework](https://github.com/robotframework/HowToWriteGoodTestCases/blob/master/HowToWriteGoodTestCases.rst)