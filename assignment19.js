import React, { useState } from "react"
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  StatusBar,
} from "react-native"

export default function App() {
  const [count, setCount] = useState(0)
  const [isDarkMode, setIsDarkMode] = useState(false)

  const handleIncrement = () => {
    setCount(count + 1)
  }

  const handleDecrement = () => {
    if (count > 0) {
      setCount(count - 1)
    }
  }

  const handleReset = () => {
    setCount(0)
  }

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode)
  }

  const backgroundColor = isDarkMode ? "#121212" : "#ffffff"
  const textColor = isDarkMode ? "#ffffff" : "#000000"
  const buttonColor = isDarkMode ? "#333333" : "#e0e0e0"

  return (
    <View style={[styles.container, { backgroundColor }]}>
      <StatusBar
        barStyle={isDarkMode ? "light-content" : "dark-content"}
      />

      <Text style={[styles.title, { color: textColor }]}>
        Simple Digital Counter
      </Text>

      <Text style={[styles.counterText, { color: textColor }]}>
        {count}
      </Text>

      <View style={styles.buttonRow}>
        <TouchableOpacity
          style={[styles.button, { backgroundColor: buttonColor }]}
          onPress={handleDecrement}
        >
          <Text style={[styles.buttonText, { color: textColor }]}>
            - Decrement
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, { backgroundColor: buttonColor }]}
          onPress={handleIncrement}
        >
          <Text style={[styles.buttonText, { color: textColor }]}>
            + Increment
          </Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity
        style={[styles.resetButton, { backgroundColor: buttonColor }]}
        onPress={handleReset}
      >
        <Text style={[styles.buttonText, { color: textColor }]}>
          Reset
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.themeButton, { backgroundColor: buttonColor }]}
        onPress={toggleTheme}
      >
        <Text style={[styles.buttonText, { color: textColor }]}>
          Toggle Theme
        </Text>
      </TouchableOpacity>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },

  title: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 30,
  },

  counterText: {
    fontSize: 70,
    fontWeight: "bold",
    marginBottom: 40,
  },

  buttonRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 20,
  },

  button: {
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 10,
    marginHorizontal: 10,
    minWidth: 140,
    alignItems: "center",
  },

  resetButton: {
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 10,
    marginBottom: 20,
    minWidth: 180,
    alignItems: "center",
  },

  themeButton: {
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 10,
    minWidth: 180,
    alignItems: "center",
  },

  buttonText: {
    fontSize: 18,
    fontWeight: "600",
  },
})
