# Created by Nem at 9/25/16
Feature:Guide Feature
  This feature contains test for the live guide functionality

  Scenario: test get images
    Given a source id
    When I get the images
    Then then images are returned
