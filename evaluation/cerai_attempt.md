# CeRAI Setup Attempt

I attempted to run the official CeRAI AI Evaluation Tool locally and documented the outcome.

## Repository

```text
https://github.com/cerai-iitm/AIEvaluationTool
```

The repository was cloned locally and its documentation was reviewed, including the Docker CLI workflow, importer/testcase execution flow, and test plan/metric structure.

## Docker Setup Attempt

CeRAI expects a root `.env` file. I created it from `.env.example`:

```powershell
Copy-Item -LiteralPath '.env.example' -Destination '.env' -Force
```

I then validated the Compose configuration:

```powershell
docker compose config --quiet
```

Result: Compose configuration validated successfully. Docker printed a warning that it could not read the user-level Docker config at `C:\Users\shahh\.docker\config.json`, but the compose file itself was valid.

I then attempted to start the required CeRAI services:

```powershell
docker compose up -d db selenium-browser interface-manager auth-service tdms-backend app-backend
```

Result:

```text
unable to get image 'mariadb:11': failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine; check if the path is correct and if the daemon is running: open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

Interpretation: Docker Desktop's Linux engine was not running or reachable in the local environment, so the official Docker workflow could not be completed during this pass.

## Local CLI Attempt

I also tried invoking the CeRAI testcase executor help command directly:

```powershell
python src\app\testcase_executor\main.py --config config.json -h
```

Result:

```text
ModuleNotFoundError: No module named 'rich'
```

Interpretation: the local Python runtime did not yet have CeRAI's full dependency set installed. Installing the full `requirements.txt` is substantial because CeRAI includes Selenium, transformer models, evaluation libraries, database connectors, dashboard dependencies, and optional model-service integrations.

## What Was Completed Despite This

Because the official CeRAI execution path was blocked by local environment setup, I completed the following:

- Reviewed CeRAI's documented Docker and CLI workflow.
- Mapped the assignment test suite to CeRAI's responsible AI, safety, language support, conversational quality, and task performance areas.
- Built a REST conversational endpoint compatible with API-style evaluation.
- Created a 23-case domain-specific test suite.
- Included a transparent local evaluator to produce reproducible results while making clear that it is not a replacement for CeRAI.

## Next Step For Full CeRAI Execution

To complete a full CeRAI run:

1. Start Docker Desktop and ensure the Linux engine is available.
2. Run `docker compose up -d db selenium-browser interface-manager auth-service tdms-backend app-backend`.
3. Import datapoints into CeRAI's TDMS/database workflow.
4. Register the local or deployed endpoint as an API target.
5. Execute relevant plans for safety, responsible AI, language support, conversational quality, and task performance.
6. Export raw CeRAI outputs into `results/`.

