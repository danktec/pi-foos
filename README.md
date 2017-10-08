# pi-foos
Raspberry Pi foosball table game automation

## Overview
Utilizes GPIO Pins on a Pi to record goals for 2 teams/sides up to 5 goals which results in a round win. Record best out of 3 round wins and post the results to a RESTful API/Website.

A UUID is generated per _game_ which can be used by the API/Website to record all goals and round winners.

Users should log into the API/Website to claim their game - then all stats and records can be associated and reported.

## Running It
Run this in Python 2.7 on a Pi - should be configured to automatically start up on Pi boot... 

At the end of a winning round, the game must be reset with the "game reset" button.

Cron should be used to run the update script.

## TODO
Init script for automatic service start
