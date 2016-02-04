Feature: simple run
    Run independent binaries and match their output.

    Background: requirements are met
        Given a reactor is created

    Scenario: execute one command
        Given a command "echo ok" is created as "echo"
        And the command "echo" is monitored for "ok" pattern
        And the command "echo" is started

        And the reactor is stopped after "echo" terminates

        When the reactor is run

        Then pattern "ok" has been matched "1" times

    Scenario: execute two commands concurrently
        Given a command "echo 1" is created as "first"
        And the command "first" is monitored for "1" pattern
        And the command "first" is started

        And a command "echo 2" is created as "second"
        And the command "second" is monitored for "2" pattern
        And the command "second" is started

        And the reactor is stopped after following commands terminate
            | command |
            | first   |
            | second  |

        When the reactor is run

        Then pattern "1" has been matched "1" times
        And pattern "2" has been matched "1" times

