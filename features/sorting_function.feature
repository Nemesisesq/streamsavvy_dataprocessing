# Created by Nem at 6/28/16
Feature: Sorting Function
  These are tests to sort the shows by service to replace the front end functions int he javascript

  @rest_api
  Scenario: reduce channels in content
    Given a package
    When we pull out the channels
    Then we have a list of channels
    # Enter steps here

  Scenario Outline: Getting popularity scores for Content
    Given The Content <content>
    When We call the popularity service
    Then Content has a popularity score

    Examples: Titles
    |content                |
    |Orange Is the New Black|
    |Mr. Robot              |
