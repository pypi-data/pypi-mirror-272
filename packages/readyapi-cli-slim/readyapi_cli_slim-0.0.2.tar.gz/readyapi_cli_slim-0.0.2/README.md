# ReadyAPI CLI

<a href="https://github.com/khulnasoft/readyapi-cli/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/khulnasoft/readyapi-cli/actions/workflows/test.yml/badge.svg" alt="Test">
</a>
<a href="https://github.com/khulnasoft/readyapi-cli/actions/workflows/publish.yml" target="_blank">
    <img src="https://github.com/khulnasoft/readyapi-cli/actions/workflows/publish.yml/badge.svg" alt="Publish">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/khulnasoft/readyapi-cli" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/khulnasoft/readyapi-cli.svg" alt="Coverage">
<a href="https://pypi.org/project/readyapi-cli" target="_blank">
    <img src="https://img.shields.io/pypi/v/readyapi-cli?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

---

**Source Code**: <a href="https://github.com/khulnasoft/readyapi-cli" target="_blank">https://github.com/khulnasoft/readyapi-cli</a>

---

Run and manage ReadyAPI apps from the command line with ReadyAPI CLI. 🚀

## Description

**ReadyAPI CLI** is a command line program `readyapi` that you can use to serve your ReadyAPI app, manage your ReadyAPI project, and more.

When you install ReadyAPI (e.g. with `pip install readyapi`), it includes a package called `readyapi-cli`, this package provides the `readyapi` command in the terminal.

To run your ReadyAPI app for development, you can use the `readyapi dev` command:

<div class="termy">

```console
$ readyapi dev main.py
INFO     Using path main.py
INFO     Resolved absolute path /home/user/code/awesomeapp/main.py
INFO     Searching for package file structure from directories with __init__.py files
INFO     Importing from /home/user/code/awesomeapp

 ╭─ Python module file ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

INFO     Importing module main
INFO     Found importable ReadyAPI app

 ╭─ Importable ReadyAPI app ─╮
 │                          │
 │  from main import app    │
 │                          │
 ╰──────────────────────────╯

INFO     Using import string main:app

 ╭────────── ReadyAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  readyapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [56345] using WatchFiles
INFO:     Started server process [56352]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

That command line program called `readyapi` is **ReadyAPI CLI**.

ReadyAPI CLI takes the path to your Python program and automatically detects the variable with the ReadyAPI (commonly named `app`) and how to import it, and then serves it.

For production you would use `readyapi run` instead. 🚀

## `readyapi dev`

When you run `readyapi dev`, it will run on development mode.

By default, it will have **auto-reload** enabled, so it will automatically reload the server when you make changes to your code. This is resource intensive and could be less stable than without it, you should only use it for development.

By default it will listen on the IP address `127.0.0.1`, which is the IP for your machine to communicate with itself alone (`localhost`).

## `readyapi run`

When you run `readyapi run`, it will run on production mode by default.

It will have **auto-reload disabled** by default.

It will listen on the IP address `0.0.0.0`, which means all the available IP addresses, this way it will be publicly accessible to anyone that can communicate with the machine. This is how you would normally run it in production, for example, in a container.

In most cases you would (and should) have a "termination proxy" handling HTTPS for you on top, this will depend on how you deploy your application, your provider might do this for you, or you might need to set it up yourself. You can learn more about it in the <a href="https://readyapi.khulnasoft.com/deployment/" class="external-link" target="_blank">ReadyAPI Deployment documentation</a>.

## License

This project is licensed under the terms of the MIT license.
