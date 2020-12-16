*** Settings ***
Documentation     Simple example using SeleniumLibrary.
Library           SeleniumLibrary
Resource          util.robot

*** Variables ***
${URL}    http://localhost:8080/app
${BROWSER}    headlessfirefox
${User Name}    devecor
${Password}    t
${Test Course Name Glibc}    glibc
${Test Course Name Linux-core}    linux-core
${Test File Name}    main.c

${Add Course Button}    xpath: //div/button[@title="新增课程"]
${Add File Button}    xpath: //div/button[@title="新增文件"]/i
${Confirm To Add Course Button}    xpath: //div[@class="el-message-box"]/descendant::button[contains(./span/text(), "确定")]

${User Name Input}    xpath: //input[@placeholder="用户名/邮箱/手机号"]

*** Test Cases ***
open
    Set Selenium Speed    0
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Title Should Be  codebang    case1: can not open codebang

login
    Login    ${User Name}    ${Password}

add course
    Add Course    ${Test Course Name Glibc}
    Add Course    ${Test Course Name Linux-core}

add file
    Verify Login Status    ${User Name}
    Select Course    ${Test Course Name Glibc}
#     Element Should Be Enabled    ${Add File Button}
#     Wait Until Element Is Visible    ${Add File Button}    3s
#     Element Should Be Visible    ${Add File Button}
#     Click Element    ${Add File Button}

delete course
    Delete Course    ${Test Course Name Linux-core}
    Delete Course    ${Test Course Name Glibc}

finally
    Close Browser
