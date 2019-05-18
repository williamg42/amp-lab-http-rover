/*
The MIT License (MIT)

Copyright (c) 2014 Thomas Mercier Jr.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#include "PWM.h"

#include <fstream>
#include <stdexcept>

#include <boost/filesystem.hpp>

#include <fcntl.h>
#include <poll.h>
#include <sys/stat.h>

#include <iostream>
using std::cerr;
using std::endl;


PWM::PWM(unsigned short id) :
   _id(id),
   _id_str(std::to_string(id)),
   _state(PWM::State::DISABLED)
{
   initCommon();
   setState(PWM::State::DISABLED);
}




void PWM::initCommon(void)
{
   _sysfsPath = std::string("/sys/class/pwm/");

   /* validate id # */
   {
      if ( !boost::filesystem::exists(_sysfsPath) )
      {
         throw std::runtime_error(_sysfsPath + " does not exist");
      }

      using boost::filesystem::directory_iterator;
      const directory_iterator end_itr; /* default construction yields past-the-end */

      bool found = false;
      for ( directory_iterator itr(_sysfsPath); itr != end_itr; ++itr)
      {
         if ( is_directory(itr->status()) &&
               itr->path().string().find("pwmchip") != std::string::npos )
         {
            /* Obtain the base number of the chip */
            std::size_t pos = itr->path().string().find("pwmchip");
            std::string pattern = "pwmchip";
            std::string base = itr->path().string().substr(pos + pattern.length());

            std::ifstream infile(itr->path().string() + "/npwm");
            if ( !infile )
            {
               throw std::runtime_error("Unable to read  " + itr->path().string() + "/npwm");
            }

            std::string npwm;
            infile >> npwm;
            infile.close();

            /* PWM id is valid */
            if ( std::stoul(base) <= _id && _id < std::stoul(base) + std::stoul(npwm) )
            {
               found = true;
               /* Update our sysfs path for the object, we have local exports */
               _sysfsPath = itr->path().string() + "/";

               break;
            }
         }
      }
      if ( !found )
      {
         throw std::runtime_error("PWM " + _id_str + " is invalid");
      }
   }



   /* validate not already exported */
   {
      /* In decreasing order of speed: stat() -> access() -> fopen() -> ifstream */
      struct stat stat_buf;
      const std::string path(_sysfsPath + "pwm" + _id_str);
      if ( stat(path.c_str() , &stat_buf) == 0 )
      {
         throw std::runtime_error(
            "PWM " + _id_str + " already exported" +
            " (Some other PWM object already owns this PWM)");
      }
   }



   /* attempt to export */
   {
      std::ofstream sysfs_export(_sysfsPath + "export", std::ofstream::app);
      if ( !sysfs_export.is_open() )
      {
         throw std::runtime_error("Unable to export PWM " + _id_str);
      }
      sysfs_export << _id_str;
      sysfs_export.close();
   }
}

PWM::~PWM()
{
   // setState(PWM::State::DISABLED);

   /* attempt to unexport */
   try
   {
      std::ofstream sysfs_unexport(_sysfsPath + "unexport", std::ofstream::app);
      if ( sysfs_unexport.is_open() )
      {
         sysfs_unexport << _id_str;
         sysfs_unexport.close();
      }
      else /* Do not throw exception in destructor! Effective C++ Item 8. */
      {
         cerr << "Unable to unexport PWM " + _id_str + "!" << endl;
         cerr << "This will prevent initialization of another PWM object for this PWM" << endl;
      }
   }
   catch (...)
   {
      cerr << "Exception caught in destructor for PWM " << _id_str << endl;
   }
}


void PWM::setState(const PWM::State &state)
{
   /* attempt to set disable by default */
   {
      std::ofstream sysfs_enable(
         _sysfsPath + "pwm" + _id_str + "/enable", std::ofstream::app);
      if ( !sysfs_enable.is_open() )
      {
         throw std::runtime_error("Unable to enable/disable PWM " + _id_str);
      }
      if ( state == PWM::State::DISABLED )      sysfs_enable << "0";
      else if ( state == PWM::State::ENABLED )  sysfs_enable << "1";
      sysfs_enable.close();
   }
   _state = state;
}


PWM::State PWM::getState(void)
{
   std::ifstream sysfs_state(_sysfsPath + "pwm" + _id_str + "/enable");
   if ( !sysfs_state.is_open() )
   {
      throw std::runtime_error("Unable to obtain enabled value for PWM " + _id_str);
   }

   const char value = sysfs_state.get();
   if ( !sysfs_state.good() )
   {
      throw std::runtime_error("Unable to obtain enabled value for PWM " + _id_str);
   }

   State status = PWM::State::DISABLED;
   if ( value == '1' )  status = PWM::State::ENABLED;

   return (status);
}


void PWM::setDuty(const PWM::Duty &duty_ns)
{
   std::ofstream sysfs_duty(_sysfsPath + "pwm" + _id_str + "/duty_cycle", std::ofstream::app);
   if ( !sysfs_duty.is_open() )
   {
      throw std::runtime_error("Unable to set duty value for PWM " + _id_str);
   }

   sysfs_duty << std::to_string(duty_ns);
   sysfs_duty.close();
   _duty_ns = duty_ns;
}


PWM::Duty PWM::getDuty(void)
{
   std::ifstream sysfs_duty(_sysfsPath + "pwm" + _id_str + "/duty_cycle");
   if ( !sysfs_duty.is_open() )
   {
      throw std::runtime_error("Unable to get duty value for PWM " + _id_str);
   }

   std::string value;
   std::getline(sysfs_duty, value);
   if ( !sysfs_duty.good() )
   {
      throw std::runtime_error("Unable to get duty value for PWM " + _id_str);
   }

   Duty val = std::strtoull(value.c_str(), NULL, 10);
   _duty_ns = val;
   return (val);
}

void PWM::setPeriod(const PWM::Period &value)
{
   std::ofstream sysfs_period(_sysfsPath + "pwm" + _id_str + "/period", std::ofstream::app);
   if ( !sysfs_period.is_open() )
   {
      throw std::runtime_error("Unable to set period value for PWM " + _id_str);
   }

   sysfs_period << std::to_string(value);
   sysfs_period.close();
   _period_ns = value;
}


PWM::Period PWM::getPeriod(void)
{
   std::ifstream sysfs_period(_sysfsPath + "pwm" + _id_str + "/period");
   if ( !sysfs_period.is_open() )
   {
      throw std::runtime_error("Unable to get period value for PWM " + _id_str);
   }

   std::string value;
   std::getline(sysfs_period, value);
   if ( !sysfs_period.good() )
   {
      throw std::runtime_error("Unable to get period value for PWM " + _id_str);
   }

   Period val = std::strtoull(value.c_str(), NULL, 10);
   _period_ns = val;
   return (val);
}

