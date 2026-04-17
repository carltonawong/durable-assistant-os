# Durable Assistant OS

A useful personal assistant first.

Durable Assistant OS (DAOS) is an agent-agnostic operating harness and shared memory system for durable human-agent collaboration.

It is designed to help a real person over time — not just answer prompts well in isolated sessions.

The core idea is simple:
- start from lived reality, not abstract system design
- help with real priorities, active projects, and constraints
- preserve useful continuity without turning the system into a bloated maze of memory rules
- distill only the reusable pieces into a public framework

This repository is intentionally narrow in scope. It is not trying to be a universal theory of agents. It is an attempt to capture the smallest set of practices that make a personal AI assistant meaningfully more useful, trustworthy, and durable.

## Thesis

Most assistant systems drift in one of two directions:
- they stay stateless and repeatedly lose context
- they become overengineered and burden the user with setup, maintenance, and abstraction

DAOS aims for the middle path:
- enough structure to preserve continuity
- enough restraint to stay practical
- enough behavioral clarity to build trust

Read the core docs here:
- [`docs/thesis.md`](docs/thesis.md)
- [`docs/memory.md`](docs/memory.md)

## What DAOS is trying to solve

A durable assistant should be able to:
- understand what matters right now
- track a small number of active projects and constraints
- behave consistently enough to earn trust
- improve without forcing the user to constantly restate context
- stay grounded in real files, real systems, and real work

## Design principles

### 1. Useful before elegant
If a design choice does not materially improve real assistance, it should probably be omitted.

### 2. Real life before framework purity
The assistant should begin with the user’s actual priorities, responsibilities, and stuck points.

### 3. Minimum viable memory
Keep enough continuity to be helpful. Avoid memory sprawl.

### 4. Trust is a feature
The assistant should be predictable about boundaries, uncertainty, and when it acts versus asks.

### 5. Compression matters
A durable system should get easier to use over time, not heavier.

## Early setup stance

DAOS favors a minimum-viable setup flow.

The opening questions should focus on things like:
- what matters most right now
- the top few active projects
- what each project is, why it matters, and what is stuck or next
- the main current constraints or responsibilities
- how the user wants reminders, task support, and boundaries handled

This keeps setup anchored to real usefulness instead of forcing premature ontology design.

## Repository roadmap

Current public-docs sequence:
- [x] `README.md`
- [x] `docs/thesis.md`
- [x] `docs/memory.md`
- [ ] `docs/behavior.md`
- [ ] `docs/wizard.md`
- [ ] `examples/carlton-instance.md`

## Non-goals

DAOS is not currently trying to be:
- a giant enterprise agent platform
- a fully general memory theory
- a framework with dozens of required configuration objects
- a replacement for judgment, verification, or human oversight

## Status

This repo is in early public formulation. The core ideas are being distilled from real assistant-building work rather than invented all at once.

That is intentional.
