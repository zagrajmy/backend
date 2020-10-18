Feature: Meeting API

  Scenario Outline: Create a meeting
    Given I am logged in as a user
    And there is a sphere
    And there is a guild I do belong to
    When I create a meeting with <data>
    Then I receive 201 response
    And Response data is equals to the data I have sent
    And Meeting status is <status>

    Examples: Creating meetings
      | data                              | status    |
      | start_time:empty                  | draft     |
      | end_time:empty                    | draft     |
      | publication_time:empty            | draft     |
      | publication_time:+1               | planned   |
      | publication_time:-1,start_time:+1 | published |

  Scenario: Create a meeting guild error
    Given I am logged in as a user
    And there is a sphere
    And there is a guild I don't belong to
    When I create a meeting
    Then I receive 400 response
    And Response data contains error "You cannot add a meeting to a guild you don't belong!" for field guild

  Scenario: Create a meeting organizer error
    Given I am logged in as a user
    And there is a sphere
    And there is a guild I do belong to
    When I create a meeting with organizer:user
    Then I receive 400 response
    And Response data contains error "You cannot add a meeting as a different person!" for field organizer

  Scenario Outline: Create a meeting with wrong start_time
    Given I am logged in as a user
    And there is a sphere
    And there is a guild I do belong to
    When I create a meeting with start_time:-1
    Then I receive 400 response
    And Response data contains error "You cannot add a meeting in the past!" for field organizer

  Scenario Outline: Update a meeting
    Given I am logged in as a user
    And there is a sphere
    And there is a guild I do belong to
    And there is a meeting connected to my guild and sphere
    When I update a meeting with <data>
    Then I receive 200 response
    And Response data is equals to the data I have sent
    And Meeting status is <status>

    Examples: Updating meetings
      | data                              | status    |
      | start_time:empty                  | draft     |
      | end_time:empty                    | draft     |
      | publication_time:empty            | draft     |
      | publication_time:+1               | planned   |
      | publication_time:-1,start_time:+1 | published |

  Scenario Outline: Update a meeting with wrong start_time
    Given I am logged in as a user
    And there is a sphere
    And there is a guild I do belong to
    And there is a past meeting connected to my guild and sphere
    When I update a meeting setting <field> to <value>
    Then I receive 400 response
    And Response data contains error "You cannot change the time of a past event!" for field <field>

    Examples: Updating meetings
      | field            | value |
      | end_time         | -1    |
      | publication_time | -5    |
      | start_time       | -3    |

  Scenario: Destroy a meeting
    Given I am logged in as a user
    And there is a sphere
    And there is a guild I do belong to
    And there is a meeting connected to my guild and sphere
    When I delete my meeting
    Then I receive 204 response
    And Meeting doesn't exist
