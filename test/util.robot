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
${Add Course Button}    xpath: //div/button[@title="新增课程"]
${Add File Button}    xpath: //div/button[@title="新增文件"]
${Confirm To Add Course Button}    xpath: //div[@class="el-message-box"]/descendant::button[contains(./span/text(), "确定")]
${Confirm To Add File Button}    xpath: //div[@class="el-message-box"]/descendant::button[contains(./span/text(), "确定")]

${Add Course Input}    xpath: //div[@class="el-message-box"]/descendant::div[@class="el-input"]/input
${Select Course Input}    xpath: //div[@class="cb-card"]/descendant::input[@class="el-input__inner"]
${Delete Course Button}    xpath: //div[@class="cb-navbar"]/descendant::button[@title="删除当前课程和相关的课程文件"]
${Add File Input}    xpath: //div[@class="el-message-box"]/descendant::div[@class="el-input"]/input

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

# 会使页面停在课程列表处
Course Should Exist
    [Arguments]    ${Course Name}
    Click Element    ${Select Course Input}
    ${Course Li} =    Get WebElement    xpath: //div[@class="el-scrollbar"]/descendant::li[span="${Course Name}"]
    Page Should Contain Element    ${Course Li}
    [Return]    ${Course Li}

Course Should Not Exist
    [Arguments]    ${Course Name}
    Click Element    ${Select Course Input}
    

Select Course
    [Arguments]    ${Course Name}
    ${Course Element} =    Course Should Exist    ${Course Name}
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
    Sleep    0.5s
    Click Element    ${Select Course Input}
    Page Should Not Contain Element    xpath: //div[@class="el-scrollbar"]/descendant::li[span="${Course Name}"]
    Click Element    ${Select Course Input}

