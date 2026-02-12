using System.Security.Cryptography.X509Certificates;

Console.WriteLine("Welcome to the points tracker system.");
Console.WriteLine("Input the name of Team 1: ");
string t1 = Console.ReadLine();
Console.WriteLine("Input name of Team 2: ");
string t2 = Console.ReadLine();

Console.WriteLine("WELCOME TO  " + t1 + " vs " + t2);

int go = 1;
int p1 = 0;
int p2 = 0;

while (go == 1)
{
    Console.WriteLine("Select Team: (1 or 2)");
    string choose = Console.ReadLine();
    int choosen;

    if (int.TryParse(choose, out choosen))
    {
        if (choose == "1")
        {
            Console.WriteLine("How many points do you want to add?");
            string adds = Console.ReadLine();
            int add;
            if (int.TryParse(adds, out add))
            {
                if (add <= 3)
                {
                    p1 = p1 + add;
                    Console.WriteLine("Added " + add + " points to " + t1);
                }
                else
                {
                    Console.WriteLine("Please input a value under three");
                }

            }
        }
        if (choose == "2")
        {
            Console.WriteLine("You have selected " + choose + ". How many points do you want to add?");
            string adds = Console.ReadLine();
            int add;
            if (int.TryParse(adds, out add))
            {
                if (add <= 3)
                {
                    p2 = p2 + add;
                    Console.WriteLine("Added " + add + " points to " + t2);
                }
                else
                {
                    Console.WriteLine("Please input a value under three");
                }

            }
        }
        if (choose == "0")
        {
            go = 4;
        }

    }


}
Console.WriteLine(t1 + " achieved a total of: " + p1);
            Console.WriteLine(t2 + " achieved a total of: " + p2);
            if (p1 == p2)
            {
                Console.WriteLine("It's a tie!");
            }
            if (p1 > p2)
            {
                Console.WriteLine(t1 + " Wins! Congratulations!");
            }
            if (p2 > p1)
            {
                Console.WriteLine(t2 + " Wins! Congratulations!");
            }