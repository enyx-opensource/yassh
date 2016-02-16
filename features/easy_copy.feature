Feature: easy copy
    Copy a file.

    Scenario: execute one file copy
        Given a "source" file is created

        When "source" is remotely copied to "destination" as "copy"

        Then the "destination" file exists
        And the "copy" result code is "0"
