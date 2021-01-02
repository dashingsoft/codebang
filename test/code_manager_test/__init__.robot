*** Settings ***
Documentation     the code manager test suite
Metadata          Version    0.1
Library           SeleniumLibrary
Resource          ../common.robot
Suite Setup       Open Codebang To Home Page
Suite Teardown    Close Browser
