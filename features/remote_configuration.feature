Feature: remote configuration
    Configure connection parameters of a remote execution or copy

    Background: requirements are met
        Given a RemoteConfiguration is instantiated for "toto@titi:4444"

    Scenario: default properties can be retrieved
        Then "username" of remote configuration is "toto"
        And "host" of remote configuration is "titi"
        And "port" of remote configuration is "4444"

    Scenario: default port property can be read as a generic property
        When "port" of remote configuration is set to "22"
        Then "port" of remote configuration is "22"
        And "Port" of remote configuration is "22"

    Scenario: generic port property can be read as a default property
        When "Port" of remote configuration is set to "4000"
        Then "port" of remote configuration is "4000"
        And "Port" of remote configuration is "4000"

    Scenario: default port property can be unset
        Given "port" of remote configuration is set to "22"
        When "port" of remote configuration is removed
        Then "port" of remote configuration is "unset"

    Scenario: default username property can be read as a generic property
        Given "username" of remote configuration is set to "root"
        Then "username" of remote configuration is "root"
        And "User" of remote configuration is "root"

    Scenario: generic username property can be read as a default property
        Given "User" of remote configuration is set to "morty"
        Then "username" of remote configuration is "morty"
        And "User" of remote configuration is "morty"

    Scenario: default username property can be unset
        Given "User" of remote configuration is set to "test"
        When "username" of remote configuration is removed
        Then "username" of remote configuration is "unset"

    Scenario: generic property can be set
        Given "IdentityFile" of remote configuration is "unset"
        When "IdentityFile" of remote configuration is set to "/dev/null"
        Then "IdentityFile" of remote configuration is "/dev/null"

    Scenario: generic property can be unset
        Given "IdentityFile" of remote configuration is set to ".ssh/known_hosts"
        When "IdentityFile" of remote configuration is removed
        Then "IdentityFile" of remote configuration is "unset"

    Scenario: an instance can be converted to a unique string
        Then remote configuration __repr__() contains port "4444" and user "toto"
