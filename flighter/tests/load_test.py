import argparse
import asyncio
import math
import random
import time
from dataclasses import dataclass
from datetime import date

import httpx


@dataclass(slots=True, frozen=True)
class RequestResult:
    latency_ms: float
    failed: bool


@dataclass(slots=True)
class LoadConfig:
    base_url: str
    origin: str
    destination: str
    departure_date: date
    mode: str
    clients: int
    rate: float
    warmup: float
    duration: float


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0

    ordered = sorted(values)
    index = math.ceil(p * len(ordered)) - 1

    return ordered[max(0, index)]


def print_stats(
    title: str,
    results: list[RequestResult],
    duration: float,
) -> None:
    latencies = [result.latency_ms for result in results]
    errors = sum(result.failed for result in results)
    total = len(results)

    print(f"\n{title}")
    print(f"Requests: {total}")
    print(f"Requests/sec: {total / duration:.2f}")
    print(f"p50: {percentile(latencies, 0.50):.2f} ms")
    print(f"p95: {percentile(latencies, 0.95):.2f} ms")
    print(f"p99: {percentile(latencies, 0.99):.2f} ms")
    print(f"Max: {max(latencies, default=0.0):.2f} ms")
    print(f"Errors: {errors / total * 100:.2f}%" if total else "Errors: 0.00%")


async def request(
    client: httpx.AsyncClient,
    url: str,
    params: dict[str, str] | None,
    results: list[RequestResult],
    measurement_start: float,
    measurement_end: float,
) -> None:
    loop = asyncio.get_running_loop()
    started_at = loop.time()
    failed = False

    try:
        response = await client.get(url, params=params)
        failed = not response.is_success
    except httpx.HTTPError:
        failed = True

    finished_at = loop.time()

    if measurement_start <= started_at < measurement_end:
        results.append(
            RequestResult(
                latency_ms=(finished_at - started_at) * 1000,
                failed=failed,
            )
        )


async def closed_load(
    client: httpx.AsyncClient,
    config: LoadConfig,
    measurement_start: float,
    measurement_end: float,
    results: list[RequestResult],
) -> None:
    url = f"{config.base_url.rstrip('/')}/api/v1/flights/search"
    params = {
        "origin": config.origin,
        "destination": config.destination,
        "date": config.departure_date.isoformat(),
    }

    async def worker() -> None:
        while asyncio.get_running_loop().time() < measurement_end:
            await request(
                client,
                url,
                params,
                results,
                measurement_start,
                measurement_end,
            )

    await asyncio.gather(
        *(worker() for _ in range(config.clients))
    )


async def open_load(
    client: httpx.AsyncClient,
    config: LoadConfig,
    measurement_start: float,
    measurement_end: float,
    results: list[RequestResult],
) -> None:
    url = f"{config.base_url.rstrip('/')}/api/v1/flights/search"
    params = {
        "origin": config.origin,
        "destination": config.destination,
        "date": config.departure_date.isoformat(),
    }

    tasks: list[asyncio.Task[None]] = []
    loop = asyncio.get_running_loop()
    next_request_at = loop.time()

    while next_request_at < measurement_end:
        delay = next_request_at - loop.time()

        if delay > 0:
            await asyncio.sleep(delay)

        if loop.time() >= measurement_end:
            break

        tasks.append(
            asyncio.create_task(
                request(
                    client,
                    url,
                    params,
                    results,
                    measurement_start,
                    measurement_end,
                )
            )
        )

        next_request_at += random.expovariate(config.rate)

    await asyncio.gather(*tasks)


async def monitor_health(
    client: httpx.AsyncClient,
    base_url: str,
    measurement_start: float,
    measurement_end: float,
    results: list[RequestResult],
) -> None:
    url = f"{base_url.rstrip('/')}/api/v1/health"
    tasks: list[asyncio.Task[None]] = []

    loop = asyncio.get_running_loop()
    next_request_at = loop.time()
    interval = 0.1

    while next_request_at < measurement_end:
        delay = next_request_at - loop.time()

        if delay > 0:
            await asyncio.sleep(delay)

        if loop.time() >= measurement_end:
            break

        tasks.append(
            asyncio.create_task(
                request(
                    client,
                    url,
                    None,
                    results,
                    measurement_start,
                    measurement_end,
                )
            )
        )

        next_request_at += interval

    await asyncio.gather(*tasks)


async def run(config: LoadConfig) -> None:
    timeout = httpx.Timeout(30.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        loop = asyncio.get_running_loop()

        started_at = loop.time()
        measurement_start = started_at + config.warmup
        measurement_end = measurement_start + config.duration

        search_results: list[RequestResult] = []
        health_results: list[RequestResult] = []

        print(f"Mode: {config.mode}")
        print(f"Warmup: {config.warmup}s")
        print(f"Measurement: {config.duration}s")

        if config.mode == "closed":
            load_task = asyncio.create_task(
                closed_load(
                    client,
                    config,
                    measurement_start,
                    measurement_end,
                    search_results,
                )
            )
        else:
            load_task = asyncio.create_task(
                open_load(
                    client,
                    config,
                    measurement_start,
                    measurement_end,
                    search_results,
                )
            )

        health_task = asyncio.create_task(
            monitor_health(
                client,
                config.base_url,
                measurement_start,
                measurement_end,
                health_results,
            )
        )

        await asyncio.gather(load_task, health_task)

        print_stats("SEARCH", search_results, config.duration)
        print_stats("HEALTH", health_results, config.duration)


def parse_args() -> LoadConfig:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
    )
    parser.add_argument(
        "--origin",
        default="SVO",
    )
    parser.add_argument(
        "--destination",
        default="KZH",
    )
    parser.add_argument(
        "--date",
        type=date.fromisoformat,
        default=date.today(),
    )
    parser.add_argument(
        "--mode",
        choices=["closed", "open"],
        default="closed",
    )
    parser.add_argument(
        "--clients",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--rate",
        type=float,
        default=5.0,
    )
    parser.add_argument(
        "--warmup",
        type=float,
        default=10.0,
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=60.0,
    )

    args = parser.parse_args()

    if args.clients < 1:
        parser.error("--clients must be positive")

    if args.rate <= 0:
        parser.error("--rate must be positive")

    if args.warmup < 0 or args.duration <= 0:
        parser.error("--warmup must be non-negative and --duration must be positive")

    return LoadConfig(
        base_url=args.base_url,
        origin=args.origin,
        destination=args.destination,
        departure_date=args.date,
        mode=args.mode,
        clients=args.clients,
        rate=args.rate,
        warmup=args.warmup,
        duration=args.duration,
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(run(parse_args()))
    print(f"\nTotal elapsed: {time.perf_counter() - start:.2f}s")