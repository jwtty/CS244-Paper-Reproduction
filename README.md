# CS244-Paper-Reproduction
Repository for CS244 spr2020 final project.

## NS2 emulation
To run ns2 emulation, you need to copy `drfq_app.h/cc` into ns-2.35 directory. 

Add Makefile rule in `ns-2.35/Makefile` (include "drfq_app.o" in the object file list). 

And add below lines in `ns-2.35/tcl/lib/ns-default.tcl` to set default values for DRFQ application:
```
Application/DrfqApp set flowid_ 0
Application/DrfqApp set profile0_ 10
Application/DrfqApp set profile1_ 10
```

Finally, run `ns drfq.tcl` to run the emulated test and check the output.