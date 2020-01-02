*** Settings ***
Documentation   Verifies storage keywords
Library         ImportResource  resources=importresource-testdata

*** Test Cases ***
Test ImportResource
  ${returnvalue}=   keyword from package importresource-testdata

  Should Be Equal   ${returnvalue}    importresource-testdata

  ${extres}=  External Resources
  Log To Console    ${extres}
