import { useEffect } from "react";
import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import * as Font from "expo-font";
import Home from "./screens/Home";
import Profile from "./screens/Profile";
import Tabs from "./components/tabs";

export default function App() {
  async function loadFonts() {
    await Font.loadAsync({
      RedHatMedium: require("./assets/fonts/RedHatMedium.ttf"),
      RedHatBold: require("./assets/fonts/RedHatBold.ttf"),
      RedHatRegular: require("./assets/fonts/RedHatRegular.ttf"),
    });
  }
  useEffect(() => {
    loadFonts();
  }, []);

  return (
    <NavigationContainer
      tabBarStyle={{
        showLabel: false,
        tabBarStyle: {
          backgroundColor: "#fff",
          position: "fixed",
          bottom: 20,
          marginLeft: 20,
          marginRight: 20,
          elevation: 2,
          borderRadius: 40,
          safeAreaInsets: {
            bottom: 0,
          },
        },
      }}
    >
      <Tabs />
    </NavigationContainer>
  );
}
