#include "random.h"
#include "drfq_app.h"
#include <stdio.h>


// DrfqApp OTcl linkage class
static class DrfqAppClass : public TclClass {
 public:
  DrfqAppClass() : TclClass("Application/DrfqApp") {}
  TclObject* create(int, const char*const*) {
    return (new DrfqApp);
  }
} class_app_drfq;


// When sample_timer_ expires, record number of packets processed
void SampleTimer::expire(Event*)
{
  t_->packet_accounting();
}


// When proc_timer_ expires, execute next packet
void ProcessTimer::expire(Event*)
{
  t_->process_next_packet();
}


// Constructor (also initialize instances of timers)
DrfqApp::DrfqApp() : packet_processed_(0), packet_pending_(0), running_(0), 
                      sample_timer_(this), proc_timer_(this)
{
  bind("profile0_", &profile0_);
  bind("profile1_", &profile1_);
  bind("flowid_", &flowid_);
}


// OTcl command interpreter
int DrfqApp::command(int argc, const char*const* argv)
{
  Tcl& tcl = Tcl::instance();
  if (argc == 2) {
    if (strcmp(argv[1], "start") == 0) {
      start();
      return (TCL_OK);
    }
    else if (strcmp(argv[1], "stop") == 0) {
      stop();
      return (TCL_OK);
    }
  }
  else if (argc == 3) {
    if (strcmp(argv[1], "attach-agent") == 0) {
      agent_ = (Agent*) TclObject::lookup(argv[2]);
      if (agent_ == 0) {
	      tcl.resultf("no such agent %s", argv[2]);
	      return(TCL_ERROR);
      }
      
      agent_->attachApp(this);
      return(TCL_OK);
    }
  }
  return (Application::command(argc, argv));
}

void DrfqApp::start()
{
  running_ = 1;
  sample_timer_.resched(1.0);
}


void DrfqApp::stop()
{
  running_ = 0;
  size_t sample_size = samples_.size();
  fprintf(stdout, "Flow %d: ", flowid_);
  for (size_t i = 0; i < sample_size; ++i) {
    fprintf(stdout, "%d ", samples_[i]);
  }
  fprintf(stdout, "\n\n");
}

void DrfqApp::packet_accounting()
{
  samples_.push_back(packet_processed_);
  packet_processed_ = 0;
  if (running_) {
    sample_timer_.resched(1.0);
  }
}

void DrfqApp::process_next_packet()
{
  --packet_pending_;
  packet_processed_++;
  if (!running_) {
    return;
  }
  if (packet_pending_ > 0) {
    proc_timer_.resched(proc_time_est());
  }
}

double DrfqApp::proc_time_est()
{
  return max(profile0_, profile1_) * 1.0 / 100.0;
}

// Receive message from underlying agent
void DrfqApp::process_data(int size, AppData* data)
{
  ++packet_pending_;
  if (packet_pending_ == 1) {
    proc_timer_.resched(proc_time_est());
  }
}