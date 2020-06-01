#Create a simulator object
set ns [new Simulator]

#Open the Trace file
set tf [open drfq.tr w]
$ns trace-all $tf

#Define a 'finish' procedure
proc finish {} {
        global ns tf
        $ns flush-trace
        close $tf
        exit 0
}

#Create four nodes
set n0 [$ns node]
set n1 [$ns node]

#Create links between the nodes
$ns duplex-link $n0 $n1 2Mb 10ms DropTail

#Set Queue Size of link (n0-n1) to 100
$ns queue-limit $n0 $n1 100

#Setup a UDP connection
set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0
set udpr0 [new Agent/UDP]
$ns attach-agent $n1 $udpr0
$ns connect $udp0 $udpr0
$udp0 set packetSize_ 3500
$udp0 set fid_ 0

#Setup a UDP connection
set udp1 [new Agent/UDP]
$ns attach-agent $n0 $udp1
set udpr1 [new Agent/UDP]
$ns attach-agent $n1 $udpr1
$ns connect $udp1 $udpr1
$udp1 set packetSize_ 3500
$udp1 set fid_ 1

#Setup a UDP connection
set udp2 [new Agent/UDP]
$ns attach-agent $n0 $udp2
set udpr2 [new Agent/UDP]
$ns attach-agent $n1 $udpr2
$ns connect $udp2 $udpr2
$udp2 set packetSize_ 3500
$udp2 set fid_ 2

#Setup a CBR over UDP connection
set cbr0 [new Application/Traffic/CBR]
$cbr0 attach-agent $udp0
$cbr0 set type_ CBR
$cbr0 set packet_size_ 3500
$cbr0 set rate_ 0.5mb
$cbr0 set random_ false

set drfq0 [new Application/DrfqApp]
$drfq0 attach-agent $udpr0
$drfq0 set flowid_ 0
$drfq0 set profile0_ 2
$drfq0 set profile1_ 10

set drfq1 [new Application/DrfqApp]
$drfq1 attach-agent $udpr1
$drfq1 set flowid_ 1
$drfq1 set profile0_ 7
$drfq1 set profile1_ 3

set drfq2 [new Application/DrfqApp]
$drfq2 attach-agent $udpr2
$drfq2 set flowid_ 2
$drfq2 set profile0_ 3
$drfq2 set profile1_ 10

#Setup a CBR over UDP connection
set cbr1 [new Application/Traffic/CBR]
$cbr1 attach-agent $udp1
$cbr1 set type_ CBR
$cbr1 set packet_size_ 700
$cbr1 set rate_ 1mb
$cbr1 set random_ false

#Setup a CBR over UDP connection
set cbr2 [new Application/Traffic/CBR]
$cbr2 attach-agent $udp2
$cbr2 set type_ CBR
$cbr2 set packet_size_ 500
$cbr2 set rate_ 2mb
$cbr2 set random_ false

#Schedule events for the CBR agents
$ns at 0.1 "$cbr0 start"
$ns at 2.0 "$cbr0 stop"
$ns at 1.1 "$cbr1 start"
$ns at 3.0 "$cbr1 stop"
$ns at 2.1 "$cbr2 start"
$ns at 4.0 "$cbr2 stop"

$ns at 0.0 "$drfq0 start"
$ns at 6.05 "$drfq0 stop"
$ns at 0.0 "$drfq1 start"
$ns at 6.05 "$drfq1 stop"
$ns at 0.0 "$drfq2 start"
$ns at 6.05 "$drfq2 stop"

#Call the finish procedure after 4 seconds of simulation time
$ns at 6.1 "finish"

#Print CBR packet size and interval
#puts "CBR packet size = [$cbr set packet_size_]"
#puts "CBR interval = [$cbr set interval_]"

#Run the simulation
$ns run

