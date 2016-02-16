Feature: logged run
    Run binaries and save their output.

    Background: requirements are met
        Given a reactor is created
        And an output buffer is created as "out_local"
        And an output buffer is created as "out_remote"

    Scenario: enter context and execute one command
        Given a remote run "echo remote" is created as "echo_remote"
            | option | value      |
            | output | out_remote |
        And the execution "echo_remote" is started

        Given a local run "echo local" is created as "echo_local"
            | option | value     |
            | output | out_local |
        And the execution "echo_local" is started

        When the reactor is run

        Then the output buffer "out_remote" content is
            """
            remote
            """
        Then the output buffer "out_local" content is
            """
            local
            """

