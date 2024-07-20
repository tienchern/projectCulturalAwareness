import model

# list of different "people"
people = []
continue_chat = True

print("Hello welcome to [name TBD], where you can chat with different people!")
country = input("Enter the person's country of origin: ")
print(f"You want to talk with someone from this country {country}")

# create the model
while continue_chat:
    print(model.say_hi())
    user_input = input("Enter your response (type quit to quit): ")
    if user_input == "quit":
        continue_chat = False
    else:
        print(model.respond(user_input))