# CS244-Paper-Reproduction

This repository is our final project for CS244: Advanced Topics in Networking, Spring 2020, Stanford.

The paper introduced a new scheduler algorithm, Dominant Resource Fairness Queuing (DRFQ), that provides share guarantees and strategy-proofness in multi-resource scheme. We implemented various python scripts to simulate performance of different scheduling algorithms and wrote NS2 simulators to reproduce DRFQ's behavior.

We have reproduced figure 3, 4, 5, 9, 11, and 12 in paper "Multi-Resource Fair Queueing for Packet Processing".

## Python simulation

All python simulation scripts are located in `figures` directory. As of our project, we have developed python simulators to reproduce figure 3, 4, 5, 11, and 12. To reproduce figure X, simply run `python figure_X.py`.

## NS2 simulation

To emulate Dominant Resource fairness Queuing algorithm, we write our own ns2 application and DRFQ scheduler.

To run ns2 emulation, you need to follow below steps:

1. Copy `drfq_app.h/cc` and `drfq_sched.h/cc` into `ns-2.35/apps/` directory.

2. Add Makefile rule in `ns-2.35/Makefile` (include `apps/drfq_app.o apps/drfq_sched.o` under `OBJ_CC`).

3. Add below lines in `ns-2.35/tcl/lib/ns-default.tcl` to set default values for DRFQ application:

    ```
    Application/DrfqApp set flowid_ 0
    Application/DrfqApp set profile0_ 10
    Application/DrfqApp set profile1_ 10
    ```
    It won't break anything if you ignore this step and just run our `drfq.tcl` script. But there are warnings shown up:

    ```
    warning: no class variable XXX
    	see tcl-object.tcl in tclcl for info about this warning.
    ```
    Similar default values can also be set for DrfqScheduler.

4. Finally, run `ns drfq.tcl` to run the emulated test and you will see output like:
    ```
    Flow 0: 9,10,10,10,10,6,5,5,5,5,4,3,3,4,3,4,5,5,5,5,5,5,5,5,5,5,5,5,5,6,10,10,10,10,10,
    Flow 1: 0,0,0,0,0,4,5,5,5,5,3,4,3,3,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,4,0,0,0,0,0,
    Flow 2: 0,0,0,0,0,0,0,0,0,0,3,3,4,3,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    ```
    It prints out the number of packets processed in each second for every flow.

5. To reproduce figure 9, simply copy the output to `figure_9.py` and then run `python figure_9.py`.
