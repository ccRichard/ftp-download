@echo off

net use \\127.0.0.1\package\Windows /user:test test

explorer \\127.0.0.1\package\Windows

exit