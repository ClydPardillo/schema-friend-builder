
// Minimal React Native app that connects to your FastAPI backend
import React, { useState } from "react";
import { View, Text, TextInput, Button, SafeAreaView, Alert } from "react-native";

export default function App() {
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");
  const [token, setToken] = useState("");
  const [message, setMessage] = useState("");

  async function login() {
    setMessage("Logging in...");
    try {
      const res = await fetch("http://localhost:8000/users/login", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email, password: pw })
      });
      const data = await res.json();
      if (data.success && data.data?.access_token) {
        setToken(data.data.access_token);
        setMessage("Login successful!");
      } else {
        setMessage("Login failed: " + data.message);
      }
    } catch (e) {
      setMessage("Network error");
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
      <Button title="Login" onPress={login} />
      {token !== "" && <Text>Token: {token.slice(0, 16)}...</Text>}
      <Text style={{ marginTop: 16 }}>{message}</Text>
    </SafeAreaView>
  );
}
