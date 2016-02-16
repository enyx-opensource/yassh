Feature: simple run
    Run independent binaries and match their output.

    Background: requirements are met
        Given a reactor is created

    Scenario: execute one command
        Given a remote run "echo ok" is created as "echo"
        And the execution "echo" is monitored for "ok" pattern
        And the execution "echo" is started

        When the reactor is run

        Then pattern "ok" has been matched "1" times

    Scenario: execute two commands concurrently
        Given a remote run "echo 1" is created as "first"
        And the execution "first" is monitored for "1" pattern
        And the execution "first" is started

        And a remote run "echo 2" is created as "second"
        And the execution "second" is monitored for "2" pattern
        And the execution "second" is started

        When the reactor is run

        Then pattern "1" has been matched "1" times
        And pattern "2" has been matched "1" times

