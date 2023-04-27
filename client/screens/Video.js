import React, { useState, useRef } from "react";
import { View, Text, TouchableOpacity, StyleSheet, Modal } from "react-native";
import { Camera } from "expo-camera";
import { Video } from "expo-av";
const VideoScreen = () => {
  const [isRecording, setIsRecording] = useState(false);

  const [videoUri, setVideoUri] = useState(null);
  const cameraRef = useRef(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [modalContent, setModalContent] = useState("");

  const showModal = (content) => {
    setModalContent("demo content");
    setModalVisible(true);
  };

  const hideModal = () => {
    setModalVisible(false);
  };

  const startRecording = async () => {
    setIsRecording(true);
    const { uri } = await cameraRef.current.recordAsync();
    setVideoUri(uri);
  };

  const stopRecording = async () => {
    setIsRecording(false);
    await cameraRef.current.stopRecording();
  };

  const resetVideo = async () => {
    setIsRecording(false);
    await cameraRef.current.stopRecording();
    setVideoUri(null);
  };

  const renderButtons = () => {
    const buttonStyle = styles.button;
    if (isRecording) {
      return (
        <TouchableOpacity style={buttonStyle} onPress={stopRecording}>
          <Text style={styles.buttonText}>Stop Recording</Text>
        </TouchableOpacity>
      );
    } else if (videoUri) {
      return (
        <View>
          <TouchableOpacity style={buttonStyle} onPress={resetVideo}>
            <Text style={styles.buttonText}>Reset Video</Text>
          </TouchableOpacity>
          <TouchableOpacity style={buttonStyle} onPress={submitVideo}>
            <Text style={styles.buttonText}>Submit Video</Text>
          </TouchableOpacity>
        </View>
      );
    } else {
      return (
        <TouchableOpacity style={buttonStyle} onPress={startRecording}>
          <Text style={styles.buttonText}>Start Recording</Text>
        </TouchableOpacity>
      );
    }
  };
  const submitVideo = async () => {
    try {
      const formData = new FormData();
      formData.append("video", {
        uri: videoUri,
        type: "video/mp4",
        name: "video.mp4",
      });
      const response = await fetch("http://192.168.1.4:5000/upload", {
        method: "POST",
        body: formData,
      });
      const result = await response.text();
      // setResponseText(result.emotions);
      // setModalVisible(true);
      showModal(result);
      console.log(result);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <View style={{ flex: 1 }}>
     <View style={{ flex: 1 }}>
  <View style={{ flex: 1, backgroundColor: "rgba(0,0,0,0.9)" }}>
    {videoUri && (
      <Video
        source={{ uri: videoUri }}
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          bottom: 0,
          right: 0,
        }}
        shouldPlay
        resizeMode="cover"
      />
    )}
  </View>
  <Camera
    ref={cameraRef}
    style={{
      position: "absolute",
      top: 0,
      left: 0,
      bottom: 0,
      right: 0,
    }}
    type={Camera.Constants.Type.front}
  />
</View>

      <View
        style={{
          position: "absolute",
          bottom: 20,
          left: 0,
          right: 0,
          alignItems: "center",
        }}
      >
        {renderButtons()}
      </View>
      <Modal
        transparent={true}
        visible={modalVisible}
        onRequestClose={hideModal}
        animationType="slide"
      >
        <View style={styles.modal}>
          <Text style={styles.modalText}>{modalContent}</Text>
          <TouchableOpacity style={styles.modalButton} onPress={hideModal}>
            <Text style={styles.modalButtonText}>Close</Text>
          </TouchableOpacity>
        </View>
      </Modal>
    </View>
  );
};

export default VideoScreen;

const styles = StyleSheet.create({
  button: {
    backgroundColor: "#3498db",
    padding: 10,
    borderRadius: 5,
    marginBottom: 10,
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
    textAlign: "center",
  },
  modal: {
    backgroundColor: "#fff",
    position: "absolute",
    alignSelf: "center",
    top: "50%",

    width: "80%",
    borderRadius: 10,
    padding: 20,
    zIndex: 10,
  },
  modalText: {
    fontSize: 18,
    marginBottom: 20,
    textAlign: "center",
  },
  modalButton: {
    backgroundColor: "blue",
    padding: 10,
    borderRadius: 5,
  },
  modalButtonText: {
    color: "white",
    fontSize: 16,
  },
});
