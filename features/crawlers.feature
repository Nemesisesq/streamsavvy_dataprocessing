# Created by Nem at 8/19/16
Feature: This feature is to test crawlers
  the following scenarios are tests to verify the function of crawlers

  Scenario: test ncaaf crawlers
    When we run the ncaaf crawler
    Then we get schedules with shows
