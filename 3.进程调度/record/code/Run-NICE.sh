taskset -c 0 ./HelloWorld-loop &
taskset -c 0 nice -10 ./HelloWorld-loop &