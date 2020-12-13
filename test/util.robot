*** Settings ***
Documentation     A common utility keywords library.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.
Library           SeleniumLibrary

*** Variables ***
${Me Dropdown Button}    xpath: //div[@class="el-dropdown"]/button
${Login Button}    xpath: //ul/li[contains(text(), "登陆")]

${Course Input}    xpath: //div[@class="el-message-box"]/descendant::div[@class="el-input"]/input
${Select Course Input}    xpath: //div[@class="cb-card"]/descendant::input[@readonly="readonly"]

*** Keywords ***
Verify Login Status
    [Arguments]    ${User Name}
    Sleep    0.5s
    Click Button    ${Me Dropdown Button}
    Element Text Should Be    ${Login Button}    登陆为 ${User Name}    ${User Name}

Login
    [Arguments]    ${User Name}    ${Password}
    Click Button    ${Me Dropdown Button}
    Click Element    ${Login Button}
    Input Text    ${User Name Input}    ${User Name}
    Input Password    xpath: //div/input[@type="password"]    ${Password}
    Click Button    xpath: //div/button[span="登陆"]
    Verify Login Status    ${User Name}

Current Course Should Be
    [Arguments]    ${Course Name}
    Element Attribute Value Should Be    ${Select Course Input}    value    ${Course Name}

Course Should Exist
    [Arguments]    ${Course Name}
    Click Element    ${Select Course Input}
    ${Course Li} =    Get WebElement    xpath: //div[@class="el-scrollbar"]/descendant::li[span="${Course Name}"]
    Page Should Contain Element    ${Course Li}
    [Return]    ${Course Li}

Select Course
    [Arguments]    ${Course Name}
    ${Course Element} =    Course Should Exist    ${Course Name}
    Click Element    ${Course Element}
    Current Course Should Be    ${Course Name}

Add Course
    [Arguments]    ${Course Name}
    Verify Login Status    ${User Name}
    Click Button    ${Add Course Button}
    Input Text    ${Course Input}    ${Course Name}
    Click Button    ${Confirm To Add Course Button}
    Current Course Should Be    ${Course Name}
