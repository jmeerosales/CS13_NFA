using System;

class CStyleCommentDFA
{
    enum State { q0, q1, q2, q3, q4 }

    public static bool IsAccepted(string input)
    {
        State currentState = State.q0;

        foreach (char symbol in input)
        {
            switch (currentState)
            {
                case State.q0:
                    if (symbol == '/') currentState = State.q1;
                    else return false;
                    break;

                case State.q1:
                    if (symbol == '*') currentState = State.q2;
                    else return false;
                    break;

                case State.q2:
                    if (symbol == 'j' || symbol == '/') currentState = State.q2;
                    else if (symbol == '*') currentState = State.q3;
                    else return false;
                    break;

                case State.q3:
                    if (symbol == '*') currentState = State.q3;
                    else if (symbol == 'j') currentState = State.q2;
                    else if (symbol == '/') currentState = State.q4;
                    else return false;
                    break;

                case State.q4:
                    // Trap / Accept state: any extra character invalidates the comment
                    return false;
            }
        }

        // Returns true only if execution ends at accept state q4
        return currentState == State.q4;
    }

    static void Main()
    {
        Console.WriteLine("--------------------------------------------------");
        Console.WriteLine("     C-Style Comment Evaluator (Σ = {j, *, /})    ");
        Console.WriteLine("--------------------------------------------------");
        Console.WriteLine("Type 'exit' to quit the program.\n");

        while (true)
        {
            Console.Write("Enter string to test: ");
            string input = Console.ReadLine();

            // Exit condition
            if (input.ToLower() == "exit")
            {
                Console.WriteLine("Exiting program...");
                break;
            }

            bool accepted = IsAccepted(input);

            if (accepted)
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine($"Result: ACCEPTED\n");
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"Result: REJECTED\n");
            }

            Console.ResetColor(); 
        }
    }
}