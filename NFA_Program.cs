using System;
using System.Collections.Generic;

class NFACStyleComment
{
    enum State { q0, q1, q2, q3, q4 }

    public static bool IsAccepted(string input)
    {
        HashSet<State> currentStates = new HashSet<State> { State.q0 };

        foreach (char symbol in input)
        {
            HashSet<State> nextStates = new HashSet<State>();

            foreach (State state in currentStates)
            {
                switch (state)
                {
                    case State.q0:
                        // δ(q0, /) = q1 ; δ(q0, *) = ∅ ; δ(q0, j) = ∅
                        if (symbol == '/') nextStates.Add(State.q1);
                        break;

                    case State.q1:
                        // δ(q1, *) = q2 ; δ(q1, j) = q0 ; δ(q1, /) = q0
                        if (symbol == '*') nextStates.Add(State.q2);
                        else if (symbol == 'j') nextStates.Add(State.q0);
                        else if (symbol == '/') nextStates.Add(State.q0);
                        break;

                    case State.q2:
                        // Inside the comment body, no '*' seen yet (or last char wasn't '*').
                        // δ(q2, j) = q2 ; δ(q2, /) = q2 ; δ(q2, *) = q3
                        // NOTE: '*' moves ONLY to q3 now (not also staying at q2).
                        // This removes the branching that let an early "*/" be
                        // "ignored" by a parallel thread that kept looping at q2.
                        if (symbol == 'j' || symbol == '/') nextStates.Add(State.q2);
                        else if (symbol == '*') nextStates.Add(State.q3);
                        break;

                    case State.q3:
                        // Just saw a '*' inside the comment - watching for the closing '/'.
                        // δ(q3, /) = q4 (comment closes HERE, at the first "*/")
                        // δ(q3, *) = q3 (consecutive stars, e.g. "**", keep watching)
                        // δ(q3, j) = q2 (star wasn't followed by '/', back to normal body)
                        if (symbol == '/') nextStates.Add(State.q4);
                        else if (symbol == '*') nextStates.Add(State.q3);
                        else if (symbol == 'j') nextStates.Add(State.q2);
                        break;

                    case State.q4:
                        // δ(q4, symbol) = ∅ for all symbols.
                        // Doing nothing here ensures q4 is NOT carried forward
                        // if extra characters exist after the comment closes.
                        break;
                }
            }

            // Update active states for the NEXT character
            currentStates = nextStates;

            // Early termination if all computational paths died
            if (currentStates.Count == 0) break;
        }

        return currentStates.Contains(State.q4);
    }

    static void Main()
    {
        Console.WriteLine("--------------------------------------------------");
        Console.WriteLine("     C-Style Comment NFA Evaluator (Σ = {j, *, /}) ");
        Console.WriteLine("--------------------------------------------------");
        Console.WriteLine("Type 'exit' to quit the program.\n");

        while (true)
        {
            Console.Write("Enter string to test: ");
            string input = Console.ReadLine();

            if (input == null) break;

            if (input.ToLower() == "exit")
            {
                Console.WriteLine("Exiting program...");
                break;
            }

            bool accepted = IsAccepted(input);

            if (accepted)
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("Result: ACCEPTED\n");
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("Result: REJECTED\n");
            }

            Console.ResetColor();
        }
    }
}