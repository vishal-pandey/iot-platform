// Client side C/C++ program to demonstrate Socket programming 
#include <stdio.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <netinet/in.h>
#include <unistd.h> 
#include <string.h> 
#include <netdb.h>
#include<json-c/json.h>


int main(int argc, char const *argv[]) 
{ 
    // ==================Getting the IP================================================

    // struct hostent *host_info;
    // struct  in_addr *address;
    // host_info = gethostbyname("iot.softwaremakeinindia.com");
    // address = (struct in_addr *)(host_info->h_addr);
    // printf("%s",inet_ntoa(*address));
    // enum CONSTEXPR { MAX_REQUEST_LEN = 1024};
    // char request[MAX_REQUEST_LEN];
    // char request_template[] = "GET / HTTP/1.1\r\nHost: %s\r\n\r\n";
    // char *hostname = "example.com";

    // int request_len = snprintf(request, MAX_REQUEST_LEN, request_template, hostname);
    // printf("%d\n", request_len);

    // ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    FILE  *fp;
    char buffer[1024];
    struct json_object *parsed_json;
    struct json_object *name;
    struct json_object *age;
    struct json_object *friends;
    struct json_object *friend;

    size_t n_friends;
    size_t i;

    fp = fopen("json.json","r");
    fread(buffer,1024,1,fp);
    fclose(fp);
    parsed_json = json_tokener_parse(buffer);   
    json_object_object_get_ex(parsed_json,"name",&name);

    printf("%s\n",json_object_get_string(name));
    return 0; 
} 
