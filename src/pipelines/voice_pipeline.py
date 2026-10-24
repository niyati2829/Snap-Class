import numpy as np 
import io
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    from resemblyzer import VoiceEncoder
    return VoiceEncoder()


def get_voice_embedding(audio_data):
    """
    Extracts a 256-dimensional voice embedding vector from raw audio bytes or a file-like object.
    Returns: list of floats (embedding) on success, or None on failure.
    """
    if audio_data is None:
        return None

    try:
        from resemblyzer import preprocess_wav
        import librosa

        # Extract bytes from various possible input types (bytes, BytesIO, UploadedFile)
        if isinstance(audio_data, (bytes, bytearray)):
            raw_bytes = bytes(audio_data)
        elif hasattr(audio_data, 'getvalue'):
            raw_bytes = audio_data.getvalue()
        elif hasattr(audio_data, 'read'):
            raw_bytes = audio_data.read()
        else:
            raw_bytes = bytes(audio_data)

        if not raw_bytes or len(raw_bytes) < 500:
            st.warning("Audio recording too short. Please speak for at least 1-2 seconds.")
            return None

        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(raw_bytes), sr=16000)

        # Check for minimum length (at least 0.25 seconds)
        if len(audio) < sr * 0.25:
            st.warning("Audio is too brief. Please speak a complete sentence.")
            return None

        # Check for volume / signal presence (RMS energy)
        rms = np.sqrt(np.mean(audio ** 2))
        if rms < 0.0005:
            st.warning("Audio volume is too low or silent. Please speak closer to your microphone.")
            return None

        # Preprocess with silence trimming (VAD)
        try:
            wav = preprocess_wav(audio)
        except Exception:
            wav = audio

        # If silence trimming removed all frames (quiet speaker or noise), fallback to un-trimmed audio
        if len(wav) < sr * 0.2:
            wav = audio

        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        print(f"Voice embedding extraction error: {e}")
        st.warning(f"Voice recognition note: {e}")
        return None


def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    new_emb_np = np.array(new_embedding)
    norm = np.linalg.norm(new_emb_np)
    if norm > 0:
        new_emb_np = new_emb_np / norm

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            stored_emb_np = np.array(stored_embedding)
            s_norm = np.linalg.norm(stored_emb_np)
            if s_norm > 0:
                stored_emb_np = stored_emb_np / s_norm
            similarity = float(np.dot(new_emb_np, stored_emb_np))
            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    try:
        from resemblyzer import preprocess_wav
        import librosa

        if hasattr(audio_bytes, 'getvalue'):
            raw_bytes = audio_bytes.getvalue()
        elif hasattr(audio_bytes, 'read'):
            raw_bytes = audio_bytes.read()
        else:
            raw_bytes = bytes(audio_bytes)

        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(raw_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        identified_results = {}

        if len(segments) == 0:
            # Fallback to entire audio if no silence split detected
            segments = [(0, len(audio))]

        for start, end in segments:
            if (end - start) < sr * 0.4:
                continue # Skip segments shorter than 0.4s
            segment_audio = audio[start:end]
            try:
                wav = preprocess_wav(segment_audio)
                if len(wav) == 0:
                    wav = segment_audio
            except Exception:
                wav = segment_audio

            embedding = encoder.embed_utterance(wav)
            sid, score = identify_speaker(embedding.tolist(), candidates_dict, threshold=threshold)
            if sid is not None:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = round(score, 2)

        return identified_results
    except Exception as e:
        print(f"Error in process_bulk_audio: {e}")
        return {}