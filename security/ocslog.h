#ifndef __ocslog_h
#define __ocslog_h

#include <string.h>
#include <stdio.h>

#define LOG_ENTRY_SIZE 		256 // 256 B
#define UNKNOWN_ERROR	-1
#define FAILURE			-2
#define SUCCESS			0

typedef enum LOG_LEVEL
{
	SILENT_LEVEL = 0,
	INFO_LEVEL = 1,
	ERROR_LEVEL = 2,
}loglevel_t;

void log_out(char*, ...); 
void log_info(char*, ...); 
void log_err(int, char*,...);
void log_init(loglevel_t);

/* 
 * LOG_ERR macro
 * Note: Macro is required for getting error location information 
 */
#define log_fnc_err(err, message, ...) do {	    \
	printf("log_fnc_err message:%s ", message); \
	} while(0)                                  \

#endif //__ocslog_h
