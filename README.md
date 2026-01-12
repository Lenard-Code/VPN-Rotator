# VPN-Rotator

## Introduction

This repository provides a flexible and scalable solution for routing traffic through multiple VPNs. It uses Docker to create a proxy that rotates requests across a series of VPN connections. This can be useful for a variety of tasks, including web scraping, bypassing geographic restrictions, and enhancing online privacy.

## Why We Created This

When conducting authorized Red Team activities, we need a solution to provide multiple source IPs to help obfuscate the true source and to further protect our Evilginx server. This project was designed to solve that problem by providing a simple, yet powerful, way to rotate through multiple VPN connections.

## Features

- **IP Rotation:** Automatically rotate your IP address with each new connection.
- **Multiple VPN Providers:** Easily configure and use multiple VPN providers.
- **Docker-Based:** The entire system is containerized with Docker, making it easy to deploy and manage.
- **Extensible:** The project is designed to be easily extended with additional VPN providers or custom functionality.

## How It Works

The system is composed of two main services: the `frontend-rotator` and the `vpn-proxy`.

- The `frontend-rotator` is a Python-based service that listens for incoming connections and forwards them to one of the `vpn-proxy` services.
- The `vpn-proxy` services are Docker containers that each run a VPN client and a proxy server.

When a request is made to the `frontend-rotator`, it selects one of the `vpn-proxy` services and forwards the request to it. The `vpn-proxy` service then forwards the request to the destination, through the VPN connection.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Configuration

1. **Clone the repository:**
   ```
   git clone https://github.com/Lenard-Code/VPN-Rotator.git
   ```
2. **Add your VPN configurations:**
   - Add your OpenVPN configuration files to the `rotating-vpn-proxy/vpn-configs` directory.
   - Add your VPN authentication files to the `rotating-vpn-proxy/vpn-auth` directory. Each VPN provider should have its own directory, with an `auth.txt` file containing the username and password on separate lines.
3. **Configure the `docker-compose.yml` file:**
   - The `docker-compose.yml` file in the `rotating-vpn-proxy` directory is pre-configured to use four VPN providers: NordVPN, PIA, HMA, and ExpressVPN. You can add, remove, or modify these services as needed.
   - For each VPN service, you will need to specify the VPN configuration file and the authentication directory.

### Launching the System

Once you have configured the system, you can launch it with the following command:

```
docker-compose up -d
```

## Security Considerations

### Access Control Lists (ACLs)

It is critical that you configure appropriate Access Control Lists (ACLs) to protect your VPN-Rotator instance. You should only allow traffic from trusted sources to access the `frontend-rotator` service. If you are using this to protect an Evilginx Pro server, you should configure your ACLs to only allow traffic from the Evilginx Pro server.

### HTTPS Proxy

To further protect your Evilginx Pro server, you should incorporate an HTTPS proxy between the Evilginx Pro server and the `frontend-rotator`. This will encrypt the traffic between the two servers, making it more difficult for an attacker to intercept and analyze the traffic.

## Usage

To use the VPN-Rotator, you can configure your applications or browser to use the `frontend-rotator` as a proxy. The `frontend-rotator` listens on port `9000` by default.

## Extensibility

The system is designed to be easily extended with additional VPN providers. To add a new VPN provider, you will need to:

1. Add the OpenVPN configuration file to the `rotating-vpn-proxy/vpn-configs` directory.
2. Add the authentication file to the `rotating-vpn-proxy/vpn-auth` directory.
3. Add a new service to the `docker-compose.yml` file in the `rotating-vpn-proxy` directory.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
