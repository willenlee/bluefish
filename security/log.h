#include <stdio.h>
#include <string.h>
#include <errno.h>

#define LOG_FNC_ERR(err) if((err) != 0) { fprintf(stderr, "ERROR: %s %s :%d Error-->%d %s ", __FILE__, __FUNCTION__, __LINE__ ,errno,strerror(errno));}

#define LOG_ERR(err, msg, ...) do { fprintf(stderr, "ERROR: " msg ": [%s]\n", ##__VA_ARGS__, strerror(err));} while(0)

#define LOG_INFO(msg, ...) do {fprintf(stdout, msg, ##__VA_ARGS__);} while(0)

#define lprintf(msg, ...) do {fprintf(stdout, msg, ##__VA_ARGS__);} while(0)


#define UNKNOWN_ERROR	-1
#define FAILURE			1
#define SUCCESS			0

