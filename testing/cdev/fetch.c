#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include<json-c/json.h>




struct string {
  char *ptr;
  size_t len;
};

void init_string(struct string *s) {
  s->len = 0;
  s->ptr = malloc(s->len+1);
  if (s->ptr == NULL) {
    fprintf(stderr, "malloc() failed\n");
    exit(EXIT_FAILURE);
  }
  s->ptr[0] = '\0';
}

size_t writefunc(void *ptr, size_t size, size_t nmemb, struct string *s)
{
  size_t new_len = s->len + size*nmemb;
  s->ptr = realloc(s->ptr, new_len+1);
  if (s->ptr == NULL) {
    fprintf(stderr, "realloc() failed\n");
    exit(EXIT_FAILURE);
  }
  memcpy(s->ptr+s->len, ptr, size*nmemb);
  s->ptr[new_len] = '\0';
  s->len = new_len;

  return size*nmemb;
}


 
int init(char *key)
{
	CURL *curl;
	CURLcode res;

    struct string s;
    init_string(&s);

	 
	curl_global_init(CURL_GLOBAL_DEFAULT);
	 
	curl = curl_easy_init();
	if(curl) 
	{
	    curl_easy_setopt(curl, CURLOPT_URL, "https://iot.softwaremakeinindia.com/iot/");


	    // printf("%s\n", key);
	    char *prepend = "key=";
	    char * finalKey = (char *) malloc(1 + strlen(key)+ strlen(prepend) );
        strcpy(finalKey, prepend);
        strcat(finalKey, key);
        // printf("Key = %s\n", finalKey );


	    // curl_easy_setopt(curl, CURLOPT_POSTFIELDS, );
	    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, finalKey);
		#ifdef SKIP_PEER_VERIFICATION
	    	curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
		#endif
	 
		#ifdef SKIP_HOSTNAME_VERIFICATION
	    	curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
		#endif
		 
		    /* Perform the request, res will get the return code */ 

   	    curl_easy_setopt (curl, CURLOPT_VERBOSE, 0L); //0 disable messages

	    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writefunc);
	    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &s);

	    res = curl_easy_perform(curl);

		    /* Check for errors */ 
	    if(res != CURLE_OK)
	    {
		    fprintf(stderr, "curl_easy_perform() failed: %s\n",curl_easy_strerror(res));
	    }

		struct json_object *parsed_json;
    	parsed_json = json_tokener_parse(s.ptr);  

    	struct json_object *username;
    	struct json_object *password;
    	struct json_object *error;


    	json_object_object_get_ex(parsed_json,"username",&username);
    	json_object_object_get_ex(parsed_json,"password",&password);
    	json_object_object_get_ex(parsed_json,"error",&error);

    	// printf("Username = %s\n",json_object_get_string(username));
    	// printf("Password = %s\n",json_object_get_string(password));
    	// printf("Error %s\n",json_object_get_string(error));


    	// const char *err = json_object_get_string(error);

    	if(json_object_get_string(error)){
    		if(strcmp(json_object_get_string(error),"Error Wrong Credentials"))
    		{
				printf("Please enter Correcte key \n");
				return 0;
			}	
    	}
		

    	
    	const char *pass = json_object_get_string(password);
    	const char *user = json_object_get_string(username);



    	// printf("Username  = %s\n",user );
    	// printf("Password  = %s\n",pass );




    	free(s.ptr);
	    curl_easy_cleanup(curl);
	}
	 
	curl_global_cleanup();
	return 1;
}


int main()
{
	if(init("7ec3b90e-672a-4502-bfc5-d83e8c4ff7d")){
		printf("Success\n");
	}

	// init("ec3b90e-672a-4502-bfc5-d83e8c4ff7da");

	return 0;
}
