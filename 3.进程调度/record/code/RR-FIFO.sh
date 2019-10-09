#!/bin/sh
./RR-FIFO-sched 2 90&
./RR-FIFO-sched 2 90&
sleep 5s
./RR-FIFO-sched 1 95&