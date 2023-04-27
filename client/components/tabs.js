import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import Home from "../screens/Home";
import Profile from "../screens/Profile";
import VideoScreen from "../screens/Video";
const Tab = createBottomTabNavigator();
const Tabs = ({ fontsLoaded }) => {
  return (
    <>
      {!fontsLoaded ? null : (
        <Tab.Navigator
          screenOptions={{
            showLabel: false,
            tabBarStyle: {
              backgroundColor: "#fff",
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
          <Tab.Screen
            name="Home"
            component={Home}
            options={{
              headerShown: false,
            }}
          />
          <Tab.Screen
            name="Camera"
            component={Profile}
            options={{
              headerShown: false,
            }}
          />
          <Tab.Screen
            name="Video"
            component={VideoScreen}
            options={{
              headerShown: false,
            }}
          />
        </Tab.Navigator>
      )}
    </>
  );
};
export default Tabs;
