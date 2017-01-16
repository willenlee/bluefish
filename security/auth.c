/*
 * auth.c

 *
 *  Created on: Jul 7, 2016
 *      Author: admin_user
 */

#define _GNU_SOURCE

#include <crypt.h>
#include "ocslog.h"
#include "auth.h"
#include "bin_sem.h"

static int delete_entry(const char *filename, const char *username);
static int shadow_append(struct spwd *sp);
static void generate_salt(char *salt);

/******************************************************************************
*   Function Name: 	app_specific_error
*   Purpose: 		convert application error into char pointer
*   In parameters: 	err, error offset
*   Return value:  	pointer to error or default error
*   Comments/Notes:
*******************************************************************************/
char * app_specific_error(int err){

	if(err < MAX_ERROR_SUPPORT && err > 0)
		return (char *)app_error_str[err];
	else
		return (char *)app_error_str[DEFAULT_ERR_IDX];

}

/******************************************************************************
*   Function Name: 	salt_size
*   Purpose: 		gets the size of the salt used for passwd encryption.
*   In parameters: 	salt, input array consisting of string to search
*   Return value:  	failed if something failed, salt location otherwise
*   Comments/Notes: supports salt up to maximum salt for this library
*******************************************************************************/
int salt_size(char *salt) {
	int i = 3;
	for (; i <= SALT_SIZE; i++)
		if (salt[i] == '$') {
			return i;
		}
	return -1;
}

static void current_day_count(int *dcnt){
	time_t date_time;

	/* get current time */
	date_time = time(NULL);

	date_time = (((date_time /60)/60)/24);

	*dcnt = (int)date_time;
}

/******************************************************************************
*   Function Name: 	ocs_group_id
*   Purpose: 		check if target group name matches ocs group name
*   In parameters: 	groupname, name of target ocs group
*	Out parameters: g_id, Id of group
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes: does array lookup on group_names
*******************************************************************************/
int ocs_group_id(const char *groupname, int *g_id){
	if(groupname == NULL){
		log_fnc_err(FAILURE, "%s: ocs_group_id: null group name.\n", app_specific_error(INVALID_PARAM));
		return INVALID_PARAM;
	}

	int idx = 0;
	for(; idx < MAX_GROUP_SUPPORT; idx++){
		if(strcmp(groupname, group_names[idx]) == SUCCESS){
			*g_id = ocs_group_ids[idx];
			return SUCCESS;
		}
	}

	return UNKNOWN_ERROR;
}

/******************************************************************************
*   Function Name: 	ocs_group_member
*   Purpose: 		check if user is a member of a given ocs group
*   In parameters: 	groupname, name of target ocs group
*					username, name of user to check
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes: ocs groups do not use linux groups in tradition sense,
*  					it just enums users with primary group id matching predefined
*  					ocs group id
*******************************************************************************/
int ocs_group_member(const char *groupname, const char *username){

	if(username == NULL || groupname == NULL){
		log_fnc_err(FAILURE, "%s: invalid input group or user name\n", app_specific_error(INVALID_PARAM));
		return INVALID_PARAM;
	}

	int g_id = 0;
	int *group_ptr = &g_id;
	if(ocs_group_id(groupname, group_ptr) != 0){
		log_fnc_err(FAILURE, "%s: non-ocs group group_member.\n", app_specific_error(UNSUPPORTED));
		return UNSUPPORTED;
	}

	struct passwd pw;
	struct passwd *result;

	char buffer[256];
	size_t length = sizeof(buffer);

	if(getpwnam_r(username, &pw, buffer, length, &result) == SUCCESS){
		if(result != NULL){
			if((pw.pw_gid == g_id) || 
			(g_id == OCS_ADMIN_ID && pw.pw_gid == 0))
			return SUCCESS;
		}
		else{
			log_fnc_err(FAILURE, "%s: group_member() getpwnam_r returned null.\n", app_specific_error(NULL_OBJECT));
		  return NULL_OBJECT;
		}
	}

	return FAILURE;
}

