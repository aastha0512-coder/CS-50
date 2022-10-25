#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int Red = image[i][j].rgbtRed;
            int Blue = image[i][j].rgbtGreen;
            int Green = image[i][j].rgbtGreen;
            float average = round(((float)Red + (float)Green + (float)Blue)/3.0);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;

        }
    }
    return;
}
int limit(int RGB)
{
    if (RGB > 255)
    {
        RGB = 255;
    }
    return RGB;
}
// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalBlue = image[i][j].rgbtGreen;
            int originalGreen = image[i][j].rgbtGreen;
            int sepiaRed = limit(round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue));
            int sepiaGreen = limit(round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue));
            int sepiaBlue = limit(round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue));
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaBlue;
            image[i][j].rgbtBlue = sepiaGreen;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int temp[3];
     for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++) {

            /** Swap pixels from left to right */
            temp[0] = image[i][j].rgbtBlue;
            temp[1] = image[i][j].rgbtGreen;
            temp[2] = image[i][j].rgbtRed;

            image[i][j].rgbtBlue = image[i][width - j - 1].rgbtBlue;
            image[i][j].rgbtGreen = image[i][width - j - 1].rgbtGreen;
            image[i][j].rgbtRed = image[i][width - j - 1].rgbtRed;

            image[i][width - j - 1].rgbtBlue = temp[0];
            image[i][width - j - 1].rgbtGreen = temp[1];
            image[i][width - j - 1].rgbtRed = temp[2];

        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int totalRed, totalBlue, totalGreen;
            totalRed = totalBlue = totalGreen = 0;
            float counter = 0.00;

            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    int currentx = x + i;
                    int currenty = j + y;

                    if (currentx < 0 || currenty < 0 || currentx > (height - 1) || currenty > (width - 1))
                    {
                        continue;
                    }
                    totalRed += temp[currentx][currenty].rgbtRed;
                    totalBlue += temp[currentx][currenty].rgbtBlue;
                    totalGreen += temp[currentx][currenty].rgbtGreen;
                    counter++;

                }


            }
            temp[i][j].rgbtRed = round(totalRed / counter);
            temp[i][j].rgbtBlue = round(totalBlue / counter);
            temp[i][j].rgbtGreen = round(totalGreen / counter);

        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }
    return;
}
