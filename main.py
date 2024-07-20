from model import Person

# list of different "people"
people: dict[str: Person]= dict()


def main():

    continue_program = True
    print("== DASHBOARD ==")
    print("Welcome! Here you can chat with different people :D")

    while continue_program == True:
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
                    continue_program = False
            case [action, name]:
                if action == "delete":
                    people.pop(name)
                elif action == "chat":
                    if name in people:
                        chat(people[name])
                    else:
                        print("ERROR: person does not exist")

            case [action, *objects]:
                if action == "create":
                    new_person = Person(country=objects[0], name=objects[1])
                    people[objects[1]] = new_person

            case _:
                print("Command not recognized")



def chat(person: Person):
    
    continue_chat = True

    print(f"== CHAT WITH {str(person).upper()}==")
    print("Type 'exit' to return to dashboard")
    print(person.say_hi())

    user_input = input("Enter: ")

    while user_input != "exit":
        print(person.respond(user_input.strip()), flush=True)
        user_input = input("Enter: ")
    



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


if __name__ == "__main__":
    main()