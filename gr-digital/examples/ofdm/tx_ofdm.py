#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: OFDM Tx
# Description: Example of an OFDM Transmitter
# Generated: Tue Aug 27 16:07:02 2013
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import window
from gnuradio.digital.utils import tagged_streams
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import numpy
import random
import wx

class tx_ofdm(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="OFDM Tx")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.occupied_carriers = occupied_carriers = (range(-26, -21) + range(-20, -7) + range(-6, 0) + range(1, 7) + range(8, 21) + range(22, 27),)
		self.length_tag_name = length_tag_name = "packet_len"
		self.sync_word2 = sync_word2 = (0, 0, 0, 0, 0, 1, 1, -1.0, -1, 1.0, 1, 1.0, -1, -1.0, -1, 1.0, 1, -1.0, 1, 1.0, 1, -1.0, -1, -1.0, -1, 1.0, -1, 1.0, -1, 1.0, 1, -1.0, 0, 1.0, 1, -1.0, 1, 1.0, -1, -1.0, 1, -1.0, -1, -1.0, 1, 1.0, 1, -1.0, 1, 1.0, -1, 1.0, -1, -1.0, -1, 1.0, 1, -1.0, 0, 0, 0, 0, 0, 0)
		self.sync_word1 = sync_word1 = (0, 0, 0, 0, 0, 0, 0, -1.0, 0, 1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, -1.0, 0, -1.0, 0, 1.0, 0, 1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, -1.0, 0, -1.0, 0, -1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, -1.0, 0, 0, 0, 0, 0, 0)
		self.samp_rate = samp_rate = 100000
		self.rolloff = rolloff = 0
		self.pilot_symbols = pilot_symbols = ((1, 1, 1, -1,),)
		self.pilot_carriers = pilot_carriers = ((-21, -7, 7, 21,),)
		self.payload_mod = payload_mod = digital.constellation_qpsk()
		self.packet_len = packet_len = 96
		self.header_mod = header_mod = digital.constellation_bpsk()
		self.header_formatter = header_formatter = digital.packet_header_ofdm(occupied_carriers, 1, length_tag_name)
		self.fft_len = fft_len = 64

		##################################################
		# Blocks
		##################################################
		self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
			self.GetWin(),
			title="Scope Plot",
			sample_rate=samp_rate,
			v_scale=0,
			v_offset=0,
			t_scale=0,
			ac_couple=False,
			xy_mode=False,
			num_inputs=1,
			trig_mode=gr.gr_TRIG_MODE_AUTO,
			y_axis_label="Counts",
		)
		self.Add(self.wxgui_scopesink2_0.win)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.GetWin(),
			baseband_freq=0,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="FFT Plot",
			peak_hold=False,
		)
		self.Add(self.wxgui_fftsink2_0.win)
		self.fft_vxx_0 = fft.fft_vcc(fft_len, False, (), False, 1)
		self.digital_packet_headergenerator_bb_0 = digital.packet_headergenerator_bb(header_formatter.formatter())
		self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(fft_len, fft_len+fft_len/4, rolloff, length_tag_name)
		self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc(fft_len, occupied_carriers, pilot_carriers, pilot_symbols, length_tag_name)
		self.digital_crc32_bb_0 = digital.crc32_bb(False, length_tag_name)
		self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc((payload_mod.points()), 1)
		self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((header_mod.points()), 1)
		self.blocks_vector_source_x_1 = blocks.vector_source_c(tuple(numpy.array(sync_word1) * numpy.sqrt(2)) + sync_word2, True, fft_len, tagged_streams.make_lengthtags((2,), (0,), length_tag_name))
		self.blocks_vector_source_x_0 = blocks.vector_source_b(range(packet_len), True, 1, tagged_streams.make_lengthtags((packet_len,), (0,), length_tag_name))
		self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate)
		self.blocks_tagged_stream_mux_1 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*fft_len, length_tag_name)
		self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, length_tag_name)
		self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, payload_mod.bits_per_symbol(), length_tag_name, False)
		self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.05, ))

		##################################################
		# Connections
		##################################################
		self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
		self.connect((self.digital_packet_headergenerator_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
		self.connect((self.digital_crc32_bb_0, 0), (self.digital_packet_headergenerator_bb_0, 0))
		self.connect((self.digital_crc32_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))
		self.connect((self.blocks_vector_source_x_0, 0), (self.digital_crc32_bb_0, 0))
		self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
		self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))
		self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_multiply_const_vxx_0, 0))
		self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.blocks_tagged_stream_mux_1, 1))
		self.connect((self.blocks_tagged_stream_mux_1, 0), (self.fft_vxx_0, 0))
		self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))
		self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))
		self.connect((self.blocks_vector_source_x_1, 0), (self.blocks_tagged_stream_mux_1, 0))
		self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_throttle_0, 0))
		self.connect((self.blocks_throttle_0, 0), (self.wxgui_scopesink2_0, 0))


	def get_occupied_carriers(self):
		return self.occupied_carriers

	def set_occupied_carriers(self, occupied_carriers):
		self.occupied_carriers = occupied_carriers
		self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, 1, self.length_tag_name))

	def get_length_tag_name(self):
		return self.length_tag_name

	def set_length_tag_name(self, length_tag_name):
		self.length_tag_name = length_tag_name
		self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, 1, self.length_tag_name))

	def get_sync_word2(self):
		return self.sync_word2

	def set_sync_word2(self, sync_word2):
		self.sync_word2 = sync_word2

	def get_sync_word1(self):
		return self.sync_word1

	def set_sync_word1(self, sync_word1):
		self.sync_word1 = sync_word1

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.blocks_throttle_0.set_sample_rate(self.samp_rate)
		self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

	def get_rolloff(self):
		return self.rolloff

	def set_rolloff(self, rolloff):
		self.rolloff = rolloff

	def get_pilot_symbols(self):
		return self.pilot_symbols

	def set_pilot_symbols(self, pilot_symbols):
		self.pilot_symbols = pilot_symbols

	def get_pilot_carriers(self):
		return self.pilot_carriers

	def set_pilot_carriers(self, pilot_carriers):
		self.pilot_carriers = pilot_carriers

	def get_payload_mod(self):
		return self.payload_mod

	def set_payload_mod(self, payload_mod):
		self.payload_mod = payload_mod

	def get_packet_len(self):
		return self.packet_len

	def set_packet_len(self, packet_len):
		self.packet_len = packet_len

	def get_header_mod(self):
		return self.header_mod

	def set_header_mod(self, header_mod):
		self.header_mod = header_mod

	def get_header_formatter(self):
		return self.header_formatter

	def set_header_formatter(self, header_formatter):
		self.header_formatter = header_formatter

	def get_fft_len(self):
		return self.fft_len

	def set_fft_len(self, fft_len):
		self.fft_len = fft_len

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = tx_ofdm()
	tb.Run(True)

