Feature: simple run
    Run independent binaries and match their output.

    Background: requirements are met
        Given a reactor is created

    Scenario: create two command and check representation.
        Given a remote run "echo ok" is created as "echo1"

        And a remote run "echo ok" is created as "echo2"

        Then the executions strings are different

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

    Scenario: try to start the same command two times
        Given a remote run "echo 1" is created as "first"

        When the execution "first" is started

        Then starting the execution "first" again should raise

    Scenario: try to stop a non-started command
        Given a remote run "echo remote" is created as "echo_remote"
        Given a local run "echo local" is created as "echo_local"

        When no execution is started

        Then stopping the execution "echo_remote" should not raise
        And stopping the execution "echo_remote" should not raise