/******************************************************************************
*   Function Name: 	group_members
*   Purpose: 		returns all members in a given group
*   In parameters: 	groupname, name of target group
* 	Out parameters:	length, pointer to size of output char array
*					members, pointer to user name char array
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int ocs_group_members(const char *groupname, const int *length, char *members){

	int response = 0;

	if(groupname == NULL || members == NULL){
		log_fnc_err(FAILURE, "%s: invalid input group name\n", app_specific_error(INVALID_PARAM));
		return INVALID_PARAM;
	}

	int gid = 0;
	int *group_ptr = &gid;
	if(ocs_group_id(groupname, group_ptr) != 0){
		log_fnc_err(FAILURE, "%s: non-ocs group group_member.\n", app_specific_error(UNSUPPORTED));
		return UNSUPPORTED;
	}

	FILE *fhandle;

	fhandle = fopen(USER_FILE, "r");

	if(!fhandle){
		log_fnc_err(FAILURE, "%s: read and append open passwd failed\n", app_specific_error(FILE_IO_ERROR));
		return FILE_IO_ERROR;
	}

	int idx = 0;
	int count = 0;
	struct passwd *pwd;

	while((pwd = fgetpwent(fhandle))){
	  if ((pwd->pw_gid == gid) ||
			/* root is ocs admin by default */
			(pwd->pw_uid == 0 && gid == OCS_ADMIN_ID)){

		  idx += (strlen(pwd->pw_name) +1);
		  if(idx > *length){
			  log_fnc_err(FAILURE, "%s: input members buffer too small for user list\n", app_specific_error(INPUT_BUFF_SIZE));
			  response = INPUT_BUFF_SIZE;
			  break;
		  }

		  if(count != 0)
			  strncat(members,", ", sizeof(char));

		  strncat(members, pwd->pw_name, USERNAME_MAX_LEN);

		  count++;

	  }
	}

	fclose(fhandle);

	return response;

}

int ocs_change_role(const char *username, const char *groupname){

	if(username == NULL || groupname == NULL){
		log_fnc_err(FAILURE, "%s: invalid input group or user name\n", app_specific_error(INVALID_PARAM));
		return INVALID_PARAM;
	}

	FILE *fhandle;
	int response = 0;
	int g_id = 0;
	int *group_ptr = &g_id;
	if(ocs_group_id(groupname, group_ptr) != 0){
		log_fnc_err(FAILURE, "%s: non-ocs group group_member. \n", app_specific_error(UNSUPPORTED));
		return UNSUPPORTED;
	}

	struct passwd pw;
	struct passwd *result;

	int sem_held = 0;

	char buffer[256];
	size_t length = sizeof(buffer);

	if((response = getpwnam_r(username, &pw, buffer, length, &result)) == SUCCESS){
		if(result != NULL){

			if(pw.pw_uid == 0 && g_id == OCS_ADMIN_ID){
				return response;
			}

			if(pw.pw_uid == 0 && g_id != OCS_ADMIN_ID){
				log_fnc_err(FAILURE, "%s: root can only be ocs admin\n", app_specific_error(INVALID_OPERATION));
				return INVALID_OPERATION;
			}

			if(pw.pw_gid == g_id){
				return response;
			}
			else{
				pw.pw_gid = g_id;

				/* semex_get and hold so u_id isn't stolen by concurrent add_user */
				if((response = semex_get()) != SUCCESS){
					log_fnc_err(FAILURE, "%s: unable to obtain semex_get error: %d",app_specific_error(FUNCTION_ERR), response);
					goto end_clean;
				}

				sem_held = 1;

				/* remove user record from passwd only */
				if ((response = delete_entry(USER_FILE, username)) != 0){
					log_fnc_err(FAILURE, "%s: unable to remove user from: %s\n", app_specific_error(response), USER_FILE);
					goto end_clean;
				}

				/* add updated user to passwd only */
				fhandle = fopen(USER_FILE, "a+");

				if(!fhandle){
					log_fnc_err(FAILURE, "%s: read and append open passwd failed\n", app_specific_error(FILE_IO_ERROR));
					response = FILE_IO_ERROR;
					goto end_clean;
				}

				if((response = putpwent(&pw, fhandle)) != 0){
					log_fnc_err(FAILURE, "%s: unable to add user to passwd: %s error %d\n", app_specific_error(FUNCTION_ERR), username, response);
				}

				fflush(fhandle);

				fclose(fhandle);
			}
		}
		else{
			log_fnc_err(FAILURE, "%s: null error getting getpwnam_r in ocs_change_role.\n", app_specific_error(FUNCTION_ERR));
			response = FUNCTION_ERR;
		}
	}

end_clean:
	if(sem_held > 0)
 		if(semex_release() != SUCCESS){
 			log_fnc_err(FAILURE, "ocs_change_role - semex_release failed\n");
 		}

	return response;
}

