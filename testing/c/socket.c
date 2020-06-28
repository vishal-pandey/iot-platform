#include <arpa/inet.h>
#include <assert.h>
#include <netdb.h> /* getprotobyname */
#include <netinet/in.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main() {
    char buffer[BUFSIZ];
    enum CONSTEXPR { MAX_REQUEST_LEN = 1024};
    char request[MAX_REQUEST_LEN];
    char request_template[] = "GET / HTTP/1.1\r\nHost: %s\r\n\r\n";
    struct protoent *protoent;
    char *hostname = "example.com";
    int request_len;
    int socket_file_descriptor;
    ssize_t nbytes_total, nbytes_last;
    // struct hostent *hostent;
    struct sockaddr_in sockaddr_in;
    unsigned short server_port = 80;

    request_len = snprintf(request, MAX_REQUEST_LEN, request_template, hostname);
    if (request_len >= MAX_REQUEST_LEN) {
        fprintf(stderr, "request length large: %d\n", request_len);
        exit(EXIT_FAILURE);
    }

    /* Build the socket. */
    protoent = getprotobyname("tcp");
    if (protoent == NULL) {
        perror("getprotobyname");
        exit(EXIT_FAILURE);
    }

    socket_file_descriptor = socket(AF_INET, SOCK_STREAM, protoent->p_proto);
    if (socket_file_descriptor == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    /* Build the address. */
    struct hostent *host_info;
    struct  in_addr *address;
    host_info = gethostbyname("iot.softwaremakeinindia.com");
    address = (struct in_addr *)(host_info->h_addr);
    printf("%s",inet_ntoa(*address));





    sockaddr_in.sin_addr.s_addr = *address;
    sockaddr_in.sin_family = AF_INET;
    sockaddr_in.sin_port = htons(server_port);

    /* Actually connect. */
    if (connect(socket_file_descriptor, (struct sockaddr*)&sockaddr_in, sizeof(sockaddr_in)) == -1) {
        perror("connect");
        exit(EXIT_FAILURE);
    }

    /* Send HTTP request. */
    nbytes_total = 0;
    while (nbytes_total < request_len) {
        nbytes_last = write(socket_file_descriptor, request + nbytes_total, request_len - nbytes_total);
        if (nbytes_last == -1) {
            perror("write");
            exit(EXIT_FAILURE);
        }
        nbytes_total += nbytes_last;
    }

    /* Read the response. */
    fprintf(stderr, "debug: before first read\n");
    while ((nbytes_total = read(socket_file_descriptor, buffer, BUFSIZ)) > 0) {
        fprintf(stderr, "debug: after a read\n");
        write(STDOUT_FILENO, buffer, nbytes_total);
    }
    fprintf(stderr, "debug: after last read\n");
    if (nbytes_total == -1) {
        perror("read");
        exit(EXIT_FAILURE);
    }

    close(socket_file_descriptor);
    exit(EXIT_SUCCESS);
}