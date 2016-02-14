Feature: easy run
    Run one binary at a time discarding its output.

    Scenario: execute one correct command
        When "echo ok" is run as "echo"
        Then the "echo" result code is "0"

    Scenario: execute one wrong command
        When "ls /non_existent" is run as "faulty_ls"
        Then the "faulty_ls" result code is not "0"

