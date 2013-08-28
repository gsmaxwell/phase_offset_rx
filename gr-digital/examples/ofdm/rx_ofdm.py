#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: OFDM Rx
# Description: Example of an OFDM receiver
# Generated: Tue Aug 27 16:06:42 2013
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import window
from gnuradio.digital.utils import tagged_streams
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx

class rx_ofdm(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="OFDM Rx")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.occupied_carriers = occupied_carriers = (range(-26, -21) + range(-20, -7) + range(-6, 0) + range(1, 7) + range(8, 21) + range(22, 27),)
		self.length_tag_name = length_tag_name = "frame_len"
		self.sync_word2 = sync_word2 = (0, 0, 0, 0, 0, 1, 1, -1.0, -1, 1.0, 1, 1.0, -1, -1.0, -1, 1.0, 1, -1.0, 1, 1.0, 1, -1.0, -1, -1.0, -1, 1.0, -1, 1.0, -1, 1.0, 1, -1.0, 0, 1.0, 1, -1.0, 1, 1.0, -1, -1.0, 1, -1.0, -1, -1.0, 1, 1.0, 1, -1.0, 1, 1.0, -1, 1.0, -1, -1.0, -1, 1.0, 1, -1.0, 0, 0, 0, 0, 0, 0)
		self.sync_word1 = sync_word1 = (0, 0, 0, 0, 0, 0, 0, -1.0, 0, 1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, -1.0, 0, -1.0, 0, 1.0, 0, 1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, -1.0, 0, -1.0, 0, -1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, 1.0, 0, -1.0, 0, 1.0, 0, -1.0, 0, 0, 0, 0, 0, 0)
		self.samp_rate = samp_rate = 3200000
		self.pilot_symbols = pilot_symbols = ((1, 1, 1, -1,),)
		self.pilot_carriers = pilot_carriers = ((-21, -7, 7, 21,),)
		self.payload_mod = payload_mod = digital.constellation_qpsk()
		self.header_mod = header_mod = digital.constellation_bpsk()
		self.header_formatter = header_formatter = digital.packet_header_ofdm(occupied_carriers, 1, length_tag_name)
		self.fft_len = fft_len = 64

		##################################################
		# Blocks
		##################################################
		self.gr_delay_0 = gr.delay(gr.sizeof_gr_complex*1, fft_len+fft_len/4)
		self.fft_vxx_0_0 = fft.fft_vcc(fft_len, True, (), True, 1)
		self.fft_vxx_0 = fft.fft_vcc(fft_len, True, (), True, 1)
		self.digital_packet_headerparser_b_0 = digital.packet_headerparser_b(header_formatter.formatter())
		self.digital_ofdm_sync_sc_cfb_0 = digital.ofdm_sync_sc_cfb(fft_len, fft_len/4, False)
		self.digital_ofdm_serializer_vcc_1 = digital.ofdm_serializer_vcc(fft_len, occupied_carriers, "length_tag_key", "", 1, "", True)
		self.digital_ofdm_serializer_vcc_0 = digital.ofdm_serializer_vcc(fft_len, occupied_carriers, length_tag_name, "", 0, "", True)
		self.digital_ofdm_frame_equalizer_vcvc_0_0 = digital.ofdm_frame_equalizer_vcvc(digital.ofdm_equalizer_simpledfe(fft_len, header_mod.base(), occupied_carriers, pilot_carriers, pilot_symbols).base(), fft_len/4, length_tag_name, True, 0)
		self.digital_ofdm_frame_equalizer_vcvc_0 = digital.ofdm_frame_equalizer_vcvc(digital.ofdm_equalizer_simpledfe(fft_len, header_mod.base(), occupied_carriers, pilot_carriers, pilot_symbols, 2).base(), fft_len/4, "length_tag_key", False, 0)
		self.digital_ofdm_chanest_vcvc_0 = digital.ofdm_chanest_vcvc((sync_word1), (sync_word2), 2, 0, -1, False)
		self.digital_header_payload_demux_0 = digital.header_payload_demux(3, fft_len, fft_len/4, length_tag_name, "", True, gr.sizeof_gr_complex)
		self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(header_mod.base())
		self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(payload_mod.base())
		self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate)
		self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_char*1, "Rx Packets")
		self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
		self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)
		self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(-2.0/fft_len)

		##################################################
		# Connections
		##################################################
		self.connect((self.digital_ofdm_frame_equalizer_vcvc_0_0, 0), (self.digital_ofdm_serializer_vcc_0, 0))
		self.connect((self.digital_header_payload_demux_0, 0), (self.fft_vxx_0, 0))
		self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_chanest_vcvc_0, 0))
		self.connect((self.digital_ofdm_chanest_vcvc_0, 0), (self.digital_ofdm_frame_equalizer_vcvc_0_0, 0))
		self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.digital_packet_headerparser_b_0, 0))
		self.connect((self.digital_ofdm_serializer_vcc_0, 0), (self.digital_constellation_decoder_cb_0_0, 0))
		self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_tag_debug_0, 0))
		self.connect((self.fft_vxx_0_0, 0), (self.digital_ofdm_frame_equalizer_vcvc_0, 0))
		self.connect((self.digital_ofdm_frame_equalizer_vcvc_0, 0), (self.digital_ofdm_serializer_vcc_1, 0))
		self.connect((self.digital_header_payload_demux_0, 1), (self.fft_vxx_0_0, 0))
		self.connect((self.digital_ofdm_serializer_vcc_1, 0), (self.digital_constellation_decoder_cb_0, 0))
		self.connect((self.blocks_throttle_0, 0), (self.digital_ofdm_sync_sc_cfb_0, 0))
		self.connect((self.blocks_throttle_0, 0), (self.gr_delay_0, 0))
		self.connect((self.analog_noise_source_x_0, 0), (self.blocks_throttle_0, 0))
		self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_xx_0, 0))
		self.connect((self.digital_ofdm_sync_sc_cfb_0, 0), (self.analog_frequency_modulator_fc_0, 0))
		self.connect((self.gr_delay_0, 0), (self.blocks_multiply_xx_0, 1))
		self.connect((self.digital_ofdm_sync_sc_cfb_0, 1), (self.digital_header_payload_demux_0, 1))
		self.connect((self.blocks_multiply_xx_0, 0), (self.digital_header_payload_demux_0, 0))

		##################################################
		# Asynch Message Connections
		##################################################
		self.msg_connect(self.digital_packet_headerparser_b_0, "header_data", self.digital_header_payload_demux_0, "header_data")

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
		self.analog_frequency_modulator_fc_0.set_sensitivity(-2.0/self.fft_len)
		self.gr_delay_0.set_delay(self.fft_len+self.fft_len/4)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = rx_ofdm()
	tb.Run(True)

