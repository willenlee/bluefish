/*
 * bin_sem.h
 *
 *  Created on: Sep 13, 2016
 *      Author: admin_user
 */

#include <semaphore.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <time.h>

#define SEM_NAME  			"OCS_ACCNT_SEM_LOCK"

#define TIMEOUT_SEC		  3

int semex_get(void);
int semex_release(void);
int semex_close(void);
