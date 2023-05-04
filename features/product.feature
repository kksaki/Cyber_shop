Feature: checking products

    Scenario: add a product
        Given we want to add a product
        When we fill in the form
        Then it succeeds

    Scenario: adding product
        Given we have specific product to add
        | productNo | productName | category | sub_category | brand   | price  | types   | rating | description | created_date  | image |
        | 7000      | Very Tasty  | seafood  | fish         | fishman | 10     | organic | 5      | very nice   | 2020-10-14T00:00:00Z | products/2023/05/03/111.jpg |
        When we visit the list page
        Then we will find 'Very Tasty'