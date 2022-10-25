#include <cs50.h>
#include <stdio.h>

int main(void)
{   int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    int i;
    for (i = 0; i < height -1; i++)
    {
        printf(" ");
    }
    for (i = height; i > 0; i--)
    {
        printf("#");
    }


}