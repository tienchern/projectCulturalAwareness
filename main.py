from model import Person

# list of different "people"
people: dict[str: Person]= dict()
current_person = 0


continue_chat = True



print("== DASHBOARD ==")
print("Welcome! Here you can chat with different people :D")

while continue_chat == True:
    print(f"Your current people are: {list(people.keys())}")
    print(f"""Your options are:
            \t* quit - terminate the program
            \t* delete [name] - delete person
            \t* create [country] [name] - create person
            \t* chat [name] - chat with person
        """)
    user_input = input("Enter: ")
    match user_input.split():
        case [action]:
            if action == "quit":
                continue_chat = False
        case [action, *objects]:
            if action == "create":
                new_person = Person(country=objects[0], name=objects[1])
                people[objects[1]] = new_person
            if action == "delete":
                people.pop(objects[0])
        case _:
            print("Command not recognized")






# print("Hello welcome to [name TBD], where you can chat with different people!")
# country = input("Enter the person's country of origin: ")
# people.append(Person(country=country))
# print(f"You want to talk with someone from this country {country}")

# # create the model



# while continue_chat:
#     # print(model.say_hi())
#     user_input = input("Enter your response ")
#     if user_input == "quit":
#         continue_chat = False
#     else:
#         print(model.respond(user_input)) 