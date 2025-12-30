# Security Checklist Reference

Load this file when reviewing security-sensitive code or performing security audits.

---

## OWASP Top 10 (2021) Checklist

### A01: Broken Access Control
- [ ] Authorization checks on all protected endpoints
- [ ] CORS properly configured (no wildcard in production)
- [ ] Direct object references validated
- [ ] Path traversal prevented
- [ ] Principle of least privilege applied

### A02: Cryptographic Failures
- [ ] Sensitive data encrypted at rest
- [ ] TLS 1.2+ enforced for data in transit
- [ ] No deprecated algorithms (MD5, SHA1)
- [ ] No secrets hardcoded in source code
- [ ] Passwords hashed with bcrypt/Argon2

### A03: Injection
- [ ] Parameterized queries for all SQL
- [ ] Input validation on all user data
- [ ] Output encoding for XSS prevention
- [ ] Command injection prevented

### A04: Insecure Design
- [ ] Defense in depth applied
- [ ] Fail-secure defaults
- [ ] Rate limiting on sensitive endpoints

### A05: Security Misconfiguration
- [ ] Debug modes disabled in production
- [ ] Error messages don't leak info
- [ ] Security headers configured

### A06: Vulnerable Components
- [ ] Dependencies up to date
- [ ] `dotnet list package --vulnerable` clean

### A07: Authentication Failures
- [ ] Strong password requirements
- [ ] Session management secure
- [ ] Account lockout implemented

### A08: Integrity Failures
- [ ] CI/CD pipeline secure
- [ ] Serialization safe

### A09: Logging Failures
- [ ] Security events logged
- [ ] No sensitive data in logs

### A10: SSRF
- [ ] URL validation present
- [ ] Internal network protected

---

## Scanning Commands

```bash
# Check for vulnerable packages
dotnet list package --vulnerable --include-transitive

# Search for hardcoded secrets
grep -rn "password\s*=" --include="*.cs"
grep -rn "apikey\s*=" --include="*.cs"
```

---

## CWE References

| Issue | CWE | Severity |
|-------|-----|----------|
| SQL Injection | CWE-89 | Critical |
| XSS | CWE-79 | High |
| CSRF | CWE-352 | High |
| Hardcoded Credentials | CWE-798 | Critical |
| Missing Authorization | CWE-862 | Critical |
