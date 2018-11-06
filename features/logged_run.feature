Feature: logged run
    Run binaries and save their output.

    Background: requirements are met
        Given a reactor is created

    Scenario: Execute two commands returning output
        Given an output buffer is created as "out_remote"
        And a remote run "echo remote" is created as "echo_remote"
            | option | value      |
            | output | out_remote |
        And the execution "echo_remote" is started

        Given an output buffer is created as "out_local"
        And a local run "echo local" is created as "echo_local"
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
    Scenario: Execute one command returning multiline output
        Given an output buffer is created as "out_multiline"
        And a remote run "printf 'line 1\nline 2\n'" is created as "echo_multiline"
            | option | value         |
            | output | out_multiline |
        And the execution "echo_multiline" is started

        When the reactor is run

        Then the output buffer "out_multiline" content is
            """
            line 1
            line 2
            """

