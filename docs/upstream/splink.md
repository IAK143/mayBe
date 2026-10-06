# splink Research Report

## Original problem
Splink: Fast probabilistic entity resolution at scale solves key operational bottlenecks in its domain by providing a dedicated research baseline for efficient processing.

## Core algorithm
Algorithmic implementation based on Splink: Fast probabilistic entity resolution at scale. Designed for optimal theoretical complexity and domain performance.

## Input
Structured / Unstructured domain specific inputs (text, vectors, sparse indices, or graphs).

## Output
Transformed intelligence representations (retrieved candidates, clusters, change points, resolved entities, or embeddings).

## Data representation
In-memory structures, sparse matrices, or local disk indexes according to upstream specifications.

## Complexity characteristics
Time and space complexity optimized for scale as described in original publication.

## Memory characteristics
Bounded or configurable according to memory budgets.

## Dependencies
Python / C++ / Rust standard runtime libraries specified in project manifest.

## License
MIT

## What we reuse
Algorithmic principles, design patterns, and evaluation benchmarks.

## What we rewrite
Internal contracts and local reference adapters in clean Python 3.11 with Pydantic v2.

## What we wrap
External library bindings via adapter protocols in dedicated subsystem directories.

## What we must NOT copy
Incompatible licensed source code directly into core codebase (process/adapter boundaries enforced).

## Integration boundary
intelligence/entity_resolution adapter protocol.

## Tests
Unit tests, fixture integration tests, and benchmark contract tests.

## Benchmark
Automated JSON metrics measuring latency, memory, precision, and recall.

## Citation


## Original authors
MOJ Analytical Services

## Original paper
Splink: Fast probabilistic entity resolution at scale

## Repository structure
Upstream repository preserved unmodified under .

## Limitations
Hardware and system constraints evaluated per upstream documentation.
