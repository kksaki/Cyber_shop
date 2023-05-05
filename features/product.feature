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


    Scenario: visit the Cart
        Given a customer is logging in
        When the customer is accessing their cart
        Then the cart should be displayed with the correct products and quantities

    Scenario: visit the Orders
        Given a customer is logging in
        When the customer is accessing their order history
        Then the order history should display the correct orders with product information