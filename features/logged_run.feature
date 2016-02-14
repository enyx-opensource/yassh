Feature: logged run
    Run binaries and save their output.

    Background: requirements are met
        Given a reactor is created
        And an output buffer is created as "out"

    Scenario: enter context and execute one command
        Given a run "echo ok" is created as "echo"
            | option | value |
            | output | out   |
        And the execution "echo" is started

        When the reactor is run

        Then the output buffer "out" content is
            """
            ok
            """

