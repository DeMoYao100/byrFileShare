#include <stdio.h>
#include <string.h>

#define BUFFER_SIZE 256

void safe_function(const char *input) {
    char buffer[BUFFER_SIZE];
    // 使用动态计算的长度
    int length = strlen(input);
    // 有空间才放
    if (length < BUFFER_SIZE) {
        memcpy(buffer, input, length);
        buffer[length] = '\0'; 
    } else {
        printf("Input is too long!\n");
    }
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        // 调用函数并传入用户输入
        safe_function(argv[1]);
    } else {
        printf("Please provide an input string.\n");
    }
    return 0;
}
