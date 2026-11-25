
print("Bob Bot: What would you like to know?")

user_request = input("You: ")

if "selly oak" in user_request.lower():

    print("\nBob Bot: What sort of update source would you like?")
    print("1. News sources")
    print("2. Academic sources")
    print("3. Social media")

    choice = input("\nYou: ")

    if choice == "1":
        print("\nBob Bot: You have selected news sources.")
        print("Available simulated sources:")
        print("- BBC News: Birmingham bin strikes")
        print("- ITV News: Selly Oak waste collection updates")

        feedback = input("\nBob Bot: Are the sources satisfactory? ")

        if feedback.lower() == "yes":
            print("Bob Bot: Thank you for confirming.")
        else:
            print("Bob Bot: Please specify your preferred sources.")

    elif choice == "2":
        print("Bob Bot: No academic sources available.")

    elif choice == "3":
        print("Bob Bot: Simulated TikTok source found.")

    else:
        print("Bob Bot: Please select a valid source option.")

else:
    print("Bob Bot: No supporting information available.")
