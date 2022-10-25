#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *input_file = fopen(argv[1], "r");

    if (input_file == NULL)
    {
        printf("Error\n");
        return 2;
    }
    unsigned char buffer[512];

    int count_image = 0;

    FILE *output_file = NULL;

    char *filename = mallot(8 * sizeof(char));
}