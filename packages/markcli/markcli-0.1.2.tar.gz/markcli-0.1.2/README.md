# `markcli` - An Jupyter-inspired CLI Documentation Tool

## Description
Run markcli to fill a template that results from running the cli command included inside.

CLI commands are written in html comments (here with sapces added to avoid rendering) using the following syntax:

```
< ! - - 
command_object
- ->
```

Where `command_object` is a json string object. The minimal object, where all parameters are defaulted is:
```json
{
    "command": "some bash command"
}
```

 with the following properties (first option is default)
```javascript
{
    "command": "ls -lt",
    "print_command": false/true             // print the command in the document
    "output-format": "bash"/code block id   // Any value supported by md code blocks (e.g. json, python, etc.)
    "limit": 0/any number                   // limit the number of lines printed
    "error-strategy": "ignore"\"exit",      // Behavior on error
    "skip": false/true,                     // If true, this command is not run. If true, it is run, and if the following block is an output (of a previous command), it is updated.
     "object-type": N/A                     // Used internally by markcli to mark output blocks
}
```

Example: running the previous will result in:

<!--
{
    "print_command": true,
    "command": "ls -lt"
}
-->
<!-- { "object-type": "command-output-start" } -->
```bash
ls -lt
```
```bash
total 24
-rw-r--r-- 1 runner docker     0 May  7 04:54 README.md
-rw-r--r-- 1 runner docker 11357 May  7 04:54 LICENSE
drwxr-xr-x 2 runner docker  4096 May  7 04:54 markcli
-rw-r--r-- 1 runner docker  1065 May  7 04:54 setup.py
-rw-r--r-- 1 runner docker  2982 May  7 04:54 template.md
```
<!-- { "object-type": "command-output-end" } -->


Commands can use environment variables, the parser assumes that any capitalized word is an environemnt variable. Example:
<!--
{
    "print_command": true,
    "command": "echo $HOME"
}
-->
<!-- { "object-type": "command-output-start" } -->
```bash
echo $HOME
```
```bash
/home/runner
```
<!-- { "object-type": "command-output-end" } -->


There are two options to handle errors: To include the error code as the result of running the command, or to exit the document creation process. 
<!--
{
    "print_command": true,
    "command": "ec ho $HOME"
}
-->
<!-- { "object-type": "command-output-start" } -->
```bash
ec ho $HOME
```
```bash
/bin/sh: 1: ec: not found
```
<!-- { "object-type": "command-output-end" } -->


Using the `"skip": true` option, the command is not run. This is useful for commands that consume a lot of time or resources, and is adequate for cases where the work on the file is interactive (the inputfile is also the outputfile)

The output-fomat can be any format supported by markdown code blocks like `json`, `yml`. The default is `bash`. The output can be limited to a specific number of lines, using the `limit` option. Following is an example of using the `python` format and a limit:
<!--
{
    "command": "cat markcli/markcli.py",
    "print_command": true,
    "output-format": "python",
    "limit": 11
}
-->
<!-- { "object-type": "command-output-start" } -->
```bash
cat markcli/markcli.py
```
```python
import os
import subprocess
import shlex
import json
import jsonargparse

def setup_parser():
    
    parser = jsonargparse.ArgumentParser(
        description="A command line tool for generating templated documentation from clis",
    )
```
<!-- { "object-type": "command-output-end" } -->


# Installation

To install markcli, run:
```bash
pip install markcli
```

Then the command `markcli` will be available.

# A real-world example: document the valint command:

## Intall valint
To install valint run (Note that the -- 2>&1 is required to capture the output in this setting, but is not required in a normal shell):
<!--
{
    "command": "curl -sSfL https://get.scribesecurity.com/install.sh  | sh -s -- -t valint -D -- 2>&1",
    "print_command": true
}
-->
<!-- { "object-type": "command-output-start" } -->
```bash
curl -sSfL https://get.scribesecurity.com/install.sh  | sh -s -- -t valint -D -- 2>&1
```
```bash
scribe info Installer - Scribe CLI tools
scribe info Selected, tool=valint, version=latest
scribe info Trying to download, tool=valint, version=latest
scribe info Using dev artifacts, subpath='dev/valint/linux/amd64', ENV=dev
scribe info Downloading, Version=1.4.0-6
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
 85 28.5M   85 24.4M    0     0  44.1M      0 --:--:-- --:--:-- --:--:-- 44.1M
100 28.5M  100 28.5M    0     0  47.0M      0 --:--:-- --:--:-- --:--:-- 46.9M
scribe info Installed /home/runner/.scribe/bin/valint

```
<!-- { "object-type": "command-output-end" } -->


