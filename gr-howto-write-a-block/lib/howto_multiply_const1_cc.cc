/* -*- c++ -*- */
/*
 * Copyright 2012 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <howto_multiply_const1_cc.h>
#include <gr_io_signature.h>
#include <volk/volk.h>
#include <gr_fxpt.h>//cyjadd
#include <math.h>//cyjadd
#include <boost/math/special_functions/trunc.hpp>//cyjadd
#include <iostream>//cyjadd
howto_multiply_const1_cc_sptr
howto_make_multiply_const1_cc (gr_complex k, size_t vlen)
{
  return gnuradio::get_initial_sptr(new howto_multiply_const1_cc (k, vlen));
}

howto_multiply_const1_cc::howto_multiply_const1_cc (gr_complex k, size_t vlen)
  : gr_sync_block ("multiply_const1_cc",
		   gr_make_io_signature (1, 1, sizeof (gr_complex)*vlen),
		   gr_make_io_signature (1, 1, sizeof (gr_complex)*vlen)),
    d_k(k), d_vlen(vlen)
{
  const int alignment_multiple =
    volk_get_alignment() / sizeof(gr_complex);
  set_alignment(std::max(1,alignment_multiple));
}

gr_complex
howto_multiply_const1_cc::k() const
{
  return d_k;
}

void
howto_multiply_const1_cc::set_k(gr_complex k)
{
  d_k = k;
}

int
howto_multiply_const1_cc::work (int noutput_items,
			    gr_vector_const_void_star &input_items,
			    gr_vector_void_star &output_items)
{
  const gr_complex *in = (const gr_complex *) input_items[0];
  gr_complex *out = (gr_complex *) output_items[0];
  int noi = d_vlen*noutput_items;
  double phase_const = -2*M_PI*1000/(2*1000000);//cyjadd
  double d_phase;//cyjadd
  
  for (int i = 0; i < noutput_items; i++){
     d_phase = phase_const*i;

    /*while (d_phase > (float)(M_PI))
      d_phase -= (float)(2.0 * M_PI);
    while (d_phase < (float)(-M_PI))
      d_phase += (float)(2.0 * M_PI);*/
    float oi, oq;

    gr_int32 angle = gr_fxpt::float_to_fixed (d_phase);
    gr_fxpt::sincos (angle, &oq, &oi);
    //std::cout<<"oi:"<<oi<<"oq:"<<oq<<"mag:"<<sqrt(pow(oq, 2)+pow(oi, 2))<<std::endl;
    //out[i] =in[i]* gr_complex (oi, oq);
    out[i] =in[i];
   }//cyjadd
 

  return noutput_items;
}



