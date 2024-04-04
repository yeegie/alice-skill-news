from dataclasses import dataclass


@dataclass
class SmtpParams:
    tls: bool
    host: str
    port: int
    user: str
    password: str