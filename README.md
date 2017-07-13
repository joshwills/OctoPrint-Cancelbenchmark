# OctoPrint-Cancelbenchmark

Quick and hacky OctoPrint plugin to test how long it takes for printer firmware to respond to a "M114" command after the print has been canceled in OctoPrint.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/joshwills/OctoPrint-Cancelbenchmark/archive/master.zip

## Configuration
Add "G80" to a .gcode file you've run before, preferably somewhere in the first layer during a set of long solid layer infill lines; when the plugin detects that "G80" has been sent, it will send/add "M114" to the queue and cancel the print in OctoPrint.  When the plugin detects a response line with "Count" in it (the response from recent versions of Marlin to "M114") it will calculate the time between canceling and receiving that line.  All of this is done in the Python/server side, and all output is to the server Info log (octoprint.log is one way of viewing this).
