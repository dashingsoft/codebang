*** Settings ***
Documentation    Login test contains all cases
...              Login success case
...              Login fail case

Library          SeleniumLibrary
Resource         util.robot
Test Setup       Open Codebang To Home Page
Test Teardown    Close Browser


*** Test Cases ***
The Login Success Case
    Login Should Success    ${User Name}    ${Password}

The Login Failure Case
    Login Should Fail    ${User Name}    "wrong password"
    Login Should Fail    "wrong username"    ${Password}
    Login Should Fail    "wrong username"    "wrong password"
