## Wave App / Module Name

The template I use when starting new H2O Wave app projects. 

## Compatibility Matrix

This app has no specific platform or product dependencies and is expected to 
work with any HAIC release.

This version of Product was tested to be compatible with

- HAIC Version Suite: 22.07.1

## Network / Internet Dependencies

Outside of installing initial python libraries, this app does not require 
any specific network or internet access. 

## Infrastructure Dependencies

This application was specifically tested on the default python runtime of 
the AI App Store at the time of writing: Python3.7

## Special Kubernetes Configurations

None

## Application Configuration Options

This app has no configuration options

## Installation instructions

Import the app using the h2o CLI:
```shell script
h2o import bundle -v ALL_USERS
```

## Upgrade instructions

There is no specific upgrade path for this app, new versions can be installed 
by following the installation instructions. 

It is recommended to remove the older version from being published in the AI 
App Store by changing the visibility to `private`.
```shell script
h2o app update -v PRIVATE <APPID>
```

## Validation instructions
Before installing the app, you can test that it works in the environment by 
running `h2o bundle test`. You should see:
![Screen1](./static/screenshot-1.png "Screen1")

