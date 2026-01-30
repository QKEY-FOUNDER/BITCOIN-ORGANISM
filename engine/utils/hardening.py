import warnings

def silence_known_warnings():
    """
    Hardening mínimo do organismo.
    Silencia warnings conhecidos que não afetam a semântica nem os dados.
    """

    # urllib3 + LibreSSL (macOS)
    try:
        from urllib3.exceptions import NotOpenSSLWarning
        warnings.filterwarnings(
            "ignore",
            category=NotOpenSSLWarning
        )
    except Exception:
        pass

    # Fallback por mensagem (casos genéricos)
    warnings.filterwarnings(
        "ignore",
        message=".*LibreSSL.*",
        category=Warning,
    )

    # pandas / numpy ruído comum
    warnings.filterwarnings(
        "ignore",
        category=FutureWarning,
    )

    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
    )
