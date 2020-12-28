*** Settings ***
Documentation     the login test suite
Metadata          Version    0.1
Library           SeleniumLibrary
Resource          ../common.robot
Resource          login_action.robot
Suite Setup       Open Codebang To Home Page
Suite Teardown    Close Browser
Test Teardown     Logout
