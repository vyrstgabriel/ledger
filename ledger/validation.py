from __future__ import annotations


def parse_tickers(raw: str) -> list[str]:
    tickers = [ticker.strip().upper() for ticker in raw.split(",") if ticker.strip()]
    return list(dict.fromkeys(tickers))


def parse_weights(raw: str, tickers: list[str]) -> dict[str, float]:
    if not raw.strip():
        return equal_weights(tickers)

    weights: dict[str, float] = {}
    for item in raw.split(","):
        if not item.strip():
            continue
        if ":" not in item:
            raise ValueError("Weights must use TICKER:WEIGHT pairs, like AAPL:40, MSFT:60.")

        ticker, value = item.split(":", 1)
        ticker = ticker.strip().upper()
        try:
            weights[ticker] = float(value.strip()) / 100
        except ValueError as exc:
            raise ValueError(f"Weight for {ticker} must be a number.") from exc

    missing = [ticker for ticker in tickers if ticker not in weights]
    extra = [ticker for ticker in weights if ticker not in tickers]
    if missing:
        raise ValueError(f"Missing weights for: {', '.join(missing)}.")
    if extra:
        raise ValueError(f"Weight provided for tickers not in portfolio: {', '.join(extra)}.")

    total = sum(weights.values())
    if abs(total - 1) > 0.001:
        raise ValueError(f"Weights must add up to 100%. Current total is {total:.1%}.")

    return weights


def equal_weights(tickers: list[str]) -> dict[str, float]:
    if not tickers:
        raise ValueError("At least one ticker is required.")

    weight = 1 / len(tickers)
    return {ticker: weight for ticker in tickers}

