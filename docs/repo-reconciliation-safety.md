# Repo reconciliation safety

Use this read-only check before trusting an old DAOS repo path, local package checkout, or memory pointer as current truth.

Run from the candidate repo:

```bash
git status --short --branch
git rev-list --left-right --count HEAD...origin/main
git worktree list
```

Then inspect nearby workspace roots for a duplicate checkout with the same remote/name. A risky report is: dirty files, ahead/behind counts, detached or old branch, or multiple candidate folders where only one matches current `origin/main`.

Safe next step: inspect diffs, compare to current history, then archive non-destructively if obsolete. Do not run `git reset --hard`, delete folders, or migrate files until the useful local changes and the current source of truth are understood.