## General options
<!--
{
    "command": "$HOME/.scribe/bin/valint --help"
}
-->
<!-- { "object-type": "command-output-start" } -->
```bash
Command Line Interpreter (CLI) tool,that empowers supply chain stakeholders to ensure supply chain integrity, verify compliance, and generate and manage evidence.

Usage:
  valint [command]

Available Commands:
  bom         Create evidence command
  discard     Discard evidence
  download    Downloads the evidence based on cache
  evidence    Add file as evidence command
  help        Help about any command
  list        List evidence command
  slsa        Create SLSA provenance evidence command
  verify      Verify compliance policies against evidence to ensure the integrity of supply chain.

Flags:
      --allow-expired                 Allow expired certs
      --attest.config string          Attestation config path
      --attest.default string         Attestation default config, options=[sigstore sigstore-github x509 x509-env] (default "sigstore")
      --backoff string                Backoff duration (default "15s")
      --ca string                     x509 CA Chain path
      --cache-enable                  Enable local cache (default true)
      --cert string                   x509 Cert path
  -c, --config string                 Configuration file path
      --context-dir string            Context dir
  -C, --context-type string           CI context type, options=[jenkins github circleci azure gitlab travis tekton bitbucket local admission] (default "local")
      --crl string                    x509 CRL path
      --crl-full-chain                Enable Full chain CRL verfication
      --deliverable string            Mark as deliverable, options=[true, false]
      --depth int                     Git clone depth
      --disable-crl                   Disable certificate revocation verificatoin
  -e, --env strings                   Environment keys to include in evidence
  -F, --filter-regex strings          Filter out files by regex (default [**/*.pyc,**/.git/**])
      --filter-scope strings          Filter packages by scope
  -G, --gate string                   Policy Gate name
      --git-auth string               Git repository authentication info, [format: 'username:password']
      --git-branch string             Git branch in the repository
      --git-commit string             Git commit hash in the repository
      --git-tag string                Git tag in the repository
  -h, --help                          help for valint
      --key string                    x509 Private key path
  -L, --label strings                 Add Custom labels
  -D, --level string                  Log depth level, options=[panic fatal error warning info debug trace]
      --log-context                   Attach context to all logs
      --log-file string               Output log to file
      --oci                           Enable OCI store
  -R, --oci-repo string               Select OCI custom attestation repo
  -d, --output-directory string       Output directory path (default "/home/runner/.cache/valint")
  -O, --output-file string            Output file name
  -p, --pipeline-name string          Pipeline name
      --platform string               Select target platform, examples=windows/armv6, arm64 ..)
      --predicate-type string         Custom Predicate type (generic evidence format) (default "http://scribesecurity.com/evidence/generic/v0.1")
  -n, --product-key string            Product Key
  -V, --product-version string        Product Version
  -q, --quiet                         Suppress all logging output
      --rule-args stringToString      Policy arguments (default [])
  -U, --scribe.client-id string       Scribe Client ID
  -P, --scribe.client-secret string   Scribe Client Secret
  -E, --scribe.enable                 Enable scribe client
  -u, --scribe.url string             Scribe API Url (default "https://api.scribesecurity.com")
  -s, --show                          Print evidence to stdout
      --structured                    Enable structured logger
      --timeout string                Timeout duration (default "120s")
  -v, --verbose count                 Log verbosity level [-v,--verbose=1] = info, [-vv,--verbose=2] = debug
      --version                       version for valint

Use "valint [command] --help" for more information about a command.
```
<!-- { "object-type": "command-output-end" } -->


