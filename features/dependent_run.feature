Feature: dependent run
    Achieve complex asynchronous executions of dependant tasks.

    Background: requirements are met
        Given a reactor is created

    Scenario: second run is executed when first terminates
        Given a remote run "echo 1" is created as "first_echo"
        And the execution "first_echo" is started

        And a local run "echo 2" is created as "second_echo"
        And the execution "second_echo" is started when "first_echo" terminates
        And the execution "second_echo" is monitored for "2" pattern

        When the reactor is run

        Then pattern "1" hasn't been matched
        And pattern "2" has been matched "1" times

    Scenario: first run is killed when second terminates
        Given a remote run "sleep 100 && echo sleep_finished" is created as "sleep"
        And the execution "sleep" is monitored for "sleep_finished" pattern
        And the execution "sleep" is started

        And a local run "echo ok" is created as "echo"
        And the execution "echo" is monitored for "ok" pattern
        And the execution "echo" is started

        And the execution "sleep" is stopped when "echo" terminates

        When the reactor is run

        Then pattern "sleep_finished" hasn't been matched
        And pattern "ok" has been matched "1" times

