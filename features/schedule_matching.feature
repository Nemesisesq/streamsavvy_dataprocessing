# Created by Nem at 8/15/16
Feature: Schedule Matching
  # Enter feature description here
  This feature is to connect the schedules crawled from espn to sports that are indexed in elastic search

  Scenario: NCAAF schedule matching
    Given a list of ncaaf teams
    When we match all the schedules
    Then the teams in the Sport model have schedules
    # Enter steps here
