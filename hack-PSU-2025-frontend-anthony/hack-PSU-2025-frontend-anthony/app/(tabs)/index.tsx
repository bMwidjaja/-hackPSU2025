import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useState, useRef, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Modal, TextInput } from 'react-native';
import * as MediaLibrary from 'expo-media-library';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface RatingEntry {
  id: string;
  name: string;
  rating: number;
  timestamp: string;
}

export default function HomeScreen() {
  const [type, setType] = useState<CameraType>('front');
  const [permission, requestPermission] = useCameraPermissions();
  const [showNameModal, setShowNameModal] = useState(false);
  const [showMessage, setShowMessage] = useState(false);
  const [name, setName] = useState('');
  const [tempPhotoUri, setTempPhotoUri] = useState<string | null>(null);
  const cameraRef = useRef<any>(null);
  const router = useRouter();
  const [showGuide, setShowGuide] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowGuide(false);
    }, 5000);

    return () => clearTimeout(timer);
  }, []);

  const takePicture = async () => {
    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePictureAsync({
          quality: 1,
          base64: true,
        });
        setTempPhotoUri(photo.uri);
        setShowNameModal(true);
      } catch (error) {
        console.error('Error taking picture:', error);
        alert('Failed to take picture. Please try again.');
      }
    }
  };

  const handleNameSubmit = async () => {
    if (tempPhotoUri && name.trim()) {
      try {
        // Save photo to camera roll
        await MediaLibrary.saveToLibraryAsync(tempPhotoUri);

        // Create mock backend response
        const newRating: RatingEntry = {
          id: Date.now().toString(),
          name: name,
          rating: 1,
          timestamp: new Date().toISOString()
        };

        // Get existing ratings
        const existingRatingsString = await AsyncStorage.getItem('ratings');
        console.log('Existing ratings:', existingRatingsString); // Debug log

        const existingRatings: RatingEntry[] = existingRatingsString 
          ? JSON.parse(existingRatingsString) 
          : [];

        // Add new rating
        const updatedRatings = [...existingRatings, newRating];
        console.log('Updated ratings:', updatedRatings); // Debug log

        // Save updated ratings
        await AsyncStorage.setItem('ratings', JSON.stringify(updatedRatings));
        console.log('Saved to AsyncStorage'); // Debug log

        setShowNameModal(false);
        setShowMessage(true);
        
        setTimeout(() => {
          setShowMessage(false);
          router.push('/leaderboard');
          setName('');
          setTempPhotoUri(null);
        }, 1000);

      } catch (error) {
        console.error('Error:', error);
        alert('Failed to save photo. Please try again.');
      }
    }
  };

  // Helper functions to manage ratings storage
  async function getRatings(): Promise<RatingEntry[]> {
    try {
      const ratings = await AsyncStorage.getItem('ratings');
      return ratings ? JSON.parse(ratings) : [];
    } catch (error) {
      console.error('Error getting ratings:', error);
      return [];
    }
  }

  async function saveRatings(ratings: RatingEntry[]) {
    try {
      await AsyncStorage.setItem('ratings', JSON.stringify(ratings));
    } catch (error) {
      console.error('Error saving ratings:', error);
    }
  }

  if (!permission) {
    return <View style={styles.container}><Text>Requesting camera permission...</Text></View>;
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text>No access to camera</Text>
        <TouchableOpacity style={styles.button} onPress={requestPermission}>
          <Text style={styles.text}>Grant Permission</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <CameraView
        ref={cameraRef}
        style={styles.camera}
        facing={type}
      >
        {showGuide && (
          <View style={styles.guideContainer}>
            <Text style={styles.guideText}>Center Your Whole Face</Text>
          </View>
        )}

        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={styles.button}
            onPress={() => setType(type === 'back' ? 'front' : 'back')}
          >
            <Text style={styles.text}>Flip Camera</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.button}
            onPress={takePicture}
          >
            <Text style={styles.text}>Take Photo</Text>
          </TouchableOpacity>
        </View>
      </CameraView>

      <Modal
        visible={showNameModal}
        transparent={true}
        animationType="slide"
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Enter your name</Text>
            <TextInput
              style={styles.input}
              value={name}
              onChangeText={setName}
              placeholder="Your name"
              placeholderTextColor="#666"
            />
            <TouchableOpacity
              style={styles.submitButton}
              onPress={handleNameSubmit}
            >
              <Text style={styles.submitButtonText}>Submit</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      {showMessage && (
        <View style={styles.messageContainer}>
          <Text style={styles.messageText}>Photo Saved!</Text>
          <Text style={styles.nameText}>{name}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    position: 'absolute',
    bottom: 100,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: 20,
  },
  button: {
    backgroundColor: '#A1CEDC',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    flex: 0.45,
  },
  text: {
    fontSize: 16,
    color: '#000',
    fontWeight: 'bold',
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  modalContent: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
    width: '80%',
    alignItems: 'center',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#000',
  },
  input: {
    width: '100%',
    height: 40,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    paddingHorizontal: 10,
    marginBottom: 15,
    color: '#000',
  },
  submitButton: {
    backgroundColor: '#A1CEDC',
    padding: 12,
    borderRadius: 8,
    width: '100%',
    alignItems: 'center',
  },
  submitButtonText: {
    color: '#000',
    fontWeight: 'bold',
    fontSize: 16,
  },
  messageContainer: {
    position: 'absolute',
    top: '40%',
    alignSelf: 'center',
    backgroundColor: '#000',
    padding: 20,
    borderRadius: 15,
    alignItems: 'center',
  },
  messageText: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  nameText: {
    color: '#A1CEDC',
    fontSize: 18,
    marginTop: 10,
    textAlign: 'center',
  },
  guideContainer: {
    position: 'absolute',
    top: 50,
    left: 0,
    right: 0,
    alignItems: 'center',
  },
  guideText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '500',
    fontFamily: 'Avenir',
    backgroundColor: '#000',
    padding: 8,
    borderRadius: 8,
  },
});

//ctrl + l is ai guy