taskset -c 0 ./HelloWorld-loop &
taskset -c 0 nice -4 ./HelloWorld-loop &
taskset -c 1 ./HelloWorld-loop &
taskset -c 1 ./HelloWorld-loop &