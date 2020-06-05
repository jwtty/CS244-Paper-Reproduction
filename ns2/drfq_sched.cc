#include "connector.h" 
#include "packet.h"
#include "queue.h"
#include "drfq_sched.h"
#include "stdlib.h"

#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

DrfqScheduler::DrfqScheduler() : flow_in_process_(-1), current_virtual_time_(0), drqf_timer_(this)
{
	for (int i = 0; i < 3; ++i) {
		qs_[i] = new PacketQueue();
		virtual_time_[i][0] = virtual_time_[i][1] = -1;
	}
	bind("profile00_", &profiles_[0][0]);
	bind("profile01_", &profiles_[0][1]);
	bind("profile10_", &profiles_[1][0]);
	bind("profile11_", &profiles_[1][1]);
	bind("profile20_", &profiles_[2][0]);
	bind("profile21_", &profiles_[2][1]);
	bind("qlen_",&qlen_);
}
	
DrfqScheduler::~DrfqScheduler()
{
	if (flow_in_process_ != -1) {
		drqf_timer_.cancel();
	}
	for (int i = 0; i < 3; ++i) {
		PacketQueue *q_ = qs_[i];
		if (q_->length() != 0) {
			for (Packet *p=q_->head(); p != 0; p = p->next_) {
				Packet::free(p);
			}
		}
		delete q_;
	}
}


void DrfqScheduler::recv(Packet *p, Handler *)
{
	hdr_ip *iph = hdr_ip::access(p);
	int flowid = iph->fid_;

	PacketQueue *q_ = qs_[flowid];
	// enque packets appropriately if a non-zero q already exists
	if (q_->length() !=0) {
		if (q_->length() < qlen_) {
			q_->enque(p);
			return;
		}
		else {
			drop(p);
			return;
		}
	}
	q_->enque(p);
	virtual_time_[flowid][0] = current_virtual_time_;
	virtual_time_[flowid][1] = current_virtual_time_ + MAX(profiles_[flowid][0], profiles_[flowid][1]);

	if (flow_in_process_ == -1) {
		schedule_next_packet();
	}
}

void DrfqScheduler::schedule_next_packet()
{
	int min_virtual_start_time = -1;
	for (int i = 0; i < 3; ++i) {
		if (virtual_time_[i][0] != -1) {
			if (min_virtual_start_time == -1 || min_virtual_start_time > virtual_time_[i][0]) {
				min_virtual_start_time = virtual_time_[i][0];
				flow_in_process_ = i;
			}
		}
	}
	if (min_virtual_start_time == -1) {
		fprintf(stdout, "No flow to schedule\n");
		flow_in_process_ = -1;
		return;
	}
	PacketQueue *q_ = qs_[flow_in_process_];
	if (q_->length() == 0) {
		fprintf (stderr,"ERROR: queue for flow in process cannot be empty!\n");
		abort();
	}
	current_virtual_time_ = virtual_time_[flow_in_process_][0];
	int process_time = virtual_time_[flow_in_process_][1] - virtual_time_[flow_in_process_][0];
	Packet *p=q_->deque();
	if (q_->length() == 0) {
		virtual_time_[flow_in_process_][0] = virtual_time_[flow_in_process_][1] = -1;
	}
	else {
		virtual_time_[flow_in_process_][0] = virtual_time_[flow_in_process_][1];
		virtual_time_[flow_in_process_][1] = virtual_time_[flow_in_process_][0] + 
					MAX(profiles_[flow_in_process_][0], profiles_[flow_in_process_][1]);
	}
	drqf_timer_.resched(process_time / 100.0);
	target_->recv(p);
}

void DRQF_Timer::expire(Event* /*e*/)
{
	drqf_sched_->schedule_next_packet();
}


static class DrqfSchedClass : public TclClass {
public:
	DrqfSchedClass() : TclClass ("DrqfScheduler") {}
	TclObject* create(int,const char*const*) {
		return (new DrfqScheduler());
	}
}class_sched_drqf;
