*** Settings ***
Documentation    the test cases for course
Resource         course_action.robot
Resource         login_action.robot
Test Setup       Login    devecor    t
Test Teardown    Logout

*** Variables ***
${Course Name}            glibc
${New Course Name}        glibc-new
${Another Course Name}    linux-core


*** Test Cases ***
Add Course After Login
    [Tags]    main    normal
    Click Add Course Button
    Input Course Name    ${Course Name}
    Confirm To Add Course
    Current Course Should Be    ${Course Name}
    [Teardown]    Run Keywords
    ...           Delete Course    ${Course Name}    AND
    ...           Logout

Add Course Before Login
    [Tags]    abnormal
    [Setup]
    Click Add Course Button
    Verify Course Can Not Be Added
    [Teardown]

Delete Course After Login
    [Tags]    main    normal
    Add Course    ${Course Name}
    Select Course    ${Course Name}
    Click Button To Delete Course
    Confirm To Delete Course
    Wait Until Animation Is Finished
    Course Should Be Deleted    ${Course Name}

Rename Course After Login
    [Tags]    main normal
    Add Course    ${Course Name}
    Select Course    ${Course Name}
    Click Button To Rename Course
    Input New Course Name    ${New Course Name}
    Confirm To Rename Course
    Current Course Should Be    ${New Course Name}
    Delete Course    ${New Course Name}

Course Renaming Or Deletion Before Login
    [Tags]    abnormal
    [Setup]
    Verify Course Can Not Be Deleted
    Verify Course Can Not Be Renamed
    [Teardown]

Switch Another Course After Login
    [Tags]    normal   fail
    Add Course    ${Course Name}
    Add Course    ${Another Course Name}
    Select Course    ${Course Name}
    Delete Course    ${Course Name}
    Delete Course    ${Another Course Name}