/******************************************************************************
*   Function Name: 	check_root
*   Purpose: 		checks if uid is zero
*   Return value:  	FAILED user not verified as root, SUCCESS user is root
*   Comments/Notes:
*******************************************************************************/
int check_root(){
	if(geteuid() == 0)
		return 0;
	else
		return 1;
}

/******************************************************************************
*   Function Name: 	get_username_from_id
*   Purpose: 		returns user name from user id
*   In parameters: 	user_id, id of target group
*					lenght, size of input char array
* 	Out parematers:	username, pointer to username char array
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int get_username_from_id(const uid_t user_id, const size_t length, char *username){

	if(username == NULL){
		log_fnc_err(FAILURE, "%s: provide user name parameter\n", app_specific_error(INVALID_PARAM));
		return INVALID_PARAM;
	}

	if(user_id == 0){
		strcpy(username, "root");
		return 0;
	}

	int response;

	struct passwd pw;
	struct passwd *result;

	char buffer[256];
	size_t len = sizeof(buffer);
	if((response = getpwuid_r(user_id, &pw, buffer, len, &result)) == SUCCESS){
		if(result != NULL){
				strncpy(username, pw.pw_name, length);
				return response;
		}
		else{
			log_fnc_err(FAILURE, "%s: getpwuid_r null object user id: %d", app_specific_error(NULL_OBJECT), user_id);
			return NULL_OBJECT;
		}
	}

	return FAILURE;
}

/******************************************************************************
*   Function Name: 	get_groupname_from_id
*   Purpose: 		returns group name from group id
*   In parameters: 	group_id, id of target group
*					length, size of input char array
* 	Out parameters:	groupname, pointer to group name array
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int get_groupname_from_id(const gid_t group_id, const size_t length, char *groupname){
	int response;

	struct group grp;
	struct group *result;

	if(groupname != NULL){
		char buffer[256];
		size_t len = sizeof(buffer);

		if((response = getgrgid_r(group_id, &grp, buffer, len, &result)) == SUCCESS){
			if(result != NULL){
					strncpy(groupname, grp.gr_name, length);
					return response;
			}
			else{
				log_fnc_err(FAILURE, "%s: getgrgid_r null object user id: %d", app_specific_error(NULL_OBJECT), group_id);
				return NULL_OBJECT;
			}
		}
	}

	return FAILURE;
}

/******************************************************************************
*   Function Name: 	get_groupid_from_name
*   Purpose: 		returns group id from group name
*   In parameters: 	username, pointer to groupname array
* 	Out parameters:	id, pointer to group id
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int get_groupid_from_name(const char *groupname, gid_t *id){
	int response;

	if(!groupname){
		log_fnc_err(FAILURE, "%s: groupname name parameter\n", app_specific_error(INVALID_PARAM));
		return INVALID_PARAM;
	}

	struct group grp;
	struct group *result;

	char buffer[256];
	size_t length = sizeof(buffer);
	if((response = getgrnam_r(groupname, &grp, buffer, length, &result)) == SUCCESS){
		if(result != NULL){
				*id = grp.gr_gid;
				return 0;
		}
		else{
			log_fnc_err(FAILURE, "%s: getgrnam_r null object user id: %s", app_specific_error(NULL_OBJECT), groupname);
			return NULL_OBJECT;
		}
	}

	return FAILURE;
}

/******************************************************************************
*   Function Name: 	get_current_username
*   Purpose: 		returns user name of calling process
*   In parameters: 	username, pointer to username array
*					length, size of username pointer
* 	Out parameters:	username, user name of calling process
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int get_current_username(char *username, size_t length){
		uid_t user_id = geteuid();
		return get_username_from_id(user_id, length, username);
}

/******************************************************************************
*   Function Name: 	get_user_id
*   Purpose: 		gets user id from user name
*   In parameters: 	username, input target username
* 	Out parameters:	userid, the pw_uid for the user
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int get_userid_from_name(const char *username, uid_t *userid){

	int response;

	if(username == NULL){
		log_fnc_err(FAILURE, "%s: username name parameter\n", app_specific_error(INVALID_PARAM));
		return INVALID_PARAM;
	}

	struct passwd pw;
	struct passwd *result;

	char buffer[256];
	size_t length = sizeof(buffer);

	if((response = getpwnam_r(username, &pw, buffer, length, &result)) == SUCCESS){
		if(result != NULL){
			*userid = pw.pw_uid;
			return response;
		}
		else{
			return NULL_OBJECT;
		}
	}
	else{
		log_fnc_err(FAILURE, "%s: getpwnam_r error: %s %d\n", app_specific_error(FUNCTION_ERR), username, response);
		return FUNCTION_ERR;
	}

	return FAILURE;

}

/******************************************************************************
*   Function 		add_user
*   Purpose: 		adds a user to the passwd, shadow and group file.
*   In parameters: 	populated spwd structure
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int add_user(const char *username, const char *groupname, const char *password){

	FILE *fhandle;
	int response;
	int sem_held = 0;

	if(username == NULL || password == NULL){
		log_fnc_err(FAILURE, "%s: provide valid username and password\n", app_specific_error(INVALID_PARAM));
		return INVALID_PARAM;
	}

	uid_t userid;
	if(get_userid_from_name(username, &userid) == SUCCESS){
		log_fnc_err(FAILURE, "%s: user already exists: %s Id: %d", app_specific_error(INVALID_OPERATION), username, userid);
		return INVALID_OPERATION;
	}

	int name_length = 0;
	unsigned char letter = 0x20;

	char* temp_user = (char *)username;
	/* check user name 0-9, A-Z, a-z) */
	while(*++temp_user){
		letter = *temp_user;

		if((letter >= 0x41 && letter <= 0x5A) ||
		   (letter >= 0x30 && letter <= 0x39) ||
		   (letter >= 0x61 && letter <= 0x7A)){
		}
		else{
			log_fnc_err(FAILURE, "%s: illegal character in username\n", app_specific_error(INVALID_PARAM));
			return INVALID_PARAM;
		}

		name_length++;
	}

	if(name_length < USERNAME_MIN_LEN ||
	   name_length > USERNAME_MAX_LEN){
		log_fnc_err(FAILURE, "%s: illegal user name length: %s min length: %d max length: %d\n",
				app_specific_error(INVALID_PARAM),
				username, USERNAME_MIN_LEN, USERNAME_MAX_LEN);
		return INVALID_PARAM;
	}

	gid_t groupid = 0;
	if((response = get_groupid_from_name(groupname, &groupid)) != SUCCESS){
		log_fnc_err(FAILURE, "%s: error: %d invalid group name: %s\n", app_specific_error(FUNCTION_ERR), response, groupname);
		return FUNCTION_ERR;
	}

	char homedir[USERNAME_MAX_LEN + 7];
	snprintf(homedir, sizeof(homedir), "/home/%s", username);

	struct passwd pw;

	pw.pw_name = (char *)username;
	pw.pw_passwd = (char*)"x"; /*x indicates etc/shadow */
	pw.pw_gid = groupid;
	pw.pw_gecos = "ocscli account";
	pw.pw_shell = USER_SHELL;
	pw.pw_dir = homedir;
	pw.pw_uid = MIN_ID+1;

	fhandle = fopen(USER_FILE, "a+");

	if(!fhandle){
		log_fnc_err(FAILURE, "%s: read and append open passwd failed\n", app_specific_error(FILE_IO_ERROR));
		return FILE_IO_ERROR;
	}

	/* lock the pwd before getting the pid, to prevent dups*/
	if((response = semex_get()) != SUCCESS){
		log_fnc_err(FAILURE, "%s: unable to obtain semex_get error: %d", app_specific_error(FUNCTION_ERR), response);
		goto end_clean;
	}

	sem_held = 1;

	struct passwd *pwd;
	/* get avail uid */
	while ((pwd = fgetpwent(fhandle))) {
		if ((pwd->pw_uid >= pw.pw_uid) && (pwd->pw_uid < MAX_ID)) {
			pw.pw_uid = ++pwd->pw_uid;
		}
	}

	if((response = putpwent(&pw, fhandle)) != SUCCESS){
		log_fnc_err(FAILURE, "%s: error: %d, unable to add user to passwd: %s\n",
				app_specific_error(FUNCTION_ERR), response, username);
	}

	if(fflush(fhandle) != SUCCESS && fclose(fhandle) != SUCCESS){
		log_fnc_err(FAILURE, "%s: error: %d, unable to flush and close passwd: %s\n",
				app_specific_error(FUNCTION_ERR), response, username);
	}

	/* update shadow */
   if(response == SUCCESS) {

	   struct spwd sp;
	   memset(&sp, 0, sizeof(sp));

	   int daycnt = 0;
	   current_day_count(&daycnt);

	   /* generate a salt */
	   char salt[40];
	   char *saltptr = salt;
	   generate_salt(saltptr);

	   struct crypt_data data;
	   data.initialized = 0;

	   sp.sp_namp = pw.pw_name;
	   sp.sp_pwdp = (char*)crypt_r((const char*)password, saltptr, &data);
	   sp.sp_lstchg = daycnt;
	   sp.sp_min = 0;
	   sp.sp_max = 99999;
	   sp.sp_warn = 7;
	   sp.sp_inact = -1;
	   sp.sp_expire = -1;
	   sp.sp_flag = -1;

	   response = shadow_append(&sp);

	   if (response == SUCCESS) {
		   if (mkdir(pw.pw_dir, 0755) == 0) {
			   chown(pw.pw_dir, pw.pw_uid, pw.pw_gid);
			   chmod(pw.pw_dir, 02755);
		   }
	   }

   }

 end_clean:
 	 if(sem_held > 0)
 		if(semex_release() != SUCCESS){
 			log_fnc_err(FAILURE, "add_user - semex_release failed\n");
 		}

   return response;

}

