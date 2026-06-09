#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Dynamic string buffer structure with automatic growth capability
typedef struct
{
    char *data;      // Pointer to character data
    size_t length;   // Current number of characters (excluding null terminator)
    size_t capacity; // Total allocated space
} StringBuffer;

// Initialize a new StringBuffer with given capacity
StringBuffer *sb_init(size_t initial_capacity)
{
    if (initial_capacity == 0)
    {
        initial_capacity = 1; // Ensure minimum capacity of 1
    }

    // Allocating memory for string itself
    StringBuffer *sb = (StringBuffer *)malloc(sizeof(StringBuffer));

    // checking if malloc was executed successfully
    if (sb == NULL)
        return NULL;

    // Allocating memory for the character buffer
    sb->data = (char *)malloc(initial_capacity * sizeof(char));

    // Checking state of allocation again
    if (sb->data == NULL)
    {
        free(sb);
        return NULL;
    }

    // Initial string is empty
    sb->length = 0;

    // Storing initial capacity
    sb->capacity = initial_capacity;

    // Ending empty string with null character
    sb->data[0] = '\0';

    return sb;
}

// Append a string to the buffer, doubling capacity if necessary
StringBuffer *sb_append(StringBuffer *sb, const char *str)
{
    size_t str_len = strlen(str);
    size_t required = sb->length + str_len + 1; // Account for null terminator

    while (required > sb->capacity)
    {
        size_t new_capacity = sb->capacity * 2;

        char *new_data = realloc(sb->data, new_capacity * sizeof(char));
        if (new_data == NULL)
        {
            return NULL;
        }

        sb->data = new_data;
        sb->capacity = new_capacity;
    }

    // Copy new string to end of existing string
    strcpy(sb->data + sb->length, str);

    // Update length
    sb->length += str_len;

    return sb;
}

// Free all allocated memory for the StringBuffer
void sb_free(StringBuffer *sb)
{
    if (sb == NULL)
        return;
    free(sb->data); // Free the character buffer
    free(sb);       // Free the struct itself
}

// Display the contents, length, and capacity of the StringBuffer
void sb_print(StringBuffer *sb)
{
    if (sb == NULL)
    {
        printf("\n\nStringBuffer is NULL\n");
        return;
    }
    printf("\n========== StringBuffer Contents ==========\n");
    printf("Contents: %s\n", sb->data);
    printf("Length: %zu\n", sb->length);
    printf("Capacity: %zu\n", sb->capacity);
    printf("========================================== \n\n");
}

// Main driver function with interactive menu for StringBuffer operations
int main()
{
    StringBuffer *sb = sb_init(0); // Start with minimum capacity

    if (sb == NULL)
    {
        printf("Failed to initialize StringBuffer\n");
        return 1;
    }

    printf("Initial capacity of String: %zu\n\n", sb->capacity);

    int choice;
    char input[256];

    printf("========== StringBuffer Menu ==========\n");
    printf("1. Append\n");
    printf("2. Exit\n");
    printf("=======================================\n\n");

    while (1)
    {
        printf("Enter your choice (1-2): ");
        scanf("%d", &choice);
        getchar(); // Consume newline

        switch (choice)
        {
        case 1:
            printf("Enter string to append: ");
            fgets(input, sizeof(input), stdin);

            // Remove newline if present
            size_t len = strlen(input);
            if (len > 0 && input[len - 1] == '\n')
            {
                input[len - 1] = '\0';
            }

            if (sb_append(sb, input) == NULL)
            {
                printf("Failed to append string\n");
                sb_free(sb);
                return 1;
            }

            sb_print(sb);
            break;

        case 2:
            printf("Exiting...\n");
            sb_free(sb);
            return 0;

        default:
            printf("Invalid choice. Please enter 1 or 2.\n\n");
        }
    }

    return 0;
}
