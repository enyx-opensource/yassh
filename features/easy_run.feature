Feature: easy run
    Run one binary at a time discarding its output.

    Scenario: execute one correct command
        When a command "echo ok" is run as "echo"
        Then the command "echo" result code is "0"

    Scenario: execute one wrong command
        When a command "ls /non_existent" is run as "faulty_ls"
        Then the command "faulty_ls" result code is not "0"

