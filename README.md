# Wave Template
My personal starting point for creating new H2O Wave Applications.

## Local Development
By default, we use python 3.7 in the `Makefile` to match the default distribution running in the H2O AI Hybrid Cloud.

Build a python environment with:
```shell script
make setup
```

This app currently runs on Wave SDK version 0.16.0. Download and run the Wave server with:
```shell script
make wave run-wave
```

Run the application in development mode which will auto-update with any code changes:

```shell script
make run-app
```


