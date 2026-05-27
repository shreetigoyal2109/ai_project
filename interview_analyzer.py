"""
FastAPI Audio Analysis Service
Complete port of Flask audio analyzer with all key features
"""

import librosa
import numpy as np
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class FastAPIAudioAnalyzer:
    """Complete audio analysis service ported from Flask"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.filler_words = {
            'um', 'uh', 'er', 'ah', 'like', 'you know', 'so', 'well', 
            'actually', 'basically', 'literally', 'kind of', 'sort of'
        }
    
    def analyze_audio(self, audio_path: str) -> Dict[str, Any]:
        """Main analysis method - comprehensive audio analysis"""
        try:
            # Load audio with robust fallback methods
            y, sr_rate = self._load_audio_robust(audio_path)
            duration = len(y) / sr_rate if len(y) > 0 else 0
            
            logger.info(f"Audio loaded: duration={duration:.2f}s, sample_rate={sr_rate}")
            
            results = {
                'basic_info': {},
                'speech_analysis': {},
                'pitch_analysis': {},
                'tone_analysis': {},
                'quality_metrics': {},
                'spectral_features': {}
            }
            
            # Run all analysis components with error handling
            try:
                results['basic_info'] = self._get_basic_info(audio_path, duration, sr_rate)
            except Exception as e:
                results['basic_info'] = {'error': str(e)}
            
            try:
                results['speech_analysis'] = self._analyze_speech(audio_path, y, sr_rate)
            except Exception as e:
                results['speech_analysis'] = {'error': str(e)}
            
            try:
                results['pitch_analysis'] = self._analyze_pitch_robust(y, sr_rate)
            except Exception as e:
                results['pitch_analysis'] = {'error': str(e)}
            
            try:
                results['tone_analysis'] = self._analyze_tone(y, sr_rate)
            except Exception as e:
                results['tone_analysis'] = {'error': str(e)}
            
            try:
                results['quality_metrics'] = self._analyze_quality(y, sr_rate)
            except Exception as e:
                results['quality_metrics'] = {'error': str(e)}
            
            try:
                results['spectral_features'] = self._analyze_spectral_features(y, sr_rate)
            except Exception as e:
                results['spectral_features'] = {'error': str(e)}
            
            return results
            
        except Exception as e:
            logger.error(f"Critical audio analysis error: {e}")
            raise Exception(f"Audio analysis failed: {str(e)}")
    
    def _load_audio_robust(self, audio_path: str):
        """Load audio with multiple fallback methods for better compatibility"""
        try:
            # Try librosa first
            y, sr = librosa.load(audio_path, sr=None)
            if len(y) > 0:
                return y, sr
        except Exception as e:
            logger.warning(f"Librosa loading failed: {e}")
        
        try:
            # Try with pydub as fallback
            audio = AudioSegment.from_file(audio_path)
            samples = np.array(audio.get_array_of_samples())
            if audio.channels == 2:
                samples = samples.reshape((-1, 2))
                samples = samples.mean(axis=1)  # Convert stereo to mono
            samples = samples.astype(np.float32) / (2**15)
            return samples, audio.frame_rate
        except Exception as e:
            raise Exception(f"Could not load audio file: {e}")
    
    def _get_basic_info(self, audio_path: str, duration: float, sr_rate: int):
        """Get basic file information"""
        file_size = os.path.getsize(audio_path)
        return {
            'duration_seconds': round(duration, 2),
            'duration_minutes': round(duration / 60, 2),
            'sample_rate': sr_rate,
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'format': os.path.splitext(audio_path)[1].lower()
        }
    
    def _analyze_speech(self, audio_path: str, y: np.ndarray, sr_rate: int):
        """Analyze speech content and calculate words per minute"""
        try:
            duration_seconds = len(y) / sr_rate
            duration_minutes = duration_seconds / 60
            
            # Convert to WAV for speech recognition
            temp_wav_path = None
            try:
                audio = AudioSegment.from_file(audio_path)
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                    temp_wav_path = temp_wav.name
                    audio.export(temp_wav_path, format="wav")
                
                # Perform speech recognition
                with sr.AudioFile(temp_wav_path) as source:
                    audio_data = self.recognizer.record(source)
                    transcribed_text = self.recognizer.recognize_google(audio_data)
                
                # Calculate speech metrics
                words = transcribed_text.split()
                word_count = len(words)
                character_count = len(transcribed_text)
                
                words_per_minute = (word_count / duration_minutes) if duration_minutes > 0 else 0
                words_per_second = (word_count / duration_seconds) if duration_seconds > 0 else 0
                average_word_length = (character_count / word_count) if word_count > 0 else 0
                
                # Detect filler words
                filler_count = sum(1 for word in words if word.lower() in self.filler_words)
                filler_percentage = (filler_count / word_count * 100) if word_count > 0 else 0
                
                return {
                    'transcribed_text': transcribed_text,
                    'word_count': word_count,
                    'character_count': character_count,
                    'words_per_minute': round(words_per_minute, 2),
                    'words_per_second': round(words_per_second, 2),
                    'average_word_length': round(average_word_length, 2),
                    'filler_words_count': filler_count,
                    'filler_words_percentage': round(filler_percentage, 2),
                    'speech_detected': True,
                    'confidence_score': 'High'
                }
                
            finally:
                if temp_wav_path and os.path.exists(temp_wav_path):
                    os.unlink(temp_wav_path)
                    
        except sr.UnknownValueError:
            return self._provide_basic_speech_metrics(duration_seconds, duration_minutes)
        except Exception as e:
            return self._provide_basic_speech_metrics(duration_seconds, duration_minutes, str(e))
    
    def _provide_basic_speech_metrics(self, duration_seconds, duration_minutes, error_msg=None):
        """Provide basic speech metrics when recognition fails"""
        return {
            'transcribed_text': '',
            'word_count': 0,
            'character_count': 0,
            'words_per_minute': 0,
            'words_per_second': 0,
            'average_word_length': 0,
            'filler_words_count': 0,
            'filler_words_percentage': 0,
            'speech_detected': False,
            'confidence_score': 'Low',
            'error': error_msg or 'Could not understand audio - no speech detected'
        }
    
    def _analyze_pitch_robust(self, y: np.ndarray, sr_rate: int):
        """Analyze pitch characteristics using multiple methods for robustness"""
        try:
            # Method 1: Try librosa fundamental frequency estimation
            try:
                f0 = librosa.yin(y, fmin=75, fmax=600, sr=sr_rate)
                f0_clean = f0[f0 > 0]  # Remove unvoiced segments
                
                if len(f0_clean) > 0:
                    return {
                        'mean_pitch_hz': round(float(np.mean(f0_clean)), 2),
                        'median_pitch_hz': round(float(np.median(f0_clean)), 2),
                        'min_pitch_hz': round(float(np.min(f0_clean)), 2),
                        'max_pitch_hz': round(float(np.max(f0_clean)), 2),
                        'pitch_std_dev': round(float(np.std(f0_clean)), 2),
                        'pitch_range_hz': round(float(np.max(f0_clean) - np.min(f0_clean)), 2),
                        'voiced_percentage': round(len(f0_clean) / len(f0) * 100, 2),
                        'pitch_stability': round(1 / (1 + np.std(f0_clean)), 3),
                        'method': 'librosa_yin'
                    }
            except Exception as e:
                logger.warning(f"Librosa pitch analysis failed: {e}")
            
            # Fallback: Basic autocorrelation method
            try:
                correlation = np.correlate(y, y, mode='full')
                correlation = correlation[len(correlation)//2:]
                
                min_period = int(sr_rate / 600)  # Max 600 Hz
                max_period = int(sr_rate / 75)   # Min 75 Hz
                
                if max_period < len(correlation):
                    correlation_segment = correlation[min_period:max_period]
                    if len(correlation_segment) > 0:
                        peak_idx = np.argmax(correlation_segment) + min_period
                        fundamental_freq = sr_rate / peak_idx
                        
                        return {
                            'mean_pitch_hz': round(fundamental_freq, 2),
                            'median_pitch_hz': round(fundamental_freq, 2),
                            'min_pitch_hz': round(fundamental_freq * 0.8, 2),
                            'max_pitch_hz': round(fundamental_freq * 1.2, 2),
                            'pitch_std_dev': round(fundamental_freq * 0.1, 2),
                            'pitch_range_hz': round(fundamental_freq * 0.4, 2),
                            'voiced_percentage': 50.0,
                            'pitch_stability': 0.5,
                            'method': 'autocorrelation_fallback'
                        }
            except Exception as e:
                logger.warning(f"Autocorrelation pitch analysis failed: {e}")
            
            # If all methods fail, return default values
            return {
                'mean_pitch_hz': 0,
                'median_pitch_hz': 0,
                'min_pitch_hz': 0,
                'max_pitch_hz': 0,
                'pitch_std_dev': 0,
                'pitch_range_hz': 0,
                'voiced_percentage': 0,
                'pitch_stability': 0,
                'method': 'none',
                'error': 'All pitch analysis methods failed'
            }
            
        except Exception as e:
            return {
                'error': f'Pitch analysis failed: {str(e)}'
            }
    
    def _analyze_tone(self, y: np.ndarray, sr_rate: int):
        """Analyze tone and timbre characteristics"""
        try:
            # Spectral centroid (brightness)
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr_rate)[0]
            brightness_score = np.mean(spectral_centroids)
            
            # Zero crossing rate (roughness indicator)
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            roughness_score = np.mean(zcr)
            
            # MFCC features for timbre
            mfccs = librosa.feature.mfcc(y=y, sr=sr_rate, n_mfcc=13)
            mfcc_mean = np.mean(mfccs, axis=1)
            
            return {
                'brightness_score': round(float(brightness_score), 2),
                'roughness_score': round(float(roughness_score), 4),
                'spectral_centroid_mean': round(float(brightness_score), 2),
                'zero_crossing_rate_mean': round(float(roughness_score), 4),
                'mfcc_features': [round(float(x), 3) for x in mfcc_mean[:5]],  # First 5 MFCCs
                'timbre_complexity': round(float(np.std(mfcc_mean)), 3)
            }
            
        except Exception as e:
            return {
                'error': f'Tone analysis failed: {str(e)}'
            }
    
    def _analyze_quality(self, y: np.ndarray, sr_rate: int):
        """Analyze audio quality metrics"""
        try:
            # Calculate RMS energy
            rms = librosa.feature.rms(y=y)
            
            # Calculate dynamic range
            dynamic_range = np.max(y) - np.min(y)
            
            # Calculate signal-to-noise ratio estimate
            frame_length = 2048
            hop_length = 512
            frames = librosa.util.frame(y, frame_length=frame_length, hop_length=hop_length)
            frame_energies = np.sum(frames**2, axis=0)
            
            # Estimate SNR (simple approach)
            if len(frame_energies) > 0:
                signal_energy = np.max(frame_energies)
                noise_energy = np.min(frame_energies)
                snr_estimate = 10 * np.log10(signal_energy / noise_energy) if noise_energy > 0 else float('inf')
            else:
                snr_estimate = 0
            
            return {
                'rms_energy_mean': round(float(np.mean(rms)), 4),
                'rms_energy_std': round(float(np.std(rms)), 4),
                'dynamic_range': round(float(dynamic_range), 4),
                'snr_estimate_db': round(float(snr_estimate), 2) if snr_estimate != float('inf') else 'High',
                'peak_amplitude': round(float(np.max(np.abs(y))), 4),
                'clipping_detected': bool(np.any(np.abs(y) >= 0.99))
            }
            
        except Exception as e:
            return {
                'error': f'Quality analysis failed: {str(e)}'
            }
    
    def _analyze_spectral_features(self, y: np.ndarray, sr_rate: int):
        """Extract additional spectral features"""
        try:
            # Spectral bandwidth
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr_rate)
            
            # Spectral contrast
            spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr_rate)
            
            # Spectral flatness
            spectral_flatness = librosa.feature.spectral_flatness(y=y)
            
            # Spectral rolloff
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr_rate)
            
            return {
                'spectral_bandwidth_mean': round(float(np.mean(spectral_bandwidth)), 2),
                'spectral_bandwidth_std': round(float(np.std(spectral_bandwidth)), 2),
                'spectral_contrast_mean': [round(float(np.mean(contrast)), 3) for contrast in spectral_contrast],
                'spectral_flatness_mean': round(float(np.mean(spectral_flatness)), 4),
                'spectral_flatness_std': round(float(np.std(spectral_flatness)), 4),
                'spectral_rolloff_mean': round(float(np.mean(spectral_rolloff)), 2),
                'spectral_rolloff_std': round(float(np.std(spectral_rolloff)), 2)
            }
            
        except Exception as e:
            return {
                'error': f'Spectral analysis failed: {str(e)}'
            }

# Create global instance
fastapi_audio_analyzer = FastAPIAudioAnalyzer()

def get_audio_analyzer():
    """Get the global audio analyzer instance"""
    return fastapi_audio_analyzer