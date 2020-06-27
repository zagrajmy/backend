Feature: Sphere manager permissions

  Scenario Outline: Sphere manager can list his spheres
  	Given a set of staff users:
  		| username | groups         |
  		| Sam      | Sphere Manager |
  		| Max      | Sphere Manager |
  	Given 'visible' instance of <model> connected to Sam's sphere
    Given 'not_visible' instance of <model> connected to Max's sphere
    Given Sam is logged in
    When User tries <action> on model <model> in app <app>
    Then I can see only 'visible', not 'not_visible'

    Examples: Django Admin
      | app          | model      | action |
      | notice_board | sphere     | list   |
      | chronology   | room       | list   |
      | chronology   | agendaitem | list   |
      | chronology   | festival   | list   |
      | chronology   | waitlist   | list   |
      | chronology   | helper     | list   |
      | chronology   | timeslot   | list   |
      | chronology   | proposal   | list   |


  Scenario Outline: No access for Sphere Manager to list views
    Given a set of staff users:
      | username | groups         |
      | Sam      | Sphere Manager |
    Given Sam is logged in
    When User tries <action> on model <model> in app <app>
    Then The result is error code 403

    Examples: Django Admin
      | app          | model   | action | status |
      | crowd        | user    | create | 403    |
      | crowd        | user    | list   | 403    |
      | notice_board | guild   | create | 403    |
      | notice_board | guild   | list   | 403    |
      | notice_board | meeting | create | 403    |
      | notice_board | sphere  | create | 403    |



  Scenario Outline: No access for Sphere Manager to detail views
    Given a set of staff users:
      | username | groups         |
      | Sam      | Sphere Manager |
    Given there is any <model>
    Given Sam is logged in
    When User tries <action> on model <model> in app <app>
    Then The result is error code <status>

    Examples: Django Admin
      | app          | model  | action | status |
      | crowd        | user   | delete | 403    |
      | crowd        | user   | read   | 403    |
      | crowd        | user   | update | 403    |
      | notice_board | guild  | delete | 403    |
      | notice_board | guild  | read   | 403    |
      | notice_board | guild  | update | 403    |