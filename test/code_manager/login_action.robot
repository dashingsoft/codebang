*** Settings ***
Documentation    the common keywords for login defined here
Resource         ../common.robot


*** Variables ***
${Confirm To Login Button}         xpath: //div/button[span="登陆"]
${Me Dropdown Button}              xpath: //div[@class="el-dropdown"]/button
${Login Button}                    xpath: //ul/li[contains(text(), "登陆")]
${Logout Button}                   xpath: //ul/li[contains(text(), "注销")]
${Login Dialog Close Button}       xpath: //div[@class="el-dialog__header"]/descendant::button[@aria-label="Close"]

${Login Dialog}                    xpath: //div[@class="el-dialog__wrapper" and contains(./descendant::label/text(), "账户")]

${User Name Input}                 xpath: //input[@placeholder="用户名/邮箱/手机号"]
${User Password Input}             xpath: //div/input[@type="password"]

${Default User Name}               devecor
${Default User Password}           t


*** Keywords ***
Open Login Dialog
    Click Button    ${Me Dropdown Button}
    Wait Until Element Is Visible    ${Login Button}    0.5s
    Click Element    ${Login Button}
    Wait Until Element Is Visible    ${Login Dialog}    0.5s

Input User Name
    [Arguments]    ${User Name}
    Input Text    ${User Name Input}    ${User Name}

Input User Password
    [Arguments]    ${User Password}
    Input Password    ${User Password Input}    ${User Password}

Confirm To Login
    Click Button    ${Confirm To Login Button}

Login Should Succeed
    [Arguments]    ${User Name}=${Empty}
    ${IsLogin} =    Is Login    ${User Name}
    Run Keyword If    not ${IsLogin}    Fail    "Login should succeed, but it didn't"

Login Should Fail
    [Arguments]    ${User Name}=${Empty}
    [Documentation]    Verifies that the ${User Name} login failed.
...                    ${Login Dialog} should be existing, or it will raise a fail. 
    Click Element    ${Login Dialog Close Button}
    Wait Until Element Is Not Visible    ${Login Dialog Close Button}    0.5s
    ${IsLogin} =    Is Login    ${User Name}
    Run Keyword If    ${IsLogin}    Fail    "Login should fail, but it didn't"

Is Login
    [Arguments]    ${User Name}=${Empty}
    Wait Until Element Is Visible    ${Me Dropdown Button}    0.5s
    Click Button    ${Me Dropdown Button}
    Sleep    0.3s
    ${Element Text} =    Get Text    ${Login Button}
    ${Return Value} =    Set Variable    ${False}
    ${Return Value} =    Run Keyword If    "登陆为${Space}${User Name}" in "${Element Text}"    Set Variable    ${True}
    Click Button    ${Me Dropdown Button}
    [Return]    ${Return Value}

Login
    [Arguments]    ${User Name}    ${Password}
    Open Login Dialog
    Input User Name    ${User Name}
    Input User Password    ${Password}
    Confirm To Login
    Login Should Succeed

Logout
    ${Is Login} =    Is Login
    Return From Keyword If    not ${Is Login}    ${None}
    Click Button    ${Me Dropdown Button}
    Wait Until Element Is Visible     ${Logout Button}    0.5s
    Click Element    ${Logout Button}
    Wait Until Element Is Not Visible     ${Logout Button}    0.5s
    ${Is Login} =    Is Login
    Run Keyword If    ${Is Login}    Fail    "Logout failed"

Login With Default User
    Login    ${Default User Name}    ${Default User Password}
