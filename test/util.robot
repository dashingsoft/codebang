*** Settings ***
Documentation     A common utility keywords library.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.
Library           SeleniumLibrary

*** Variables ***
${URL}                             http://localhost:8080/app
${BROWSER}                         chrome

${User Name}                       devecor
${Password}                        t
${Test Course Name Glibc}          glibc
${Test Course Name Linux-core}     linux-core
${Test File Name}                  main.c

${Me Dropdown Button}              xpath: //div[@class="el-dropdown"]/button
${Login Button}                    xpath: //ul/li[contains(text(), "登陆")]
${Add Course Button}               xpath: //div/button[@title="新增课程"]
${Add File Button}                 xpath: //div/button[@title="新增文件"]
${Confirm To Add Course Button}    xpath: //div[@class="el-message-box"]/descendant::button[contains(./span/text(), "确定")]
${Confirm To Add File Button}      xpath: //div[@class="el-message-box"]/descendant::button[contains(./span/text(), "确定")]
${Login Dialog Close Button}       xpath: //div[@class="el-dialog__header"]/descendant::button[@aria-label="Close"]

${User Name Input}                 xpath: //input[@placeholder="用户名/邮箱/手机号"]
${Add Course Input}                xpath: //div[@class="el-message-box"]/descendant::div[@class="el-input"]/input
${Select Course Input}             xpath: //div[@class="cb-card"]/descendant::input[@class="el-input__inner"]
${Delete Course Button}            xpath: //div[@class="cb-navbar"]/descendant::button[@title="删除当前课程和相关的课程文件"]
${Add File Input}                  xpath: //div[@class="el-message-box"]/descendant::div[@class="el-input"]/input

${Login Dialog}                    xpath: //div[@class="el-dialog__body" and contains(./descendant::label/text(), "账户")]

*** Keywords ***
Open Codebang To Home Page
    Set Selenium Speed    0
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Title Should Be  codebang    can not open codebang

Verify Login Status
    [Arguments]    ${User Name}
    Wait Until Element Is Visible    ${Me Dropdown Button}    1s
    Sleep    0.2s
    Click Button    ${Me Dropdown Button}
    Wait Until Element Contains    ${Login Button}    登陆为 ${User Name}    1s

Close Login Dialog If It Is Opening
    ${Count} =    Get Element Count    ${Login Dialog}
    Run Keyword If    ${Count} > 0    Click Button    ${Login Dialog Close Button}

Login Should Success
    [Arguments]    ${User Name}    ${Password}
    Click Button    ${Me Dropdown Button}
    Wait Until Element Is Visible    ${Login Button}    0.5s
    Click Element    ${Login Button}
    Input Text    ${User Name Input}    ${User Name}
    Input Password    xpath: //div/input[@type="password"]    ${Password}
    Click Button    xpath: //div/button[span="登陆"]
    Verify Login Status    ${User Name}

Login Should Fail
    [Arguments]    ${User Name}     ${Password}
    [Documentation]    Failure test case for incrrect username or password or both
    Click Button    ${Me Dropdown Button}
    Wait Until Element Is Visible    ${Login Button}    0.5s
    Click Element    ${Login Button}
    Input Text    ${User Name Input}    ${User Name}
    Input Password    xpath: //div/input[@type="password"]    ${Password}
    Click Button    xpath: //div/button[span="登陆"]
    User Should Not Login    ${User Name}

Is Login
    [Arguments]    ${User Name}
    Close Login Dialog If It Is Opening
    Wait Until Element Is Visible    ${Me Dropdown Button}    1s
    Sleep    0.3s
    Click Button    ${Me Dropdown Button}
    Sleep    0.3s
    ${Element Text} =    Get Text    ${Login Button}
    ${Return Value} =    Set Variable    ${False}
    ${Return Value}    Run Keyword If    "登陆为" in "${Element Text}"    Set Variable    ${True}
    [Return]    ${Return Value}

User Should Not Login
    [Arguments]    ${User Name}
    ${IsLogin} =    Is Login    ${User Name}
    Run Keyword If    ${IsLogin}    Fail    "Login should fail, but it didn't"

Current Course Should Be
    [Arguments]    ${Course Name}
    Sleep    0.2s
    Element Attribute Value Should Be    ${Select Course Input}    value    ${Course Name}

# 会使页面停在课程列表处
Course Should Exist
    [Arguments]    ${Course Name}
    Click Element    ${Select Course Input}
    ${Course Li} =    Get WebElement    xpath: //div[@class="el-scrollbar"]/descendant::li[span="${Course Name}"]
    Wait Until Page Contains Element    ${Course Li}    1s
    [Return]    ${Course Li}

Course Should Not Exist
    [Arguments]    ${Course Name}
    Click Element    ${Select Course Input}

Select Course
    [Arguments]    ${Course Name}
    ${Course Element} =    Course Should Exist    ${Course Name}
    Sleep    0.5s
    Click Element    ${Course Element}
    Current Course Should Be    ${Course Name}

Add Course
    [Arguments]    ${Course Name}
    Verify Login Status    ${User Name}
    Click Button    ${Add Course Button}
    Input Text    ${Add Course Input}    ${Course Name}
    Click Button    ${Confirm To Add Course Button}
    Current Course Should Be    ${Course Name}

Add File
    [Arguments]    ${File Name}
    Verify Login Status    ${User Name}
    Select Course    ${Test Course Name Glibc}
    Mouse Down    ${Add File Button}
    Mouse Up    ${Add File Button}
    Input Text    ${Add File Input}    ${File Name}
    Click Button    ${Confirm To Add File Button}
    Wait Until Element Is Not Visible    ${Confirm To Add File Button}    1s

Delete Course
    [Arguments]    ${Course Name}
    Select Course    ${Course Name}
    Click Button    ${Delete Course Button}
    Click Button    xpath: //div[@class="el-message-box"]/descendant::button[contains(span, "确定")]
    Wait Until Element Is Visible    ${Select Course Input}
    Sleep    0.2s
    Click Element    ${Select Course Input}
    Page Should Not Contain Element    xpath: //div[@class="el-scrollbar"]/descendant::li[span="${Course Name}"]
    Click Element    ${Select Course Input}
