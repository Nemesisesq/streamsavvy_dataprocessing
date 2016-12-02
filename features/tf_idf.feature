# Created by Nem at 11/28/16
Feature: This Feature describes tests for Term Frequency - Inverse Document Frequency recomendation engine

  Scenario: Test tf_idf recommendation engine.
    Given our content engine
    When  we train our content engine
    Then We make a prediction

  Scenario: Test Predictor
    Given our content engine
    When  We make a prediction

  Scenario: Testing The Function that invokes the recomendation engine
    Given an id
    When we get_recomendations
    Then we get a combined list of shows


  Scenario: Testing Sending Recomendation to Rabbit MQ
    Given a payload
    Then we publish the payload to RabbitMQ