/******************************************************************************
*   Function Name: 	remove_user
*   Purpose: 		removes user from passwd, shodow, group file.
*   In parameters: 	username, target user to remove
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int remove_user(const char *username){

	int response = 0;
	int sem_held = 0;

	if((response = semex_get()) != SUCCESS){
		log_fnc_err(FAILURE, "%s: unable to obtain semex_get error: %d", app_specific_error(FUNCTION_ERR), response);
		goto end_clean;
	}

	sem_held = 1;

	if ((response = delete_entry(USER_FILE, username)) != 0){
		/* error reported in delete entry, just log info if needed */
		printf("unable to remove user from: %s\n", USER_FILE);
		goto end_clean;
	}

	if ((response = delete_entry(SHADOW_FILE, username)) != 0){
		printf("unable to remove user from: %s\n", SHADOW_FILE);
		goto end_clean;
	}

	// remove the users home directory, but don't complain if it's not there.
	char homedir[USERNAME_MAX_LEN + 7];
	snprintf(homedir, sizeof(homedir), "/home/%s", username);
	remove(homedir);

end_clean:
 if(sem_held > 0)
	if(semex_release() != SUCCESS){
		log_fnc_err(FAILURE, "remove_user - semex_release failed\n");
	}

	return response;
}

/******************************************************************************
*   Function Name: 	update_password
*   Purpose: 		updates user password in shadow file
*   In parameters: 	username, name of target user to update password
*					password, new unencrypted password
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int update_password(const char *username, const char *password){

	int response = 0;
	int sem_held = 0;

	char buffer[256];
	struct spwd spw;
	struct spwd *result;
	getspnam_r(username, &spw, buffer, sizeof(buffer), &result);

	if (!result) {
		log_fnc_err(FAILURE, "%s: unable to locate user pwd\n", app_specific_error(INVALID_PARAM));
		return INVALID_PARAM;
	}

	char salt[40];
	char *saltptr = salt;
	generate_salt(saltptr);

	int daycnt = 0;
	current_day_count(&daycnt);

	struct crypt_data data;
	data.initialized = 0;

	result->sp_pwdp = (char*)crypt_r((const char*)password, saltptr, &data);
	result->sp_lstchg = daycnt;
	result->sp_inact = -1;
	result->sp_expire = -1;

	/* lckpwdf isn't thread safe, using semaphore instead, and hold so uid isn't stolen by concurrent add_user */
	if((response = semex_get()) != SUCCESS){
		log_fnc_err(FAILURE, "%s: unable to obtain semex_get error: %d", app_specific_error(FUNCTION_ERR), response);
		goto end_clean;
	}



	sem_held = 1;

	if ((response = delete_entry(SHADOW_FILE, username)) != 0){
		printf("unable to remove user from: %s\n", SHADOW_FILE);
		goto end_clean;
	}

	response = shadow_append(result);

