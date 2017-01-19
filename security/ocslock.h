/*
 * Module: ocslock.h
 *
 * Description: Exports public functions defined in ocslock.c
 *
 * Copyright (C) 2016 Microsoft Corp
 *
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *
 *    Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 *    Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the
 *    distribution.
 *
 *    Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 *  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 *  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 *  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 *  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 *  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
*/

#ifndef SEMLOCK_H_
#define SEMLOCK_H_

/* 
 * Enum with all ocslocks
 * NOTE: When adding new lock, 
 * (i) add it both the OCSLOCK_NAME enum list, 
 * (ii) increment NUM_OCSLOCKS and,
 * (iii) add to OCSLOCK_STRING  
 */
typedef enum OCSLOCK_NAME
{ 
	PRU_CHARDEV = 0,
	PRU_SEQNUM = 1,	
	TELEMETRY_DAEMON = 2, 	
	OCSGPIOACCESS = 3,		
	I2C0_CHARDEV = 4,
	I2C1_CHARDEV = 5,
	PRU_PERSIST = 6,
	OCSLOG_SHM = 7,
	OCSLOG_DAEMON = 8,
	NVDIMM_DAEMON = 9,
	USR_ACCNT = 10,
	NUM_OCSLOCKS = 11,
}ocslock_t;

static const char *OCSLOCK_STRING[NUM_OCSLOCKS] = {
    "ocsprudev", 
    "ocspruseqno", 
    "ocstelemetrydaemon", 
    "ocsgpioaccess", 
    "ocsi2c0dev", 
    "ocsi2c1dev", 
    "ocsprupersist",
    "ocslogshm",
    "ocslogdaemon",
    "ocsnvdimmdaemon",
	"ocsuseraccount",
};

/* Extern functions */
extern int ocs_lock(ocslock_t);
extern int ocs_unlock(ocslock_t);
extern int ocslock_init(ocslock_t);
extern void config_mutex_rec(int(*rec_fn)());

extern int ocs_condwait(ocslock_t);
extern int ocs_condsignal(ocslock_t);


#endif // SEMLOCK_H_
