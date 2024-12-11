# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:57:22 2024

@author: Administrator
"""
import mido
import time
# from synthesizer import Player, Synthesizer, Waveform
import pygame
class MidiPlayer:
    def __init__(self,port="COM3",base_pitch=60):
        self.base_pitch = base_pitch
        self.port = mido.open_output(port)#this probably should be removed and added to the main code
        # Initialize pygame mixer
        pygame.mixer.init()
        # Initialize a MIDI file and track 
        self.midi_file = mido.MidiFile()
        self.midi_track = mido.MidiTrack()
        self.midi_file.tracks.append(self.midi_track)
        
    def Live_Midi(self,distance,amplitude,width):
        pass


    def send_midi_message(self, pitch, velocity=127, pitchbend=0, dt=1):

        #dt is in seconds, I should convert it to ticks, this will later be modified
        dt=500*dt
        
        note_on = mido.Message('note_on', note=self.base_pitch+pitch, velocity=velocity,time=0)

        # Send and Record note_on message
        self.port.send(note_on)
        self.midi_track.append(note_on) 
        
        if pitchbend!=0:
            pitchbend_message = mido.Message('pitchwheel', pitch=pitchbend)
            
            #Send and Record Pitch_Bend message
            self.port.send(pitchbend_message)
            self.midi_track.append(pitchbend_message) 

        note_off = mido.Message('note_off', note=self.base_pitch+pitch, velocity=velocity,time=dt)

        # Send and Record note_off message
        self.port.send(note_off)
        self.midi_track.append(note_off) 
        
        return 0
    
    def save_midi_file(self, filename): 
        self.midi_file.save(filename) 
    
    def Synthesize_midi_file(self, filename):
        """Load and play the MIDI file, and stop on pressing 'q'."""
        
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        pygame.time.Clock().tick(10)
        
        k=str(input("Press q to stop playing"))
        if k=="q":
            pygame.mixer.music.stop()
        return 0

            
    def Live_Synthesizer(self, pitch, velocity, pitchbend, dt):
        pass