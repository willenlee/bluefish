#include "ocslog.h"
#include "bin_sem.h"
#include <sys/stat.h>
#include <errno.h>

void __attribute__ ((constructor)) mutex_int(void);
void __attribute__ ((destructor)) mutex_end(void);

/* semaphore pointer */
sem_t *mutex;

static int binary_sem_signal(void);
static int binary_sem_open(void);
static int binary_sem_wait(int permit_recurse);

void mutex_int(void){
	if(!mutex)
		binary_sem_open();
}

void mutex_end(void){
	if(mutex)
		sem_close(mutex);
}

/******************************************************************************
*   Function 		binary_sem_open
*   Purpose: 		opens/creates connection to named semaphore.
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
 int binary_sem_open(void){

	if(!mutex){
		mode_t org_mask = umask(0);
			mutex = sem_open(SEM_NAME, O_CREAT, (S_IRWXU | S_IRWXG | S_IRWXO), 1);
		umask(org_mask);
		if(mutex == SEM_FAILED){
			log_fnc_err(FAILURE, "unable to create/attach semaphore. NULL_OBJECT\n");
			if(!mutex)
				sem_close(mutex);

			return FAILURE;
		};
	}

	return SUCCESS;
}

/******************************************************************************
*   Function 		binary_sem_wait
*   Purpose: 		decrements (locks) the semaphore
*   In parameters: 	permit_recurse allows the function re-enter if semaphore
*   				owner dies while waiting
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
static int binary_sem_wait(int permit_recurse){

	if(!mutex){
		log_fnc_err(FAILURE, "NULL mutex variable in binary_sem_wait\n");
		return FAILURE;
	}

	int response;

	struct timespec time;

	clock_gettime(CLOCK_REALTIME, &time);
	time.tv_sec += TIMEOUT_SEC;

	response = sem_timedwait(mutex, &time);
	if(response != 0){
		log_fnc_err(response, "binary_sem_wait - semaphore timed wait\n");

		if(errno == EOWNERDEAD){
			log_fnc_err(response, "semaphore owner died\n");
			/* put sem into know state  */
			response = binary_sem_signal();
			if(response == 0 && permit_recurse > 0){
				return binary_sem_wait(0);
			}
		}

		if(errno == EINVAL && permit_recurse > 0){
			log_fnc_err(response, "semaphore sem_close() while waiting error: %d\n", EINVAL);
			if(binary_sem_open() == SUCCESS){
				binary_sem_wait(0);
			}
		}
	}

	return response;
}

/******************************************************************************
*   Function 		binary_sem_signal
*   Purpose: 		increments (releases) the semaphore
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
static int binary_sem_signal(void){
	int response = 0;

	if(!mutex){
		log_fnc_err(FAILURE, "binary_sem_signal - semaphore not initialized\n");
		return FAILURE;
	}

	response = sem_post(mutex);

	if(response !=0){
		log_fnc_err(errno, "binary_sem_signal - semaphore sem_post: %d\n", response);
	}

	return response;
}

/******************************************************************************
*   Function 		semex_get
*   Purpose: 		wrapper to create an lock/decrements the semaphore
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int semex_get(void){
	if(binary_sem_open() == SUCCESS)
		// wait semaphore with error recursion
		return binary_sem_wait(1);
	else
		return FAILURE;

}

/******************************************************************************
*   Function 		semtex_release
*   Purpose: 		wrapper to post/release the semaphore
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int semex_release(void){
	return binary_sem_signal();
}

/******************************************************************************
*   Function 		semex_close
*   Purpose: 		wrapper to close semaphore
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes: if the semaphore pointer is null, it will return SUCCESS
*******************************************************************************/
int semex__close(void){
	if(!mutex)
		return SUCCESS;
	else
		return sem_close(mutex);
}
