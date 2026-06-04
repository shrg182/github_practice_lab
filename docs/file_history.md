# File History

You can compare the **current version** and the **previous version** in three useful ways.

## 1. Compare current file with the last Git commit

In Terminal, inside your project folder:

```bash
git status
```

Then compare all changed files:

```bash
git diff
```

Or compare only your to-do script:

```bash
git diff todo_list.py
```

This shows changes between:

```text
last committed version  vs  current working version
```

Lines removed usually start with:

```text
-
```

Lines added usually start with:

```text
+
```

## 2. Compare current version in VS Code

In VS Code:

1. Open the project folder.
2. Click **Source Control** on the left sidebar.
3. Find `todo_list.py` under **Changes**.
4. Click the file name.

VS Code will open a side-by-side comparison:

```text
Previous committed version | Current edited version
```

This is usually the easiest way to review changes visually.

## 3. Compare two committed versions

First check your commit history:

```bash
git log --oneline
```

You may see something like:

```text
a1b2c3d Improve todo list script
f6e7d8c Add todo list script
```

To compare two commits:

```bash
git diff f6e7d8c a1b2c3d
```

Or for one file only:

```bash
git diff f6e7d8c a1b2c3d -- todo_list.py
```

## Very useful commands

See what changed now:

```bash
git diff
```

See what files changed:

```bash
git status
```

See previous commits:

```bash
git log --oneline
```

See one old version of a file:

```bash
git show HEAD~1:todo_list.py
```

Compare current file with the previous commit:

```bash
git diff HEAD~1 -- todo_list.py
```

## Important note

This only works well if you have already used Git commits. A commit is like a saved history point.

Good workflow:

```bash
git status
git add todo_list.py
git commit -m "Add todo list script"
```

Then after editing:

```bash
git diff todo_list.py
```

Recommended next step: run this first inside your project folder:

```bash
git status
git diff todo_list.py
```