## Bom command
<!--
{
    "command": "$HOME/.scribe/bin/valint bom --help"
}
-->
<!-- { "object-type": "command-output-start" } -->
```bash
Collect, Create and Store evidence for artifacts (SBOMs,SLSA provenance) or any third-party tools.

Usage:
  valint bom [TARGET] [flags]

Examples:
  valint bom <target>
  
  <target> Target object name format=[<image:tag>, <dir path>, <git url>]

  valint bom alpine:latest                         create default (cyclonedxjson) sbom
  valint bom alpine:latest -o cyclonedxxml         create cyclonedx xml sbom
  valint bom alpine:latest -o attest               create intoto attestation of cyclonedx sbom 
  valint bom alpine:latest -o attest-slsa          create intoto attestation of SLSA provenance
  valint bom alpine:latest                     show verbose debug information
  valint bom alpine:latest -A "*/**"           collect files content in to SBOM

  Supports the following image sources:
  valint bom yourrepo/yourimage:tag     defaults to using images from a Docker daemon. If Docker is not present, the image is pulled directly from the registry.

  You can also explicitly specify the scheme to use:
  valint bom docker:yourrepo/yourimage:tag          explicitly use the Docker daemon
  valint bom podman:yourrepo/yourimage:tag          explicitly use the Podman daemon
  valint bom docker-archive:path/to/yourimage.tar   use a tarball from disk for archives created from "docker save"
  valint bom oci-archive:path/to/yourimage.tar      use a tarball from disk for OCI archives (from Skopeo or otherwise)
  valint bom dir:path/to/yourproject                read directly from a path on disk (any directory)
  valint bom registry:yourrepo/yourimage:tag        pull image directly from a registry (no container runtime required)
  valint bom file:path/to/yourproject/file          read directly from a path on disk (any single file)
  valint bom git:path/to/yourrepository             read directly from a local repository on disk
  valint bom git:https://github.com/yourrepository.git         read directly from a remote repository on git

  SBOM-Example:
  valint bom alpine:latest -o attest
  valint bom alpine:latest -o statement

  SLSA-Example:
  valint bom alpine:latest -o attest-slsa
  valint bom alpine:latest -o statement-slsa

  Generic-Example:
  valint bom file.json -o attest-slsa
  valint bom file.json -o statement-slsa

  Format-aliases:
  * json=attest-cyclonedx-json
  * predicate=predicate-cyclonedx-json
  * statement=statement-cyclonedx-json
  * attest=attest-cyclonedx-json


Flags:
  -A, --attach-regex strings           Attach files content by regex
      --author-email string            Set author email
      --author-name string             Set author name
      --author-phone string            Set author phone
      --components strings             Select sbom components groups, options=[metadata layers packages syft files dep commits] (default [metadata,layers,packages,syft,dep,commits])
  -f, --force                          Force overwrite cache
  -o, --format strings                 Evidence format, options=[cyclonedx-json cyclonedx-xml attest-cyclonedx-json statement-cyclonedx-json attest-slsa statement-slsa statement-generic attest-generic] (default [cyclonedx-json])
  -h, --help                           help for bom
      --package-exclude-type strings   Exclude package type, options=[ruby python javascript java dpkg apk rpm go dotnet r rust binary sbom nix conan alpm cocoapods swift dart elixir php erlang github portage haskell kernel]
      --package-group string           Select package group, options=[index install all]
  -t, --package-type strings           Select package type, options=[ruby python javascript java dpkg apk rpm go dotnet r rust binary sbom nix conan alpm cocoapods swift dart elixir php erlang github portage haskell kernel]
      --supplier-email string          Set supplier email
      --supplier-name string           Set supplier name
      --supplier-phone string          Set supplier phone
      --supplier-url strings           Set supplier url
      --version                        version for bom

Global Flags:
      --allow-expired                 Allow expired certs
      --attest.config string          Attestation config path
      --attest.default string         Attestation default config, options=[sigstore sigstore-github x509 x509-env] (default "sigstore")
      --backoff string                Backoff duration (default "15s")
      --ca string                     x509 CA Chain path
      --cache-enable                  Enable local cache (default true)
      --cert string                   x509 Cert path
  -c, --config string                 Configuration file path
      --context-dir string            Context dir
  -C, --context-type string           CI context type, options=[jenkins github circleci azure gitlab travis tekton bitbucket local admission] (default "local")
      --crl string                    x509 CRL path
      --crl-full-chain                Enable Full chain CRL verfication
      --deliverable string            Mark as deliverable, options=[true, false]
      --depth int                     Git clone depth
      --disable-crl                   Disable certificate revocation verificatoin
  -e, --env strings                   Environment keys to include in evidence
  -F, --filter-regex strings          Filter out files by regex (default [**/*.pyc,**/.git/**])
      --filter-scope strings          Filter packages by scope
  -G, --gate string                   Policy Gate name
      --git-auth string               Git repository authentication info, [format: 'username:password']
      --git-branch string             Git branch in the repository
      --git-commit string             Git commit hash in the repository
      --git-tag string                Git tag in the repository
      --key string                    x509 Private key path
  -L, --label strings                 Add Custom labels
  -D, --level string                  Log depth level, options=[panic fatal error warning info debug trace]
      --log-context                   Attach context to all logs
      --log-file string               Output log to file
      --oci                           Enable OCI store
  -R, --oci-repo string               Select OCI custom attestation repo
  -d, --output-directory string       Output directory path (default "/home/runner/.cache/valint")
  -O, --output-file string            Output file name
  -p, --pipeline-name string          Pipeline name
      --platform string               Select target platform, examples=windows/armv6, arm64 ..)
      --predicate-type string         Custom Predicate type (generic evidence format) (default "http://scribesecurity.com/evidence/generic/v0.1")
  -n, --product-key string            Product Key
  -V, --product-version string        Product Version
  -q, --quiet                         Suppress all logging output
      --rule-args stringToString      Policy arguments (default [])
  -U, --scribe.client-id string       Scribe Client ID
  -P, --scribe.client-secret string   Scribe Client Secret
  -E, --scribe.enable                 Enable scribe client
  -u, --scribe.url string             Scribe API Url (default "https://api.scribesecurity.com")
  -s, --show                          Print evidence to stdout
      --structured                    Enable structured logger
      --timeout string                Timeout duration (default "120s")
  -v, --verbose count                 Log verbosity level [-v,--verbose=1] = info, [-vv,--verbose=2] = debug
```
<!-- { "object-type": "command-output-end" } -->


