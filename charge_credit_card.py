"""
Charge a credit card
"""

import imp
import os
import sys

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController

CONSTANTS = imp.load_source('modulename', 'constants.py')


def charge_credit_card(amount):
    """
    Charge a credit card
    """

    # Create a merchantAuthenticationType object with authentication details
    # retrieved from the constants file
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = CONSTANTS.apiLoginId
    merchantAuth.transactionKey = CONSTANTS.transactionKey

    # Create the payment data for a credit card
    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber = input("Credit card number please! ")
    creditCard.expirationDate = input("Expiration date (year-mo): ")
    creditCard.cardCode = input("CVV Code")

    # Add the payment data to a paymentType object
    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    # Create order information
    order = apicontractsv1.orderType()
    order.invoiceNumber = input("Invoice Number: ")
    order.description = input("Order description: ")

    # Set the customer's Bill To address
    customerAddress = apicontractsv1.customerAddressType()
    customerAddress.firstName = input("Customer first name: ")
    customerAddress.lastName = input("Customer last name: ")
    customerAddress.company = input("Customer company: ")
    customerAddress.address = input("Customer address: ")
    customerAddress.city = input("City: ")
    customerAddress.state = input("State: ")
    customerAddress.zip = input("Zip code: ")
    customerAddress.country = input("Country; ")

    # Set the customer's identifying information
    customerData = apicontractsv1.customerDataType()
    customerData.type = "individual"
    customerData.id = "99999456654"
    customerData.email = input("Customer email: ")

    # Add values for transaction settings
    duplicateWindowSetting = apicontractsv1.settingType()
    duplicateWindowSetting.settingName = "duplicateWindow"
    duplicateWindowSetting.settingValue = "600"
    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(duplicateWindowSetting)

    # setup individual line items
    line_item_1 = apicontractsv1.lineItemType()
    line_item_1.itemId = "12345"
    line_item_1.name = "first"
    line_item_1.description = "Here's the first line item"
    line_item_1.quantity = int(input("How many do you want? "))
    line_item_1.unitPrice = line_item_1.quantity
    # print("That will cost " + line_item_1.quantity)


    # build the array of line items
    line_items = apicontractsv1.ArrayOfLineItem()
    line_items.lineItem.append(line_item_1)


    # Create a transactionRequestType object and add the previous objects to it.
    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = amount
    transactionrequest.payment = payment
    transactionrequest.order = order
    transactionrequest.billTo = customerAddress
    transactionrequest.customer = customerData
    transactionrequest.transactionSettings = settings
    transactionrequest.lineItems = line_items

    # Assemble the complete transaction request
    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId = "MerchantID-0001"
    createtransactionrequest.transactionRequest = transactionrequest
    # Create the controller
    createtransactioncontroller = createTransactionController(
        createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()

    print("Thank you for shopping!")

    if response is not None:
        # Check to see if the API request was successfully received and acted upon
        if response.messages.resultCode == "Ok":
            # Since the API request was successful, look for a transaction response
            # and parse it to display the results of authorizing the card
            if hasattr(response.transactionResponse, 'messages') is True:
                print(
                    'Successfully created transaction with Transaction ID: %s'
                    % response.transactionResponse.transId)
                print('Transaction Response Code: %s' %
                      response.transactionResponse.responseCode)
                print('Message Code: %s' %
                      response.transactionResponse.messages.message[0].code)
                print('Description: %s' % response.transactionResponse.
                      messages.message[0].description)
            else:
                print('Failed Transaction.')
                if hasattr(response.transactionResponse, 'errors') is True:
                    print('Error Code:  %s' % str(response.transactionResponse.
                                                  errors.error[0].errorCode))
                    print(
                        'Error message: %s' %
                        response.transactionResponse.errors.error[0].errorText)
        # Or, print errors if the API request wasn't successful
        else:
            print('Failed Transaction.')
            if hasattr(response, 'transactionResponse') is True and hasattr(
                    response.transactionResponse, 'errors') is True:
                print('Error Code: %s' % str(
                    response.transactionResponse.errors.error[0].errorCode))
                print('Error message: %s' %
                      response.transactionResponse.errors.error[0].errorText)
            else:
                print('Error Code: %s' %
                      response.messages.message[0]['code'].text)
                print('Error message: %s' %
                      response.messages.message[0]['text'].text)
    else:
        print('Null Response.')

    return response


if (os.path.basename(__file__) == os.path.basename(sys.argv[0])):
    charge_credit_card(CONSTANTS.amount)
