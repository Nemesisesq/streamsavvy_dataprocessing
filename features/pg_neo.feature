# Created by Nem at 12/26/16
Feature: Pg_Neo
  this is to test the migration of data from postgres to Mongodb and Neo4j

  Scenario: test creation of nested content objects to dictionary objects.
    When we convert all content
    Then we have a list of dictionaries