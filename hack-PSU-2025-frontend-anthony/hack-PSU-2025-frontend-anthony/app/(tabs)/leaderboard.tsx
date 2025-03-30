import { useState, useEffect, useCallback } from 'react';
import { useFocusEffect } from '@react-navigation/native';
import { StyleSheet, View, FlatList, TouchableOpacity } from 'react-native';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface RatingEntry {
  id: string;
  name: string;
  rating: number;
  timestamp: string;
}

export default function LeaderboardScreen() {
  const [ratings, setRatings] = useState<RatingEntry[]>([]);

  useFocusEffect(
    useCallback(() => {
      loadRatings();
    }, [])
  );

  const loadRatings = async () => {
    try {
      const savedRatings = await AsyncStorage.getItem('ratings');
      console.log('Loading ratings:', savedRatings); // Debug log
      if (savedRatings) {
        const parsedRatings = JSON.parse(savedRatings);
        console.log('Parsed ratings:', parsedRatings); // Debug log
        setRatings(parsedRatings);
      }
    } catch (error) {
      console.error('Error loading ratings:', error);
    }
  };

  const clearLeaderboard = async () => {
    try {
      await AsyncStorage.removeItem('ratings');
      setRatings([]); // Clear the state
    } catch (error) {
      console.error('Error clearing ratings:', error);
    }
  };

  return (
    <ThemedView style={styles.container}>
      <ThemedText style={styles.title}>Leaderboard</ThemedText>
      
      <TouchableOpacity 
        style={styles.clearButton}
        onPress={clearLeaderboard}
      >
        <ThemedText style={styles.clearButtonText}>Clear History</ThemedText>
      </TouchableOpacity>

      <FlatList
        data={ratings}
        renderItem={({ item }) => (
          <View style={styles.ratingItem}>
            <ThemedText style={styles.name}>{item.name}</ThemedText>
            <ThemedText style={styles.rating}>{item.rating.toFixed(1)}</ThemedText>
          </View>
        )}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.listContent}
      />
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#000',
  },
  title: {
    fontSize: 25,
    marginTop: 90,
    marginBottom: 20,
    textAlign: 'center',
    color: '#fff',
    fontWeight: 'bold',
  },
  listContent: {
    paddingBottom: 20,
  },
  ratingItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#111',
    borderRadius: 10,
    marginBottom: 10,
  },
  name: {
    fontSize: 18,
    color: '#fff',
  },
  rating: {
    fontSize: 24,
    color: '#A1CEDC',
    fontWeight: 'bold',
  },
  clearButton: {
    backgroundColor: '#FF4444',
    padding: 10,
    borderRadius: 8,
    marginBottom: 20,
    alignSelf: 'center',
  },
  clearButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
}); 