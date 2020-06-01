
/*
 * drqf_app.h
 */

#ifndef ns_drqf_app_h
#define ns_drqf_app_h

#include "timer-handler.h"
#include "packet.h"
#include "app.h"
#include <vector>

class DrfqApp;

// Timer used to maintain sampling frequency
// Record number of packets processed every 1s
class SampleTimer : public TimerHandler {
 public:
	SampleTimer(DrfqApp* t) : TimerHandler(), t_(t) {}
	inline virtual void expire(Event*);
 protected:
	DrfqApp* t_;
};


// Timer used to emulate the process of a single packet
// in the flow
class ProcessTimer : public TimerHandler {
 public:
	ProcessTimer(DrfqApp* t) : TimerHandler(), t_(t) {}
	inline virtual void expire(Event*);
 protected:
	DrfqApp* t_;
};


// Dominant Resource Fairness Queuing Application Class Definition
class DrfqApp : public Application {
 public:
	DrfqApp();
	void process_data(int size, AppData* data);
	void packet_accounting();   // called by SampleTimer:expire
	void process_next_packet(); // called by ProcessTimer:expire
 protected:
	int command(int argc, const char*const* argv);
	void start();       // Start sending data packets (Sender)
	void stop();        // Stop sending data packets (Sender)
 private:
	std::vector<int> samples_;     // Record all the samples
	int flowid_;                   // Identifier for different applications
	int packet_processed_;         // Number of packets processed in current period
	int packet_pending_;           // Number of packets pending to process
	int profile0_, profile1_;      // Resource profiles
	int running_;                  // If 1 application is running
	SampleTimer sample_timer_;     // SampleTimer
	ProcessTimer  proc_timer_;     // ProcessTimer
	inline double proc_time_est(); // Estimate process time of a single packet
};


#endif // ns_drqf_app_h
