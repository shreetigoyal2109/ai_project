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
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.filler_words = {
            'um', 'uh', 'er', 'ah', 'like', 'you know', 'so', 'well', 
            'actually', 'basically', 'literally', 'kind of', 'sort of'
        }
    
    def analyze_audio(self, audio_path: str) -> Dict[str, Any]:
        try:
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

fastapi_audio_analyzer = FastAPIAudioAnalyzer()

def get_audio_analyzer():
    return fastapi_audio_analyzer
