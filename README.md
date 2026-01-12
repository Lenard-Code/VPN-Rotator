# VPN-Rotator

## Introduction

This project provides a Docker-based solution for creating a rotating VPN proxy. It allows you to route your traffic through a pool of VPN connections, with each new connection using a different VPN provider.

## Why?

When conducting **authorized** phishing engagements, it's crucial to have a solution that provides multiple source IPs to help obfuscate the true source of traffic and to further protect our infrastructure, such as an Evilginx server. This project was designed to meet that need by creating a simple, scalable, and effective way to rotate IP addresses. The more VPN providers added they better to further obfuscate Blue Teams ability to identify compromised accounts.

## Features

- **IP Rotation:** Automatically rotates your IP address for each new connection.
- **Multiple VPN Providers:** Supports the use of multiple VPN providers simultaneously.
- **Docker-based:** Easy to deploy and manage using Docker and Docker Compose.
- **Extensible:** Can be easily extended to support additional VPN providers.
- **Proxy Support:** Acts as a standard HTTP proxy that can be used with any application that supports proxies.

## How It Works

The system is composed of two main components:

- **`frontend-rotator`:** A Python-based service that listens for incoming connections and forwards them to one of the available `vpn-proxy` services. It uses a round-robin algorithm to distribute the connections among the VPNs.
- **`vpn-proxy`:** A service that establishes a connection to a VPN provider using OpenVPN and forwards traffic from the `frontend-rotator` through the VPN tunnel.

The `docker-compose.yml` file defines the services and their configurations. Each `vpn-proxy` service is configured with a specific VPN provider's OpenVPN configuration file and authentication credentials. The `frontend-rotator` service then routes traffic to these `vpn-proxy` services.

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1.  **Clone the repository:**
    ```
    git clone https://github.com/Lenard-Code/VPN-Rotator.git
    cd VPN-Rotator
    ```
2.  **Configure your VPN providers:**
    - Place your OpenVPN configuration files (`.ovpn`) in the `rotating-vpn-proxy/vpn-configs` directory.
    - For each VPN provider, create a corresponding directory in `rotating-vpn-proxy/vpn-auth` (e.g., `rotating-vpn-proxy/vpn-auth/nordvpn`).
    - Inside each provider's auth directory, create a `auth.txt` file containing the username and password for the VPN service, each on a new line.
3.  **Build and run the services:**
    ```
    docker-compose up --build
    ```

## Security Considerations

### Access Control Lists (ACLs)

It is critical to set up appropriate Access Control Lists (ACLs) to ensure that only authorized systems can access the proxy. Without ACLs, the proxy could be used by unauthorized parties. You should configure your firewall or network security groups to restrict access to the `frontend-rotator`'s port (9000 by default) to only trusted IP addresses.

### HTTPS Proxy

For an additional layer of security, you can incorporate an HTTPS proxy. This can be done by setting up a reverse proxy (e.g., Nginx, Caddy, or Traefik) in front of the `frontend-rotator`. The reverse proxy can handle SSL termination and provide more advanced filtering and logging capabilities.

## Usage

Once the services are up and running, you can use the VPN Rotator by configuring your application or web browser to use the following proxy settings:

-   **Proxy Type:** HTTP
-   **Host:** `localhost`
-   **Port:** `9000`

All traffic from your application will now be routed through the rotating VPN proxy.

## Future Features

Planned for future releases:

-   **Proxy Service Integration:** A functionality to utilize other proxy services, such as residential proxies, in addition to VPNs.
-   **Geolocation Matching:** Add logic to identify the victim's source IP and match it with a VPN/Proxy location. This will help to circumvent geolocation-based conditional access policies and reduce the risk of being assigned a suspicious IP address.
-   **Logging:** Add additional logging to keep track of which OVPN profile was used for specific users.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
