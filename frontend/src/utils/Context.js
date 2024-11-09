import { createContext, useEffect, useRef, useState } from "react";
export const ContextApp = createContext();

const welcomeMessage = `
Hello! I'm your Procurement Assistant. I can help you explore procurement data, whether you're looking for the total number of orders in a specific period, the quarter with the highest spending, or frequently ordered items. Just ask me a question, and I'll provide the information you need!
`;

// Use environment variable for WebSocket URL
const SERVER_WS_URL = "ws://localhost:9000";

const AppContext = ({ children }) => {
  const [showSlide, setShowSlide] = useState(false);
  const [Mobile, setMobile] = useState(false);
  const [chatValue, setChatValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [socket, setSocket] = useState(null); // Store WebSocket instance here

  const [message, setMessage] = useState([
    {
      text: welcomeMessage,
      isBot: true,
    },
  ]);
  const msgEnd = useRef(null);

  useEffect(() => {
    msgEnd.current.scrollIntoView();
  }, [message]);

  useEffect(() => {
    // Create a WebSocket connection on mount
    const webSocket = new WebSocket(`${SERVER_WS_URL}/chats/ask`);

    webSocket.onopen = () => {
      console.log("WebSocket connected");
    };

    webSocket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    webSocket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    setSocket(webSocket); // Save the WebSocket instance to state

    return () => {
      if (webSocket) {
        webSocket.close(); // Clean up WebSocket connection on component unmount
      }
    };
  }, []);

  useEffect(() => {
    if (socket) {
      socket.onmessage = (event) => {
        // Process the response from the WebSocket server
        const data = JSON.parse(event.data);
        setMessage([
          ...message,
          { text: data?.answer, isBot: true }, // Assuming response has 'data'
        ]);
        setIsLoading(false); // Stop loading after receiving the response
      };
    }
  }, [socket, message]);

  // Send message to WebSocket server
  const sendMsgToSocket = (msg) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ question: msg }));
      setIsLoading(true); // Set loading while waiting for response
    }
  };

  const handleSend = async () => {
    if (!isLoading) {
      const text = chatValue;
      setChatValue("");
      setMessage([...message, { text, isBot: false }]);
      sendMsgToSocket(text); // Send to WebSocket instead of API
    }
  };

  // Enter Click function
  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      handleSend();
    }
  };

  const clearMessages = () => {
    setMessage([
      {
        text: welcomeMessage,
        isBot: true,
      },
    ]);
  };

  return (
    <ContextApp.Provider
      value={{
        showSlide,
        setShowSlide,
        Mobile,
        setMobile,
        chatValue,
        setChatValue,
        handleSend,
        message,
        msgEnd,
        handleKeyPress,
        isLoading,
        clearMessages,
      }}
    >
      {children}
    </ContextApp.Provider>
  );
};
export default AppContext;
