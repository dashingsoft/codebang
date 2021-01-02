*** Settings ***
Documentation    the test cases for login
Resource         login_action.robot
Test Teardown    Logout


*** Variables ***
${Valid User Name}          devecor
${Valid Password}           t
${Invalid User Name}        wrong name
${Invalid User Password}    wrong password


*** Test Cases ***
Login With Valid User
    [Tags]    normal
    Open Login Dialog
    Input User Name    ${Valid User Name}
    Input User Password    ${Valid Password}
    Confirm To Login
    Login Should Succeed

Login With Invalid Username
    [Tags]    abnormal
    Open Login Dialog
    Input User Name    ${Invalid User Name}
    Input User Password    ${Valid Password}
    Confirm To Login
    Login Should Fail

Login With Invalid Password
    [Tags]    abnormal
    Open Login Dialog
    Input User Name    ${Valid User Name}
    Input User Password    ${Invalid User Password}
    Confirm To Login
    Login Should Fail

Login With Invalid Username And Password
    [Tags]    abnormal
    Open Login Dialog
    Input User Name    ${Invalid User Name}
    Input User Password    ${Invalid User Password}
    Confirm To Login
    Login Should Fail
