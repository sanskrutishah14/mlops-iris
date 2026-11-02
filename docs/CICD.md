# CI/CD Explained

```
 git push / PR
      |
      v
 +---------+    +--------+    +----------------------------+
 |  lint   | -> |  test  | -> |  docker                    |   = CI (ci.yml)
 | flake8  |    | train  |    | build, run, smoke test,    |
 +---------+    | MLflow |    | Trivy scan                 |
                | gate   |    +----------------------------+
                | pytest |
                +--------+
      | (push to main, CI green)
      v
 +------------------+    +--------------------------------------+
 | build-and-push   | -> | deploy (environment: staging)        |   = CD (cd.yml)
 | image -> GHCR    |    | kind cluster, kubectl apply,         |
 | :sha and :latest |    | rollout status, smoke test, rollback |
 +------------------+    +--------------------------------------+

 push to main  ----------------------------> Streamlit Community Cloud auto-redeploys
 git tag v1.0.0 -> release.yml -> versioned image + GitHub Release
 weekly -> Dependabot PRs for pip, Actions, Docker
```

## Workflows
| File | Trigger | What it does |
|---|---|---|
| `ci.yml` | push to main/develop, PRs to main | lint, train with MLflow + accuracy gate (>= 0.90), pytest + coverage (API, training, Streamlit UI), Docker build + container smoke test + Trivy scan |
| `cd.yml` | CI succeeds on main, or manual | push image to GHCR, deploy to Kubernetes (kind), smoke test, rollback on failure |
| `release.yml` | tag `vX.Y.Z` | versioned image on GHCR + auto release notes |
| `dependabot.yml` | weekly | dependency update PRs |

## One-time GitHub setup
1. Repo -> Settings -> Actions -> General -> Workflow permissions -> **Read and write**.
2. Settings -> Environments -> New environment **staging** (optional: add yourself as required reviewer = manual approval gate).
3. Settings -> Branches -> Add rule for `main`: require pull request + require status checks (`lint`, `test`, `docker`).
4. After first CD run: Packages -> iris-api -> Package settings -> make public if you want others to pull it.

## Try it end to end
```bash
git checkout -b feature/change-model
# edit N_ESTIMATORS in src/train.py
git add . && git commit -m "Tune model" && git push -u origin feature/change-model
# open PR -> lint/test/docker run -> merge -> CD runs -> Streamlit redeploys
git checkout main && git pull
git tag v1.0.0 && git push origin v1.0.0     # triggers release.yml
```

Show the quality gate failing: set `MIN_ACCURACY: "0.99"` in ci.yml, push, watch `test` fail, then revert with `git revert <sha>`.

## Status badge for README
```
![CI](https://github.com/<username>/mlops-project/actions/workflows/ci.yml/badge.svg)
```
