Feature: simple copy
    Copy a file.

    Background: requirements are met
        Given a reactor is created

    Scenario: execute one file copy
        Given a "source" file is created
        And a remote copy from "source" file to "destination" file is created as "copy"
        And the execution "copy" is started

        When the reactor is run

        Then the "destination" file exists
        And the "copy" result code is "0"

    Scenario: interrupt one file copy
        Given a remote copy from "/dev/zero" file to "/dev/null" file is created as "copy"

        And a local run "echo finish" is created as "finish"
        And the execution "copy" is stopped when "finish" terminates

        And the execution "copy" is started
        And the execution "finish" is started

        When the reactor is run

        Then the "copy" result code is not "0"
