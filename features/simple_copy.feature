Feature: simple copy
    Copy a file.

    Background: requirements are met
        Given a reactor is created

    Scenario: execute one file copy
        Given a "source" file is created
        And a copy from "source" file to "destination" file is created as "copy"
        And the execution "copy" is started

        When the reactor is run

        Then the "destination" file exists
        And the "copy" result code is "0"
