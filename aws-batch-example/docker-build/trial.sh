#!/bin/bash

# Start time
start_time=$(date +%s)

# Fork two background processes
sleep 12 &
pid1=$!
echo ${pid1}
sleep 6 &
pid2=$!
echo ${pid2}
# Wait for both processes to complete

wait $pid1
wait $pid2

# End time
end_time=$(date +%s)

# Calculate elapsed time
elapsed_time=$((end_time - start_time))

echo "Total time elapsed: $elapsed_time seconds"