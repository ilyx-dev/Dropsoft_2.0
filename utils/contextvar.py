import contextvars

wallet_address_var = contextvars.ContextVar("wallet_address", default="unknown")