end_clean:
	if(sem_held > 0)
		if(semex_release() != SUCCESS){
			log_fnc_err(FAILURE, "remove_user - semex_release failed\n");
		}

	return response;
}

/******************************************************************************
*   Function Name: 	verify_username_permission
*   Purpose: 		returns the user primary group for permissions
*   In parameters: 	username, name of user to verify
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int verify_username_permission(const char *username, int *group_id){

	int response;

	if(!username){
		log_fnc_err(FAILURE, "%s: user name cannot be null\n", app_specific_error(INVALID_PARAM));
		return INVALID_PARAM;
	}

	struct passwd pw;
	struct passwd *result;

	char buffer[256];
	size_t length = sizeof(buffer);

	if((response = getpwnam_r(username, &pw, buffer, length, &result)) == SUCCESS){
		if(result != NULL){

			/* root is ocs admin by default */
			if (pw.pw_uid == 0) {
				*group_id = OCS_ADMIN_ID;
				return response;
			}

			int idx = 0;
			for(; idx < MAX_GROUP_SUPPORT; idx++){
				if(pw.pw_gid == ocs_group_ids[idx]){
					*group_id = pw.pw_gid;
					return response;
				}
			}

			log_fnc_err(FAILURE, "%s: user: %s not ocs group member\n",
					app_specific_error(UNSUPPORTED), username);
			response = FAILURE;

		}
		else{
			log_fnc_err(FAILURE, "%s: ocs_verify_permission getpwnam_r(%s) returned null\n",
					app_specific_error(NULL_OBJECT), username);
			response = NULL_OBJECT;
		}
	}
	else{
		log_fnc_err(FAILURE, "%s: ocs_verify_permission getpwnam_r(%s) returned: %d\n",
				app_specific_error(FUNCTION_ERR),  username, response);
		return response;
	}

	return response;

}

