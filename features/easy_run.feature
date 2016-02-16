Feature: easy run
    Run one binary at a time discarding its output.

    Scenario: execute one correct command
        When "echo remote" is remotely run as "echo_remote"
        And "echo local" is locally run as "echo_local"
        Then the "echo_remote" result code is "0"
        And the "echo_local" result code is "0"

    Scenario: execute one wrong command
        When "ls /non_existent" is remotely run as "faulty_ls_remote"
        And "ls /non_existent" is locally run as "faulty_ls_local"
        Then the "faulty_ls_remote" result code is not "0"
        And the "faulty_ls_local" result code is not "0"

