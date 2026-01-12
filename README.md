# VPN Rotator

This project provides a Docker-based solution for creating a rotating VPN proxy. It allows you to route traffic through a pool of VPN connections, with each new connection using a different VPN. This is useful for tasks that require a high degree of anonymity or for bypassing IP-based rate limiting.

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

To get started with the VPN Rotator, you will need to have Docker and Docker Compose installed on your system.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/Lenard-Code/VPN-Rotator.git
   cd VPN-Rotator
   ```

2. **Configure your VPN providers:**
   - Place your OpenVPN configuration files (`.ovpn`) in the `rotating-vpn-proxy/vpn-configs` directory.
   - For each VPN provider, create a corresponding directory in `rotating-vpn-proxy/vpn-auth` (e.g., `rotating-vpn-proxy/vpn-auth/nordvpn`).
   - Inside each provider's auth directory, create a `auth.txt` file containing the username and password for the VPN service, each on a new line.

3. **Build and run the services:**
   ```
   docker-compose up --build
   ```

## Configuration

The main configuration file for the project is `docker-compose.yml`. This file defines the services, networks, and volumes used by the VPN Rotator.

### Adding a New VPN Provider

To add a new VPN provider, you will need to:

1. **Add a new service** to the `docker-compose.yml` file for the new VPN provider. This service should be based on the `vpn-proxy` image and should be configured with the appropriate OpenVPN configuration file and authentication credentials.
2. **Add the new service** to the `PROXIES` list in `rotating-vpn-proxy/frontend-rotator/rotator.py`.

## Usage

Once the services are up and running, you can use the VPN Rotator by configuring your application or web browser to use the following proxy settings:

- **Proxy Type:** HTTP
- **Host:** `localhost`
- **Port:** `9000`

All traffic from your application will now be routed through the rotating VPN proxy.

## Extensibility

The VPN Rotator is designed to be extensible. You can easily add support for additional VPN providers or customize the behavior of the `frontend-rotator` service to meet your specific needs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