/******************************************************************************
*   Function Name: 	verify_caller_permission
*   Purpose: 		returns the calling process primary group for permissions
*   In parameters: 	username, name of user to verify
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int verify_caller_permission(int *group_id){

	int response;

	struct passwd pw;
	struct passwd *result;

	char buffer[256];
	size_t length = sizeof(buffer);

	uid_t user_id;
	user_id = getuid();

	if((response = getpwuid_r(user_id, &pw, buffer, length, &result)) == SUCCESS){
		if(result != NULL){

			/* root is ocs admin by default */
			if (pw.pw_uid == 0) {
				*group_id = OCS_ADMIN_ID;
				return response;
			}

			int idx = 0;
			for(; idx < MAX_GROUP_SUPPORT; idx++){
				if(pw.pw_gid == ocs_group_ids[idx]){
					*group_id = pw.pw_gid;
					return response;
				}
			}

			log_fnc_err(FAILURE, "%s: user id: %d not ocs group member\n",
					app_specific_error(UNSUPPORTED), user_id);
			response = FAILURE;

		}
		else{
			log_fnc_err(FAILURE, "%s: ocs_verify_permission getpwuid_r(%d) returned null\n",
					app_specific_error(NULL_OBJECT), user_id);
			response = NULL_OBJECT;
		}
	}
	else{
		log_fnc_err(FAILURE, "%s: ocs_verify_permission getpwuid_r(%d) returned: %d\n",
				app_specific_error(FUNCTION_ERR),  user_id, response);
		return response;
	}

	return response;

}

