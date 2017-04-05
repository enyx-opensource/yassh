Feature: remote configuration
    Configure connection paramers of a remote execution or copy

    Scenario: test1
        # Test constructor
        When a RemoteConfiguration is instantiated for toto@titi:4444
        Then username of remote configuration is toto
        And  host of remote configuration is titi
        And  port of remote configuration is 4444

        # remote.port and remote.get('Port') are the same thing
        When port of remote configuration is set to 22
        Then port of remote configuration is 22
        And  Port of remote configuration is 22

        When Port of remote configuration is set to 4000
        Then port of remote configuration is 4000
        And  Port of remote configuration is 4000

        When port of remote configuration is removed
        Then port of remote configuration is unset

        # remote.username and remote.get('User') are the same thing
        When username of remote configuration is set to root
        Then username of remote configuration is root
        And  User of remote configuration is root

        When User of remote configuration is set to morty
        Then username of remote configuration is morty
        And  User of remote configuration is morty

        When username of remote configuration is removed
        Then username of remote configuration is unset

        # Test a generic property
        When IdentityFile of remote configuration is unset
        And  IdentityFile of remote configuration is set to /dev/null
        Then IdentityFile of remote configuration is /dev/null

        When IdentityFile of remote configuration is removed
        Then IdentityFile of remote configuration is unset

        When a RemoteConfiguration is instantiated for toto@titi:4444
        Then remote configuration has __repr__ with port=4444 and user=toto
