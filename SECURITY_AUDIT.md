# Security Audit Report — 25fall-CV

**Date**: 2026-05-30  
**Scope**: Full codebase (`模型代码.ipynb`, `requirements.txt`, `dataset.yaml`, repo config)

---

## Summary

| Category | Findings | Severity | Fixed? |
|---|---|---|---|
| Unsafe archive extraction (path traversal) | 3 instances | **Critical** | Yes |
| Unsafe `torch.load` (arbitrary code execution) | 6 instances | **Critical** | Yes |
| Unpinned dependencies | 8 packages | **High** | Yes |
| Missing `.gitignore` | Secrets/weights could be committed | **High** | Yes |
| Bare `except:` clauses | 12 instances | **Medium** | No (noted) |
| Hardcoded platform paths | ~80 references | **Low** | No (noted) |
| SQL injection | 0 | — | N/A |
| Hardcoded API keys / secrets | 0 | — | N/A |
| CORS / web endpoints | 0 | — | N/A |
| Debug endpoints | 0 | — | N/A |
| Missing authentication | 0 | — | N/A |

---

## Critical — Fixed

### 1. Unsafe Archive Extraction (Path Traversal — CVE-2007-4559)

**Cells affected**: 1, 36  
**Risk**: `zipfile.extractall()` and `tarfile.extractall()` can write files outside the target directory if the archive contains paths with `..` or absolute paths. An attacker who controls the archive contents could overwrite arbitrary files on disk.

**Fix**: Added member validation before extraction — reject any archive member whose name is absolute or contains `..`.

### 2. Unsafe `torch.load` (Arbitrary Code Execution)

**Cells affected**: 8, 9, 11, 13, 20, 21  
**Risk**: `torch.load()` uses Python's `pickle` module under the hood. Loading an untrusted `.pth`/`.pt` file can execute arbitrary code. PyTorch ≥2.6 defaults to `weights_only=True`, but older versions do not, and explicit is better than implicit.

**Fix**: Added `weights_only=True` to all `torch.load()` calls. This restricts deserialization to tensor data only, blocking arbitrary code execution.

### 3. Unpinned Dependencies (Supply Chain Risk)

**File**: `requirements.txt`  
**Risk**: Without version constraints, `pip install` pulls the latest version of each package. A compromised or breaking release of any dependency would silently affect the project.

**Fix**: Added minimum and maximum version bounds (e.g., `torch>=2.0.0,<3.0.0`).

### 4. Missing `.gitignore`

**Risk**: Without a `.gitignore`, model weights (`.pth`, `.pt`), dataset archives (`.zip`, `.tar.gz`), environment files (`.env`), and IDE configs could be accidentally committed to the repository — potentially exposing sensitive data or bloating the repo.

**Fix**: Added a comprehensive `.gitignore` covering Python bytecode, Jupyter checkpoints, model weights, datasets, training artifacts, OS files, and IDE configs.

---

## Medium — Not Fixed (Recommendations)

### 5. Bare `except:` Clauses (12 instances)

Bare `except:` catches all exceptions including `KeyboardInterrupt` and `SystemExit`, masking real errors and making debugging difficult. **Recommendation**: Replace with `except Exception as e:` and log the error.

### 6. Hardcoded Platform Paths (~80 references to `/home/ma-user/work/`)

Many cells reference Huawei ModelArts paths (`/home/ma-user/work/`, `obs://`). These are not a direct security vulnerability, but they expose internal infrastructure details and make the code non-portable. **Recommendation**: Use relative paths or environment variables (e.g., `os.environ.get('WORK_DIR', '.')`).

---

## Not Applicable to This Codebase

The following categories were scanned and found clean:

- **Hardcoded API keys / secrets**: No API keys, passwords, or tokens found in any file.
- **SQL injection**: No database queries anywhere in the codebase.
- **Unvalidated user input**: No `input()` / `raw_input()` calls or web request handlers.
- **CORS misconfiguration**: No web server or API framework (Flask, Django, FastAPI) used.
- **Exposed debug endpoints**: No web server; no `app.run(debug=True)`.
- **Missing authentication**: No web endpoints or services to protect.
