---
name: security-review
description: OWASP Top 10 security checklist and .NET security best practices. Use when reviewing security-sensitive code or performing security audits.
---

# Security Review Checklist

## OWASP Top 10 (2021)

### A01: Broken Access Control
- [ ] Authorization checks on all protected endpoints
- [ ] CORS properly configured
- [ ] Direct object references validated
- [ ] Path traversal prevented

### A02: Cryptographic Failures
- [ ] Sensitive data encrypted at rest
- [ ] TLS 1.2+ enforced
- [ ] No deprecated algorithms (MD5, SHA1)
- [ ] No secrets hardcoded

### A03: Injection
- [ ] Parameterized queries for SQL
- [ ] Input validation on all user data
- [ ] Output encoding for XSS prevention

### A04: Insecure Design
- [ ] Defense in depth applied
- [ ] Fail-secure defaults
- [ ] Rate limiting on sensitive endpoints

### A05: Security Misconfiguration
- [ ] Debug modes disabled in production
- [ ] Error messages don't leak info
- [ ] Security headers configured

### A06: Vulnerable Components
- [ ] `dotnet list package --vulnerable` clean
- [ ] Dependencies up to date

### A07: Authentication Failures
- [ ] Strong password requirements
- [ ] Session management secure
- [ ] Account lockout implemented

### A08-A10
- [ ] CI/CD pipeline secure
- [ ] Security events logged
- [ ] URL validation for external calls

## .NET Specific

- [ ] Anti-forgery tokens for forms
- [ ] HTTPS redirection enabled
- [ ] Cookie settings (HttpOnly, Secure, SameSite)
- [ ] JWT validation complete

## Quick Scans

```bash
dotnet list package --vulnerable --include-transitive
grep -rn "password\s*=" --include="*.cs"
grep -rn "FromSqlRaw" --include="*.cs"
```

## CWE Quick Reference

| Issue | CWE | Severity |
|-------|-----|----------|
| SQL Injection | CWE-89 | Critical |
| XSS | CWE-79 | High |
| Hardcoded Credentials | CWE-798 | Critical |
| Missing Authorization | CWE-862 | Critical |

## Additional Resources

For detailed security checklists and remediation guidance, see [checklist.md](checklist.md).
