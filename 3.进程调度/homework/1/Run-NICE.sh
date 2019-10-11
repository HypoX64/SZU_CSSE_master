taskset -c 0 ./HelloWorld-loop &
taskset -c 0 nice -6 ./HelloWorld-loop &