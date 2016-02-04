Feature: dependent run
    Achieve complex asynchronous executions of dependant tasks.

    Background: requirements are met
        Given a reactor is created

    Scenario: second command is executed when first terminates
        Given a command "echo 1" is created as "first_echo"
        And the command "first_echo" is started

        And a command "echo 2" is created as "second_echo"
        And the command "second_echo" is started when "first_echo" terminates
        And the command "second_echo" is monitored for "2" pattern

        And the reactor is stopped after "second_echo" terminates

        When the reactor is run

        Then pattern "1" hasn't been matched
        And pattern "2" has been matched "1" times

    Scenario: first command is killed when second terminates
        Given a command "sleep 100 && echo sleep_finished" is created as "sleep"
        And the command "sleep" is monitored for "sleep_finished" pattern
        And the command "sleep" is started

        And a command "echo ok" is created as "echo"
        And the command "echo" is monitored for "ok" pattern
        And the command "echo" is started

        And the command "sleep" is stopped when "echo" terminates

        And the reactor is stopped after "sleep" terminates

        When the reactor is run

        Then pattern "sleep_finished" hasn't been matched
        And pattern "ok" has been matched "1" times

