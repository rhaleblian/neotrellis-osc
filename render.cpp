// render.cpp
//
// Audio process which speaks with NeoTrellis.
// Run this concurrently with neotrellis.py.
// See README.md for usage instructions.
//
// 2021 yoyodyne research

#include <Bela.h>
#include <libraries/Gui/Gui.h>
#include <iostream>
#include "osc.h"

Gui gui;
int audioChannels;
int analogChannels;

void auxiliary_task(void*)
{
	while(!Bela_stopRequested()) {
	}
}

bool setup(BelaContext *context, void *userData)
{
	audioChannels = std::min(context->audioInChannels,
		context->audioOutChannels);
	analogChannels = std::min(context->analogInChannels,
		context->analogOutChannels);

	osc_setup();
	
	gui.setup(context->projectName);
	Bela_runAuxiliaryTask(auxiliary_task);

	return true;
}

void render(BelaContext *context, void *userData)
{
	// Pass through audio channels.
	static double audio;
	for (unsigned int ch=0; ch < audioChannels; ch++) {
		for(unsigned int n = 0; n < context->audioFrames; n++)
		{
			audio = audioRead(context, n, ch);
			audioWrite(context, n, ch, audio);
		}
	}
}

void cleanup(BelaContext *context, void *userData)
{
	// TODO: clean up OSC
}
