Feature: contextual run
    Run binary using the Context to pass common arguments.

    Scenario: enter context and execute one command
        Given a context is created
        When a context command "echo ok" is run as "echo"
        Then the command "echo" result code is "0"

    Scenario: execute one command without entering context
        When a context command "echo ok" is run it raises "Missing variable"

