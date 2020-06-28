#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "MQTTClient.h"
#define ADDRESS     "ssl://iot.softwaremakeinindia.com:8883" // web pr 8083 nd mqtt 8883
#define CLIENTID    "kshitij"
#define TOPIC       "key/device"
#define PAYLOAD     "My message is successfully delivered by C program"
#define QOS         1
#define TIMEOUT     10000L
int main(int argc, char* argv[])
{
	// printf("Hellow\n");
    MQTTClient client;


    MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer; // connection options initializer
    MQTTClient_message pubmsg = MQTTClient_message_initializer; // publish message initializer 
	MQTTClient_SSLOptions ssl_opts = MQTTClient_SSLOptions_initializer; // ssl initializer 

    MQTTClient_deliveryToken token;
    int rc;


    int x = MQTTClient_create(&client, ADDRESS, CLIENTID,MQTTCLIENT_PERSISTENCE_NONE, NULL);
    // printf("%d\n", x);

//  ==============SSL initializer==================

    // ssl_opts.struct_version = 2;
    // ssl_opts.trustStore
    // ssl_opts.keyStore
    // ssl_opts.privateKey
    // ssl_opts.privateKeyPassword
    // ssl_opts.enabledCipherSuites
    // ssl_opts.enableServerCertAuth
    // ssl_opts.sslVersion = 3;
    // ssl_opts.verify
    // ssl_opts.CApath = "/etc/ssl/certs/";
    // ssl_opts.ssl_error_cb
    // ssl_opts.ssl_error_context
    
 // ================ COnnection Option assignments =======

    conn_opts.keepAliveInterval = 20;	
    conn_opts.cleansession = 1;
    conn_opts.username = "user";
    conn_opts.password = "pass";
    conn_opts.connectTimeout = 5;
	conn_opts.retryInterval = 3;
	conn_opts.ssl = &ssl_opts;


    if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS)
    {	
    	// printf("CLient ",)
        printf("Failed to connect, return code %d\n", rc);
        exit(EXIT_FAILURE);
    }
    pubmsg.payload = PAYLOAD;
    pubmsg.payloadlen = strlen(PAYLOAD);
    pubmsg.qos = QOS;
    pubmsg.retained = 0;
    MQTTClient_publishMessage(client, TOPIC, &pubmsg, &token);
    printf("Waiting for up to %d seconds for publication of %s\n"
            "on topic %s for client with ClientID: %s\n",
            (int)(TIMEOUT/1000), PAYLOAD, TOPIC, CLIENTID);
    rc = MQTTClient_waitForCompletion(client, token, TIMEOUT);
    printf("Message with delivery token %d delivered\n", token);
    MQTTClient_disconnect(client, 10000);
    MQTTClient_destroy(&client);
    return rc;
}