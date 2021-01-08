*** Settings ***
Resource    user_file_action.robot
Resource    login_action.robot
Resource    course_action.robot

*** Variables ***
${File Name}    tcp.h

*** Test Cases ***
Add File Before Login
    [Tags]    normal
    Click Add File Button
    Input File Name    ${File Name}
    Confirm To Add File
    File Should Be Added    ${File Name}

Add File After Login
    [Tags]    normal    main
    [Setup]   Run Keywords
    ...       Login With Default User    AND
    ...       Add Default Course
    Click Add File Button
    Input File Name    ${File Name}
    Confirm To Add File
    File Should Be Added    ${File Name}
    [Teardown]    Delete Default Course