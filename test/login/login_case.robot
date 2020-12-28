*** Settings ***
Documentation    the test cases for login
Library          SeleniumLibrary
Resource         login_action.robot


*** Variables ***
${Valid User Name}          devecor
${Valid Password}           t
${Invalid User Name}        wrong name
${Invalid User Password}    wrong password


*** Test Cases ***
Login With Valid User
    Open Login Dialog
    Input User Name    ${Valid User Name}
    Input User Password    ${Valid Password}
    Confirm To Login
    Login Should Succeed

Login With Invalid Username
    Open Login Dialog
    Input User Name    ${Invalid User Name}
    Input User Password    ${Valid Password}
    Confirm To Login
    Login Should Fail

Login With Invalid Password
    Open Login Dialog
    Input User Name    ${Valid User Name}
    Input User Password    ${Invalid User Password}
    Confirm To Login
    Login Should Fail

Login With Invalid Username And Password
    Open Login Dialog
    Input User Name    ${Invalid User Name}
    Input User Password    ${Invalid User Password}
    Confirm To Login
    Login Should Fail