/******************************************************************************
*   Function Name: 	verify_authentication
*   Purpose: 		authenticates user login
*   In parameters: 	username and password to verify
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
int verify_authentication(const char *username, const char *password){
	char buffer[256];
	struct spwd spw;
	struct spwd *result;

	/* salt size and termination */
	char salt[SALT_SIZE +1];
	char *saltprt;
	saltprt = salt;

	getspnam_r(username, &spw, buffer, sizeof(buffer), &result);

	if(!result){
		log_fnc_err(FAILURE, "%s: unable to locate user pwd\n", app_specific_error(NULL_OBJECT));
		return NULL_OBJECT;
	}

	int salt_length = 0;
	salt_length = salt_size(result->sp_pwdp);

	if(salt_length < 0 || salt_length > SALT_SIZE){
		salt_length = SALT_SIZE;
	}

	/* just get the salt from pw string */
	strncpy(saltprt, result->sp_pwdp, salt_length);
	salt[SALT_SIZE] = '\0';

	struct crypt_data data;
	data.initialized = 0;

	if(strcmp(crypt_r(password, saltprt, &data), result->sp_pwdp) == SUCCESS){
		return SUCCESS;
	}

	return FAILURE;
}

/******************************************************************************
*   Function 		Name: shadow_append
*   Purpose: 		appends an entry to the shodow file.
*   In parameters: 	populated spwd structure
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
static int shadow_append(struct spwd *sp){

	int response = 0;
	FILE *fhandle;

	if (!sp) {
		log_fnc_err(FAILURE, "%s: password encryption failed\n", app_specific_error(INVALID_PARAM));
		return INVALID_PARAM;
	}

	fhandle = fopen(SHADOW_FILE, "a+");

	if (!fhandle) {
		log_fnc_err(FAILURE, "%s: unable to open shadow\n", app_specific_error(FILE_IO_ERROR));
		return FILE_IO_ERROR;
	}

	if ((response = putspent(sp, fhandle)) != SUCCESS) {
		log_fnc_err(FAILURE, "%s: failed to add user pw to shadow: %d\n", app_specific_error(FILE_IO_ERROR), response);
	}

	fflush(fhandle);

	fclose(fhandle);

	return response;
}

/******************************************************************************
*   Function Name:	delete_entry
*   Purpose: 		Removes an entry from a file, /etc/passwd, /etc/shadow,
*					etc/group
*   In parameters: 	filename, name of the target file.
*				   	username, user name of line to remove/locate.
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes: i don't know of another way to do this,
*					delete a line, read it into a buffer, remove the line
*					and write back.
*******************************************************************************/
static int delete_entry(const char *filename, const char *username) {

	int response = 1;
	long length = 0;

	char *buffer;
	FILE *handle;

	handle = fopen(filename, "r");
	if(!handle){
		log_fnc_err(FAILURE, "%s: file open error: %s\n", app_specific_error(FILE_IO_ERROR), filename);
		response = FILE_IO_ERROR;
		goto end_clean;
	}

	if(fseek(handle, 0L, SEEK_END) == SUCCESS){
		if((length = ftell(handle)) == -1){
			log_fnc_err(FAILURE, "%s: unable to determine size of file: %s\n",
					app_specific_error(FILE_IO_ERROR), filename);
			response = -1;
			goto end_clean;
		}
	}

	if(length > 0 && length < MAX_FILE_BUFFER)
		buffer = (char *)malloc((length + 1) * sizeof(char));

	if(!buffer){
		log_fnc_err(FAILURE, "%s: unable to allocate buffer for file: %s\n",
				app_specific_error(INVALID_OPERATION),  filename);
		response = INVALID_OPERATION;
		goto end_clean;
	}

	if(fseek(handle, 0L, SEEK_SET) != SUCCESS){
		log_fnc_err(FAILURE, "%s: io error seeking file: %s\n",
				app_specific_error(FILE_IO_ERROR),  filename);
		response = FILE_IO_ERROR;
		goto end_clean;
	}


	fread(buffer, length, sizeof(char), handle);
	if(ferror(handle) != 0){
		log_fnc_err(FAILURE, "%s: io error reading file: %s\n",
				app_specific_error(FILE_IO_ERROR),  filename);
		response = FILE_IO_ERROR;
		goto end_clean;
	}

	fclose(handle);

	// append : to name name
	char srchname[USERNAME_MAX_LEN +2];
	snprintf(srchname, USERNAME_MAX_LEN, "\n%s:", username);

	char *skip_start;
	char *skip_end;
	int start_idx, end_idx;

	if(strncmp(buffer, &srchname[1], strlen(srchname) -1) == SUCCESS)
		skip_start = strstr(buffer, &srchname[1]);
	else
		skip_start = strstr(buffer, srchname);


	if(!skip_start){
		log_fnc_err(FAILURE, "%s: unable to find name entry: %s\n",
				app_specific_error(FILE_IO_ERROR), username);
		response = INVALID_OPERATION;
		goto end_clean;
	}

	skip_start++;
	skip_end = strchr(skip_start, '\n');

	if(!skip_end){
		log_fnc_err(FAILURE, "%s: unable to find name termination: %s\n",
				app_specific_error(INVALID_OPERATION), username);
		response = INVALID_OPERATION;
		goto end_clean;
	}

	/* pointer subtraction to get index */
	start_idx = (skip_start - buffer);
	end_idx = (skip_end - buffer) +1;

	handle = fopen(filename, "w");
	if(!handle){
		log_fnc_err(FAILURE, "%s: io error write open file: %s\n",
				app_specific_error(FILE_IO_ERROR), filename);
		response = FILE_IO_ERROR;
		goto end_clean;
	}

	/* write-back until start of user name index */
	fwrite(buffer, start_idx, sizeof(char), handle);
	/* write-back after user name index */
	fwrite(&buffer[end_idx], (length - end_idx), sizeof(char), handle);

	fflush(handle);

	/* flag clean exit */
	response = 0;

end_clean:
	if(!buffer)
		free(buffer);

	if(!handle)
		fclose(handle);

	return response;

}

/******************************************************************************
*   Function Name: 	generate_salt
*   Purpose: 		creates the salt for password encryption.
*   In parameters: 	salt, input array which is modified by the void
*   Out parameters: salt, modified contents of input array
*   Return value:  	FAILED if something failed, SUCCESS otherwise
*   Comments/Notes:
*******************************************************************************/
static void generate_salt(char *salt){

	char state_buffer[RANDOM_BUFF];
	struct random_data data;
	memset(&data, 0, sizeof(struct random_data));

	int seed = (int)(getpid() + clock());

	initstate_r(seed, state_buffer, RANDOM_BUFF, &data);

	strcpy(salt,"$6$"); /* SHA-512 */
	int result;

	while(1){
		random_r(&data, &result);
		strcat(salt, l64a(result));

		if(strlen(salt) >= SALT_SIZE){
			salt[SALT_SIZE] = '\0';
			break;
		}
	}
}
