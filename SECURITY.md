# PyHwa Security Policy

## Disclaimer of Liability
PyHwa is provided "as is," and we, the PyHwa development team, are **not responsible for any misuse** or unintended applications of this software. Users of PyHwa must ensure they comply with their local laws, and they are fully responsible for any consequences arising from the improper use or misconfiguration of this tool.

## Intended Use: Local Network
**PyHwa is primarily designed for local network use**. Its current architecture and security protocols are optimized for environments where the server and client are operating within a trusted internal network. While PyHwa is highly customizable and offers many powerful features, it is important to understand that the default configuration **is not intended for access across multiple networks or for public internet exposure**.

### Public Access Warning
**At this time**, PyHwa should not be accessible from other networks or the public internet. We strongly recommend **limiting access to PyHwa** to devices within your local network or VPN-protected environments. Exposing PyHwa to the internet without adequate protections or network segmentation may lead to potential security risks, such as:
- Unauthenticated access.
- Vulnerability to brute-force attacks or other unauthorized access attempts.
- Exposure of sensitive data through unsecured connections.

**Internet Access**: By default, PyHwa accesses certain websites (such as MangaDex or AniList) to retrieve and update metadata. This access is necessary for syncing and updating this information, but it only occurs once unless a manual update is requested. If desired, this functionality can be **disabled**. If a site becomes unreliable or insecure, it is important to **immediately report the issue** by opening an issue to inform the project's creators and collaborators.

For a secure implementation in a public-facing network or over the internet, **additional security mechanisms are required**. However, the current version of PyHwa **does not yet support full public network deployment** without custom configurations.

## Future Updates for Public Access
We are actively working on expanding PyHwa's features to support **secure internet access**. This will include:
- Better authentication and authorization systems.
- Hardened configurations for external deployment.

These features are in development, and **users are encouraged to wait for future releases** if public network access is a requirement.

## Security Best Practices for PyHwa
While using PyHwa, we recommend the following practices to maintain security:

1. **Local Network Use Only**: Ensure that PyHwa is only accessible from trusted devices within your internal network.
2. **Password Hashing**: Always use hashed passwords (e.g., bcrypt) for admin accounts and never store plain text passwords in configuration files.
3. **Secure Configuration Files**: Restrict access to sensitive configuration files (e.g., `pyhwa.ini`) by setting appropriate file permissions (`chmod 600` on Linux).
4. **Firewall Protection**: Use a firewall to block unwanted external access to the PyHwa server.
5. **VPN Usage**: If you need remote access to your PyHwa instance, consider using a VPN to secure the connection between external users and your local network.
6. **Regular Updates**: Stay up to date with the latest releases of PyHwa, as new security features and patches will be provided regularly.

### Additional Notes:
- **Web Interface Password Handling**: If you use the web interface, the passwords you enter will be automatically placed into the corresponding configuration files and **automatically hashed** for security.
- **Documentation Reference**: If you have any doubts or questions, make sure to refer to the official documentation.
- **Be Cautious with Modifications**: If you're unsure about what you're modifying, it's better not to proceed. Instead, open an issue and ask a question to get clarification.

## Reporting Security Issues
If you discover any security issues or vulnerabilities in PyHwa, please report them to the development team immediately by contacting us through the official repository or by email at `security@pyhwa.dev`. Your feedback is crucial to maintaining the safety and integrity of this project.

---

## Summary
PyHwa **is not designed for public internet deployment** in its current form, and users should restrict its use to **local networks**. It may connect to websites for metadata updates, but this can be disabled if necessary. We disclaim any responsibility for misuse or unintended application of PyHwa, and future updates will include enhanced security features for internet-facing setups.
