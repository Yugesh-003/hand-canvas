"""
Sound Effects Module for Temple Runner
Generates procedural sound effects using pygame
"""

import pygame
import numpy as np
import random
import math

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.generate_sounds()
        
    def generate_sounds(self):
        """Generate all game sound effects"""
        self.sounds['jump'] = self.generate_jump_sound()
        self.sounds['slide'] = self.generate_slide_sound()
        self.sounds['coin'] = self.generate_coin_sound()
        self.sounds['gem'] = self.generate_gem_sound()
        self.sounds['powerup'] = self.generate_powerup_sound()
        self.sounds['collision'] = self.generate_collision_sound()
        self.sounds['footstep'] = self.generate_footstep_sound()
        
    def generate_jump_sound(self):
        """Generate jump sound effect"""
        duration = 0.3
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Generate a rising tone
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = i / sample_rate
            freq = 200 + (t / duration) * 300  # Rising from 200Hz to 500Hz
            amplitude = 0.3 * (1 - t / duration)  # Fading out
            wave = amplitude * np.sin(2 * np.pi * freq * t)
            arr[i] = [wave, wave]
        
        # Convert to pygame sound
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def generate_slide_sound(self):
        """Generate slide sound effect"""
        duration = 0.4
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Generate a whoosh sound with noise
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = i / sample_rate
            # White noise filtered
            noise = random.uniform(-1, 1) * 0.2
            # Low frequency rumble
            rumble = 0.1 * np.sin(2 * np.pi * 80 * t)
            amplitude = 0.3 * (1 - t / duration)
            wave = amplitude * (noise + rumble)
            arr[i] = [wave, wave]
        
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def generate_coin_sound(self):
        """Generate coin collection sound"""
        duration = 0.2
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Generate a pleasant chime
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = i / sample_rate
            # Multiple harmonics for a bell-like sound
            freq1 = 800
            freq2 = 1200
            freq3 = 1600
            amplitude = 0.4 * np.exp(-t * 8)  # Exponential decay
            wave = amplitude * (
                0.5 * np.sin(2 * np.pi * freq1 * t) +
                0.3 * np.sin(2 * np.pi * freq2 * t) +
                0.2 * np.sin(2 * np.pi * freq3 * t)
            )
            arr[i] = [wave, wave]
        
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def generate_gem_sound(self):
        """Generate gem collection sound"""
        duration = 0.4
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Generate a magical sparkle sound
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = i / sample_rate
            # Rising and falling tones
            freq = 1000 + 500 * np.sin(2 * np.pi * 3 * t)
            amplitude = 0.3 * np.exp(-t * 3)
            wave = amplitude * np.sin(2 * np.pi * freq * t)
            # Add some sparkle with high frequency components
            sparkle = 0.1 * amplitude * np.sin(2 * np.pi * freq * 3 * t)
            arr[i] = [wave + sparkle, wave + sparkle]
        
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def generate_powerup_sound(self):
        """Generate power-up sound"""
        duration = 0.6
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Generate an ascending arpeggio
        arr = np.zeros((frames, 2))
        notes = [261.63, 329.63, 392.00, 523.25]  # C, E, G, C (major chord)
        note_duration = duration / len(notes)
        
        for note_idx, freq in enumerate(notes):
            start_frame = int(note_idx * note_duration * sample_rate)
            end_frame = int((note_idx + 1) * note_duration * sample_rate)
            
            for i in range(start_frame, min(end_frame, frames)):
                t = (i - start_frame) / sample_rate
                amplitude = 0.4 * (1 - t / note_duration)
                wave = amplitude * np.sin(2 * np.pi * freq * t)
                arr[i] = [wave, wave]
        
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def generate_collision_sound(self):
        """Generate collision/crash sound"""
        duration = 0.5
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Generate a crash sound with noise and low frequencies
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = i / sample_rate
            # Heavy noise component
            noise = random.uniform(-1, 1) * 0.5
            # Low frequency thump
            thump = 0.3 * np.sin(2 * np.pi * 60 * t)
            # Mid frequency crash
            crash = 0.2 * np.sin(2 * np.pi * 200 * t)
            amplitude = 0.8 * np.exp(-t * 4)
            wave = amplitude * (noise + thump + crash)
            arr[i] = [wave, wave]
        
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def generate_footstep_sound(self):
        """Generate footstep sound"""
        duration = 0.1
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Generate a short thud sound
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = i / sample_rate
            # Low frequency thud with some noise
            noise = random.uniform(-1, 1) * 0.1
            thud = 0.3 * np.sin(2 * np.pi * 120 * t)
            amplitude = 0.2 * (1 - t / duration)
            wave = amplitude * (thud + noise)
            arr[i] = [wave, wave]
        
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def play_sound(self, sound_name, volume=1.0):
        """Play a sound effect"""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            sound.set_volume(volume)
            sound.play()
    
    def stop_all_sounds(self):
        """Stop all playing sounds"""
        pygame.mixer.stop()

# Create global sound manager
sound_manager = SoundManager()

def play_jump_sound():
    sound_manager.play_sound('jump', 0.7)

def play_slide_sound():
    sound_manager.play_sound('slide', 0.6)

def play_coin_sound():
    sound_manager.play_sound('coin', 0.8)

def play_gem_sound():
    sound_manager.play_sound('gem', 0.9)

def play_powerup_sound():
    sound_manager.play_sound('powerup', 0.8)

def play_collision_sound():
    sound_manager.play_sound('collision', 1.0)

def play_footstep_sound():
    sound_manager.play_sound('footstep', 0.3)
