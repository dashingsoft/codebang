*** Settings ***
Documentation     A common utility keywords resource file.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.
Library           SeleniumLibrary


*** Variables ***
${URL}            http://localhost:8080/app
${BROWSER}        chrome


*** Keywords ***
Open Codebang To Home Page
    Set Selenium Speed    0
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Title Should Be  codebang    can not open codebang

Wait Until Animation Is Finished
    Sleep    0.5s