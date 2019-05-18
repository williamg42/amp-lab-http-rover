#include <stdlib.h>
#include <signal.h>
#include <iostream>


#include "PWM.h"

#define PWM18 0
#define PWM19 1

#define PERIOD 20000000
#define StopPeriod 1500000
#define ForwardPeriod 2000000
#define ReversePeriod 1000000



PWM *Pwm0;
PWM *Pwm1;

void _cleanup(int signum)
{
	std::cout << "\nINFO: Caught signal " << signum << std::endl;
	delete Pwm0;
	delete Pwm1;
	exit(signum);
}


long map(long x, long in_min, long in_max, long out_min, long out_max)
{
	if ((in_max - in_min) > (out_max - out_min)) {
		return (x - in_min) * (out_max - out_min + 1) / (in_max - in_min + 1) + out_min;
	}
	else
	{
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
	}
}


int main(int argc, char **argv)
{




	if (argc < 2) {
		printf("Usage: PWMControl <X Value>  <Y Value>\n\n");
		printf("Give an input X and Y value, maps joystick to tank drive and sets Servo PWM");
		exit(-1);
	}


	int X = atoi(argv[1]);
	int Y = atoi(argv[2]);



	Pwm0 = new PWM(0);
//	Pwm0->setDuty(duty_ns);
	Pwm0->setPeriod(PERIOD);
//	Pwm0->setState(PWM::State::ENABLED);

	Pwm1 = new PWM(1);
//	Pwm1->setDuty(duty_ns);
	Pwm1->setPeriod(PERIOD);
//	Pwm1->setState(PWM::State::ENABLED);

	/* Register a signal handler to exit gracefully and killing the PWM pin */
	signal(SIGINT, _cleanup);

	/* Turn on the PWM */

	// Differential Steering Joystick Algorithm
// ========================================
//   by Calvin Hass
//   https://www.impulseadventure.com/elec/
//
// Converts a single dual-axis joystick into a differential
// drive motor control, with support for both drive, turn
// and pivot operations.
//

// INPUTS
	int     nJoyX = X;              // Joystick X input                     (-128..+127)
	int     nJoyY = Y;              // Joystick Y input                     (-128..+127)

// OUTPUTS
	int     nMotMixL;           // Motor (left)  mixed output           (-128..+127)
	int     nMotMixR;           // Motor (right) mixed output           (-128..+127)

// CONFIG
// - fPivYLimt  : The threshold at which the pivot action starts
//                This threshold is measured in units on the Y-axis
//                away from the X-axis (Y=0). A greater value will assign
//                more of the joystick's range to pivot actions.
//                Allowable range: (0..+127)
	float fPivYLimit = 32.0;

// TEMP VARIABLES
	float   nMotPremixL;    // Motor (left)  premixed output        (-128..+127)
	float   nMotPremixR;    // Motor (right) premixed output        (-128..+127)
	int     nPivSpeed;      // Pivot Speed                          (-128..+127)
	float   fPivScale;      // Balance scale b/w drive and pivot    (   0..1   )




// Calculate Drive Turn output due to Joystick X input
	if (nJoyY >= 0) {
		// Forward
		nMotPremixL = (nJoyX >= 0) ? 127.0 : (127.0 + nJoyX);
		nMotPremixR = (nJoyX >= 0) ? (127.0 - nJoyX) : 127.0;
	} else {
		// Reverse
		nMotPremixL = (nJoyX >= 0) ? (127.0 - nJoyX) : 127.0;
		nMotPremixR = (nJoyX >= 0) ? 127.0 : (127.0 + nJoyX);
	}

// Scale Drive output due to Joystick Y input (throttle)
	nMotPremixL = nMotPremixL * nJoyY / 128.0;
	nMotPremixR = nMotPremixR * nJoyY / 128.0;

// Now calculate pivot amount
// - Strength of pivot (nPivSpeed) based on Joystick X input
// - Blending of pivot vs drive (fPivScale) based on Joystick Y input
	nPivSpeed = nJoyX;
	fPivScale = (abs(nJoyY) > fPivYLimit) ? 0.0 : (1.0 - abs(nJoyY) / fPivYLimit);

// Calculate final mix of Drive and Pivot
	nMotMixL = (1.0 - fPivScale) * nMotPremixL + fPivScale * ( nPivSpeed);
	nMotMixR = (1.0 - fPivScale) * nMotPremixR + fPivScale * (-nPivSpeed);


	int dutytimeL = map(nMotMixL, -127, 127, 1920000, 1120000);
	int dutytimeR = map(nMotMixR, -127, 127, 1920000, 1120000);

	std::cout << dutytimeL << std::endl;
	std::cout << dutytimeR << std::endl;


	Pwm0->setDuty(dutytimeR);
	Pwm1->setDuty(dutytimeL);





	Pwm0->setState(PWM::State::ENABLED);
	Pwm1->setState(PWM::State::ENABLED);


	delete Pwm0;
	delete Pwm1;






	return 0;
}