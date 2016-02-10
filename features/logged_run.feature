Feature: logged run
    Run binaries and save their output.

    Background: requirements are met
        Given a reactor is created

    Scenario: enter context and execute one command
        Given a logged command "echo ok" is created as "echo"
        And the command "echo" is started

        When the reactor is run

        Then the logged content is
            """
            ok
            """

