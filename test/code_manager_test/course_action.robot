*** Settings ***
Documentation    the common keywords for login defined here
Resource         ../common.robot

*** Variables ***
${Add Course Button}                  xpath: //div/button[@title="新增课程"]
${Confirm To Add Course Button}       xpath: //div[@class="el-message-box"]/descendant::button[contains(./span/text(), "确定")]
${Delete Course Button}               xpath: //div[@class="cb-navbar"]/descendant::button[@title="删除当前课程和相关的课程文件"]
${Rename Course Button}               xpath: //div[@class="cb-navbar"]/descendant::button[@title="修改课程标题"]
${Confirm To Delete Course Button}    xpath: //div[@class="el-message-box"]/descendant::button[contains(span, "确定")]
${Confirm To Rename Course Button}    xpath: //div[@class="el-message-box"]/descendant::button[contains(span, "确定")]

${Course Input}                       xpath: //div[@class="el-message-box"]/descendant::div[@class="el-input"]/input
${Select Course Input}                xpath: //div[@class="cb-card"]/descendant::input[@class="el-input__inner"]

${Can Not Add Course Alert}           xpath: //div[@role="alert"]/descendant::p[contains(text(), "未登陆用户不能创建课程")]

*** Keywords ***
Click Add Course Button
    Click Button    ${Add Course Button}

Input Course Name
    [Arguments]    ${Course Name}
    Input Text    ${Course Input}    ${Course Name}

Input New Course Name
    [Arguments]    ${Course Name}
    Input Text    ${Course Input}    ${Course Name}

Confirm To Add Course
    Click Button    ${Confirm To Add Course Button}

Current Course Should Be
    [Arguments]    ${Course Name}
    Sleep    0.2s
    Element Attribute Value Should Be    ${Select Course Input}    value    ${Course Name}

Verify Course Can Not Be Added
    Wait Until Element Is Visible    ${Can Not Add Course Alert}    0.5s

Verify Course Can Not Be Renamed
    Element Should Be Disabled    ${Rename Course Button}

Verify Course Can Not Be Deleted
    Element Should Be Disabled    ${Delete Course Button}

Click Button To Delete Course
    Click Button    ${Delete Course Button}

Click Button To Rename Course
    Click Button    ${Rename Course Button}

Confirm To Delete Course
    Click Button    ${Confirm To Delete Course Button}

Confirm To Rename Course
    Click Button    ${Confirm To Rename Course Button}

Course Should Be Deleted
    [Arguments]    ${Course Name}
    Click Element    ${Select Course Input}
    Page Should Not Contain Element    xpath: //div[@class="el-scrollbar"]/descendant::li[span="${Course Name}"]
    Click Element    ${Select Course Input}

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
    Click Button    ${Add Course Button}
    Input Text    ${Course Input}    ${Course Name}
    Click Button    ${Confirm To Add Course Button}
    Current Course Should Be    ${Course Name}

Delete Course
    [Arguments]    ${Course Name}
    Select Course    ${Course Name}
    Click Button    ${Delete Course Button}
    Click Button    ${Confirm To Delete Course Button}
    Sleep    0.5s
    Click Element    ${Select Course Input}
    Page Should Not Contain Element    xpath: //div[@class="el-scrollbar"]/descendant::li[span="${Course Name}"]
    Click Element    ${Select Course Input}
