Feature: remote configuration
    Configure connection parameters of a remote execution or copy

    Background: requirements are met
        Given a RemoteConfiguration is instantiated for toto@titi:4444

    Scenario: default properties can be retrieved
        Then username of remote configuration is toto
        And  host of remote configuration is titi
        And  port of remote configuration is 4444

    Scenario: default port property can be read as a generic property
        When port of remote configuration is set to 22
        Then port of remote configuration is 22
        And  Port of remote configuration is 22

    Scenario: generic port property can be read as a default property
        When Port of remote configuration is set to 4000
        Then port of remote configuration is 4000
        And  Port of remote configuration is 4000

    Scenario: default port property can be unset
        When port of remote configuration is removed
        Then port of remote configuration is unset

    Scenario: default username property can be read as a generic property
        When username of remote configuration is set to root
        Then username of remote configuration is root
        And  User of remote configuration is root

    Scenario: generic username property can be read as a default property
        When User of remote configuration is set to morty
        Then username of remote configuration is morty
        And  User of remote configuration is morty

    Scenario: default username property can be unset
        When username of remote configuration is removed
        Then username of remote configuration is unset

    Scenario: generic property can be set
        When IdentityFile of remote configuration is unset
        And  IdentityFile of remote configuration is set to /dev/null
        Then IdentityFile of remote configuration is /dev/null

    Scenario: generic property can be unset
        When IdentityFile of remote configuration is removed
        Then IdentityFile of remote configuration is unset

    Scenario: an instance can be converted to a unique string
        When a RemoteConfiguration is instantiated for toto@titi:4444
        Then remote configuration has __repr__ with port=4444 and user=toto
