*** Settings ***
Resource         user_file_action.robot
Resource         login_action.robot
Resource         course_action.robot
Test Setup       Run Keywords
...              Login With Default User    AND
...              Add Default Course
Test Teardown    Delete Default Course

*** Variables ***
${File Name}    tcp.h
${Test Text}    hello world!

*** Test Cases ***
Add File Before Login
    [Tags]    normal    main
    [Setup]
    Click Add File Button
    Input File Name    ${File Name}
    Confirm To Add File
    File Should Be Added    ${File Name}
    [Teardown]

Add File After Login
    [Tags]    normal    main
    Click Add File Button
    Input File Name    ${File Name}
    Confirm To Add File
    File Should Be Added    ${File Name}

Edit File
    [Tags]    normal    main
    Add File    ${File Name}
    Input Test Text    ${Test Text}
    Current Text Should Be    ${Test Text}

Save File After Login
    [Tags]    normal    main
    Add File    ${File Name}
    Input Test Text    ${Test Text}
    Current Text Should Be    ${Test Text}
    Click Save File Button
    Logout
    Login With Default User
    Select Course    ${Default Course Name}
    File Should Be Added    ${File Name}
    Current Text Should Be    ${Test Text}
