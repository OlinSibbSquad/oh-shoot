# import roomba_tracking as rt
import charge_credit_card as ccc


choice = input("Are you demoing or purchasing? (1/0)?")
if (int(choice) == 1):
    # rt.main()
    pass
else:
    response = input("This will cost $1 per unit. Are you sure you are okay with this? (y/n)")
    if(response == "y"):
        ccc.charge_credit_card(1)
    else:
        print("Thanks for checking, and have a great day!")
