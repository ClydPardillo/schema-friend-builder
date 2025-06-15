// Minimal React Native app that connects to your FastAPI backend
import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, SafeAreaView, Alert, TouchableOpacity, FlatList } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import axios from "axios";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

function LoginScreen({ navigation }) {
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function login() {
    setLoading(true);
    setMessage("Logging in...");
    try {
      const res = await axios.post("http://localhost:8000/users/login", {
        email, password: pw
      });
      if (res.data.success && res.data.data?.access_token) {
        await AsyncStorage.setItem("access_token", res.data.data.access_token);
        setMessage("Login successful!");
        navigation.replace("Home");
      } else {
        setMessage("Login failed: " + res.data.message);
      }
    } catch (e) {
      setMessage("Network error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <SafeAreaView style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      <Text style={{ fontSize: 24, marginBottom: 24 }}>ClearCause Mobile Login</Text>
      <TextInput
        placeholder="Email"
        style={{ borderWidth: 1, marginBottom: 8, width: 240, padding: 8 }}
        onChangeText={setEmail}
        value={email}
        autoCapitalize="none"
      />
      <TextInput
        placeholder="Password"
        secureTextEntry
        style={{ borderWidth: 1, marginBottom: 8, width: 240, padding: 8 }}
        onChangeText={setPw}
        value={pw}
        autoCapitalize="none"
      />
      <Button title={loading ? "Loading..." : "Login"} onPress={login} disabled={loading} />
      {message !== "" && <Text style={{ marginTop: 16 }}>{message}</Text>}
    </SafeAreaView>
  );
}

function HomeScreen({ navigation }) {
  const [token, setToken] = useState(null);
  useEffect(() => {
    AsyncStorage.getItem("access_token").then(setToken);
  }, []);
  return (
    <SafeAreaView style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      <Text style={{ fontSize: 20, marginBottom: 24 }}>Welcome Home!</Text>
      {token && <Text style={{ marginVertical: 8 }}>Token saved.</Text>}
      <Button title="Campaigns" onPress={() => navigation.navigate("Campaigns")} />
      <Button title="Logout" onPress={async () => {
        await AsyncStorage.removeItem("access_token");
        navigation.replace("Login");
      }} />
    </SafeAreaView>
  );
}

function CampaignListScreen() {
  const [campaigns, setCampaigns] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  async function fetchCampaigns() {
    setLoading(true);
    try {
      const token = await AsyncStorage.getItem("access_token");
      const res = await axios.get("http://localhost:8000/campaigns/");
      setCampaigns(res.data.data);
      if (token) {
        const favRes = await axios.get("http://localhost:8000/favorites", {
          headers: { Authorization: `Bearer ${token}` }
        });
        setFavorites(favRes.data.favorites.map(f => f.campaign_id));
      }
    } catch (e) {
      Alert.alert("Failed to fetch campaigns.");
    } finally {
      setLoading(false);
    }
  }

  async function toggleFavorite(campaignId) {
    const token = await AsyncStorage.getItem("access_token");
    if (!token) return Alert.alert("Not logged in");
    if (favorites.includes(campaignId)) {
      await axios.delete(`http://localhost:8000/favorites/${campaignId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
    } else {
      await axios.post("http://localhost:8000/favorites", { campaign_id: campaignId }, {
        headers: { Authorization: `Bearer ${token}` }
      });
    }
    fetchCampaigns();
  }

  useEffect(() => {
    fetchCampaigns();
  }, []);

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <Text style={{ fontSize: 20, margin: 16 }}>Campaigns</Text>
      {loading && <Text>Loading...</Text>}
      <FlatList
        data={campaigns}
        keyExtractor={c => c.id}
        renderItem={({ item }) => (
          <View style={{ padding: 16, borderBottomWidth: 1 }}>
            <Text style={{ fontWeight: "bold" }}>{item.title}</Text>
            <Text>Status: {item.status}</Text>
            <Button
              title={favorites.includes(item.id) ? "Unfavorite" : "Favorite"}
              onPress={() => toggleFavorite(item.id)}
            />
          </View>
        )}
      />
    </SafeAreaView>
  );
}

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login" screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Campaigns" component={CampaignListScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
