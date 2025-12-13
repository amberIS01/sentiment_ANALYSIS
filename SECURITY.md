# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by emailing sahilsingh8300@gmail.com.

Please include:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if any)

## Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution**: Depending on severity

## Security Best Practices

When using this project:

1. **Input Validation**: Always validate user inputs before processing
2. **Dependencies**: Keep dependencies updated
3. **Configuration**: Don't commit sensitive configuration files
4. **Logging**: Avoid logging sensitive information

## Known Security Considerations

- The chatbot processes user input - ensure proper sanitization
- Exported conversations may contain sensitive data
- Log files should be properly secured
