Feature: easy copy
    Copy a file.

    Scenario: execute one file copy
        Given a "source" file is created
        When a copy from "source" file to "destination" file is run

        Then the "destination" file exists
