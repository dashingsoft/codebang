*** Settings ***
Documentation     Basic business process test using SeleniumLibrary.
Library           SeleniumLibrary
Resource          util.robot

*** Test Cases ***
Initialize
    Open Codebang To Home Page

Login
    Login    ${User Name}    ${Password}

Add Course
    Add Course    ${Test Course Name Glibc}
    Add Course    ${Test Course Name Linux-core}

Add File
    Add File    ${Test File Name}

Delete Course
    Delete Course    ${Test Course Name Linux-core}
    Delete Course    ${Test Course Name Glibc}

Finally
    Close Browser
