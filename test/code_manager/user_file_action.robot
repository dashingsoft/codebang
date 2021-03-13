*** Settings ***
Library    SeleniumLibrary
Library    String

*** Variables ***
${Add File Button}               xpath: //div/button[@title="新增文件"]
${Confirm To Add File Button}    xpath: //div[@class="el-message-box"]/descendant::button[contains(./span/text(), "确定")]
${Save File Button}              xpath: //button[@title="保存文件"]
${Add File Input}                xpath: //div[@class="el-message-box"]/descendant::div[@class="el-input"]/input
${Textarea}                      xpath: //textarea[@class="ace_text-input"]

*** Keywords ***
Click Add File Button
    Mouse Down    ${Add File Button}
    Mouse Up    ${Add File Button}

Input File Name
    [Arguments]    ${File Name}
    Input Text    ${Add File Input}    ${File Name}

Confirm To Add File
    Click Button    ${Confirm To Add File Button}
    Wait Until Element Is Not Visible    ${Confirm To Add File Button}    1s

File Should Be Added
    [Arguments]    ${File Name}
    @{Name} =    Get Regexp Matches    ${File Name}    ^[^.]+
    Wait Until Page Contains Element
    ...    xpath: //tbody/descendant::div[contains(span, "${Name}[0]")]
    ...    0.5s
    ...    ${File Name} should be added, but it not be

Add File
    [Arguments]    ${File Name}
    Click Add File Button
    Input File Name    ${File Name}
    Confirm To Add File
    File Should Be Added    ${File Name}

Input Test Text
    [Arguments]    ${Text}
    Input Text    ${Textarea}    ${Text}

Current Text Should Be
    [Arguments]    ${Text}
    Textarea Value Should Be    ${Textarea}    ${Text}

Click Save File Button
    Mouse Down    ${Save File Button}
    Mouse Up    ${Save File Button}
