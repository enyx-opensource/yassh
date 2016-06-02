Feature: encoding
    Run one with non ascii characters and expect non ascii output.

    Scenario: execute one correct command
        Given a reactor is created
          And an output buffer is created as "out"
          And a remote run "echo éäè" is created as "echo"
            | option | value |
            | output | out   |
          And the execution "echo" is started

        When the reactor is run

        Then the output buffer "out" content is
            """
            éäè
            """
