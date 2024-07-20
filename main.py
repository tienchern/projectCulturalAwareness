import os
from model import Person
import os

people: dict[str: Person]= dict()


def main():

    continue_program = True
    print("\n" * 100)
    print("Welcome! Here you can chat with different people :D")

    while continue_program == True:
        print("== DASHBOARD ==")
        print(f"Your current people are: {list(people.keys())}")
        print(f"""Your options are:
                \t* quit - terminate the program
                \t* delete [name] - delete person
                \t* create [name] [country] [age] - create person
                \t* chat [name] - chat with person
            """)
        user_input = input("Enter: ")
        match user_input.split():
            case [action]:
                if action == "quit":
                    continue_program = False
                    if os.path.exists("output.jpg"):
                        os.remove("output.jpg")
                else:
                    print("ERROR, command not recognized")
            case [action, name]:
                if action == "delete":
                    if name in people:
                        people.pop(name)
                    else:
                        print("ERROR, person does not exist")
                elif action == "chat":
                    if name in people:
                        chat(people[name])
                    else:
                        print("ERROR: person does not exist")
                else:
                    print("ERROR, command not recognized")

            case [action, *objects]:
                if action == "create":
                    if len(objects) < 3:
                        print("ERROR, not enough arguments supplied")
                    new_person = Person(country=objects[1], name=objects[0], age=objects[2])
                    people[objects[0]] = new_person

            case _:
                print("ERROR, Command not recognized")
            
        print("\n" * 4)



def chat(person: Person):
    
    continue_chat = True

    print(f"== CHAT WITH {str(person).upper()} ==")
    print("Type 'exit' to return to dashboard")
    print(person.say_hi())

    while continue_chat:
        user_input = input("Enter: ")
        if user_input == "exit":
            continue_chat = False
            os.remove("output.jpg")
        else:
            print(person.respond(user_input))


if __name__ == "__main__":
    main()