#include <neotrellis.h>
#include <libraries/OscSender/OscSender.h>
#include <libraries/OscReceiver/OscReceiver.h>

OscReceiver oscReceiver;
OscSender oscSender;

struct {
	const int port = 7562;
	const char *addr = "0.0.0.0";
} oscReceiverParams;

struct {
	const int port = 7563;
	const char* addr = "127.0.0.1";
} oscSenderParams;

void on_receive(oscpkt::Message* msg, const char *sender, void* arg)
{
	int key, state = 0;
	printf("received message with address %s\n", msg->addressPattern().c_str());
	auto rc = msg->match("/1/neotrellis").popInt32(key).popInt32(state);
	if (rc)
		printf("neotrellis message from %s, key %d, state %d\n", sender, key, state);
}

void osc_setup() {
	oscReceiver.setup(oscReceiverParams.port, on_receive);
	oscSender.setup(oscSenderParams.port, oscSenderParams.addr);
}
