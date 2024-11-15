import numpy as np

def normalize(value, min_value, max_value):
    """Normalizes a value to the range [0, 1] given min and max values."""
    return (value - min_value) / (max_value - min_value) if max_value > min_value else 0

def find_closest_track(target_features, track_database):
    """
    Finds the track in the database with features closest to the target features,
    using normalized values for tempo, energy, and valence.
    
    Parameters:
        target_features (tuple): Tuple with target (tempo, energy, valence).
        track_database (dict): Dictionary where each key is a track ID and the value is a dictionary
                               with 'name' and 'features' (tempo, energy, valence) for each track.
    
    Returns:
        dict: The closest track's data, including 'track_id', 'name', and 'features' (tempo, energy, valence).
    """
    # Step 1: Find min and max for each feature across all tracks in the database
    tempos = [track_info['tempo'] for track_info in track_database.values()]
    energies = [track_info['energy'] for track_info in track_database.values()]
    valences = [track_info['valence'] for track_info in track_database.values()]
    
    min_tempo, max_tempo = min(tempos), max(tempos)
    min_energy, max_energy = min(energies), max(energies)
    min_valence, max_valence = min(valences), max(valences)
    
    # Step 2: Normalize target features
    target_vector = np.array([
        normalize(target_features[0], min_tempo, max_tempo),
        normalize(target_features[1], min_energy, max_energy),
        normalize(target_features[2], min_valence, max_valence)
    ])
    
    closest_track = None
    closest_distance = float('inf')
    
    # Step 3: Iterate through each track, normalize its features, and calculate distance
    for track_id, track_info in track_database.items():
        # Normalize each feature for the current track
        normalized_track_vector = np.array([
            normalize(track_info['tempo'], min_tempo, max_tempo),
            normalize(track_info['energy'], min_energy, max_energy),
            normalize(track_info['valence'], min_valence, max_valence)
        ])
        
        # Calculate Euclidean distance between the normalized target and track features
        distance = np.linalg.norm(target_vector - normalized_track_vector)
        
        # Update closest track if the current distance is smaller
        if distance < closest_distance:
            closest_distance = distance
            closest_track = {
                'track_id': track_id,
                'name': track_info['name'],
                'tempo': track_info['tempo'],
                'energy': track_info['energy'],
                'valence': track_info['valence'],
            }
    
    return closest_track