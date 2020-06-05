#ifndef ns_drqf_sched_h
#define ns_drqf_sched_h

#include "connector.h"
#include "timer-handler.h"

class DrfqScheduler;

class DRQF_Timer : public TimerHandler {
public:
	DRQF_Timer(DrfqScheduler *t) : TimerHandler() { drqf_sched_ = t;}
	
protected:
	virtual void expire(Event *e);
	DrfqScheduler *drqf_sched_;
};


class DrfqScheduler : public Connector {
public:
	DrfqScheduler();
	~DrfqScheduler();
	void schedule_next_packet();
protected:
	void recv(Packet *, Handler *);
	int flow_in_process_;      // id of the current flow in process, -1 if idle
	int virtual_time_[3][2];   // virtual start/finish time of each flow
	int profiles_[3][2];       // resource profiles of the flows
	int current_virtual_time_; // current system virtual time
	int qlen_;                 // maximum length of each queue
	PacketQueue *qs_[3];       // queue for each flow
	DRQF_Timer drqf_timer_;    // scheduler timer
};

#endif
