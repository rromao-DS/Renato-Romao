# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is Renato Romão's GitHub profile README repository (`rromao-DS/Renato-Romao`). A repo with this special name — matching the GitHub username — is rendered by GitHub as the profile page at `github.com/rromao-DS`.

There is no application code, build system, dependency manifest, linter, or test suite in this repository. The two files that matter are:

- `README.md` — the Markdown content rendered on the GitHub profile page. It embeds external badges/widgets (GitHub stats, streak stats, activity graph, jokes card) via `img` tags pointing at third-party services (github-readme-stats.vercel.app, github-readme-streak-stats.herokuapp.com, etc.), keyed off a GitHub username in each URL.
- `Imagem.png` — the profile image displayed at the top of the README.

## Working in this repo

Changes here are essentially content edits to `README.md` (or swapping `Imagem.png`) — there is nothing to build, lint, or test. When editing, preview by checking that Markdown/HTML renders correctly on GitHub, and that any embedded widget URLs use the correct username so the stats/graphics resolve.
