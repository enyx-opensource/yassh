Feature: contextual run
    Run binary using the Context to pass common arguments.

    Background: requirements are met
        Given a context "context" is created

    Scenario: execute one command without entering context
        When a context "context" command "echo ok" is run it raises "Missing variable"

    Scenario: enter context and execute one command
        Given the context "context" is entered
        When a context "context" command "echo ok" is run as "echo"
        Then the command "echo" result code is "0"
        And the context "context" is exited


