#!/usr/bin/env python3
"""
Утилита мониторинга сроков действия SSL/TLS сертификатов.
Проверяет список доменов, выводит отчет в JSON и возвращает код 1,
если до истечения любого сертификата осталось меньше порога дней.
"""

import datetime
import json
import socket
import ssl
import sys
from typing import Any

DOMAINS = [
    "google.com",
    "github.com",
]
WARN_DAYS_THRESHOLD = 14


def check_domain_ssl(hostname: str, port: int = 443, timeout: float = 5.0) -> dict[str, Any]:
    context = ssl.create_default_context()
    # Explicitly require TLS 1.2+ so legacy protocol versions are never negotiated
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    try:
        with (
            socket.create_connection((hostname, port), timeout=timeout) as sock,
            context.wrap_socket(sock, server_hostname=hostname) as ssock,
        ):
                cert = ssock.getpeercert()
                not_after_str = cert.get("notAfter")
                expiry_date = datetime.datetime.strptime(
                    not_after_str, "%b %d %H:%M:%S %Y %Z"
                ).replace(tzinfo=datetime.timezone.utc)
                now = datetime.datetime.now(datetime.timezone.utc)
                days_left = (expiry_date - now).days

                return {
                    "domain": hostname,
                    "status": "ok" if days_left >= WARN_DAYS_THRESHOLD else "expiring_soon",
                    "days_left": days_left,
                    "expires_at": expiry_date.isoformat(),
                }
    except Exception as exc:
        return {
            "domain": hostname,
            "status": "error",
            "days_left": -1,
            "error": str(exc),
        }


def main() -> int:
    results: list[dict[str, Any]] = []
    has_issues = False

    for domain in DOMAINS:
        info = check_domain_ssl(domain)
        results.append(info)
        if info["status"] != "ok":
            has_issues = True

    print(json.dumps({"checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "results": results}, indent=2))
    return 1 if has_issues else 0


if __name__ == "__main__":
    sys.exit(main())
