Feature: checking products

    Scenario: add a product
        Given we want to add a product
        When we fill in the form
        Then it succeeds

    Scenario: adding product
        Given we have specific product to add
        | productNo | productName | category | sub_category | brand   | price  | types   | rating | description |
        | 7000      | VeryTasty  | seafood  | fish         | fishman | 10     | organic | 5      | very nice   |
        When we visit the list page
        Then we will find '7000'