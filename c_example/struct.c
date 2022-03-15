# include <stddef.h>
# include <stdint.h>
// inet_pton
# include <sys/types.h>
# include <sys/socket.h>
# include <arpa/inet.h>
# include <netdb.h>


// struct sockaddr
// {
//     /* data */
//     unsigned short sa_family; // AF_INET; AF_INET6;
//     // 14 bytes of protocol address
//     char sa_data[14];
// };


// struct in_addr 
// {
//     uint32_t s_addr;
// };


// struct in6_addr
// {
//     unsigned char s_6_addr[16];
// };


// struct sockaddr_in
// {
//     short int sin_family;
//     unsigned int sin_port;
//     struct in_addr sin_addr;
//     unsigned char sin_zero[8]

// };


// struct sockaddr_in6
// {
//     uint16_t sin6_family;
//     uint16_t sin6_port;
//     uint32_t sin6_flowinfo;
//     struct in6_addr sin6_addr;
//     uint32_t sin6_scope_id;
// };



// struct addrinfo
// {
//     int ai_flags;
//     int ai_family; // AF_INET; AF_INET6; AF_UNSPEC: force to use IPv4 or IPv6 or UNSPEC
//     int ai_socktype; // SOCK_STREAM; SOCK_DGRAM
//     int ai_protocol; // use 0 or any: TCP or UDP
//     size_t ai_addrlen ; // size of ai_addr in bytes
//     struct sockaddr *ai_addr;
//     char *ai_canonname;
//     struct addrinfo *ai_next; // linked list, next node
// };

# define AF_INET

char ip4[INET_ADDRSTRLEN];
struct sockaddr_in sa;

inet_ntop(AF_INET, &(sa.sin_addr), ip4, INET_ADDRSTRLEN);
printf("The IPv4 address is: %s\n", ip4)
